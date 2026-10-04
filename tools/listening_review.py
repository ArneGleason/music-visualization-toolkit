"""Serve the existing listening/range-note workflow with local Whisper dictation."""
import argparse
import hashlib
from http.server import ThreadingHTTPServer
import json
import pathlib
import subprocess
import tempfile
import threading
import uuid
import wave
from urllib.parse import urlsplit

from timeline import load_project
from serve import Handler as RangeHandler


def prepare_dictation(audio, wav):
    """Measure decoded samples: browser WebM often has no duration metadata."""
    result = subprocess.run(
        ["ffmpeg", "-v", "error", "-nostdin", "-y", "-i", str(audio),
         "-t", "186", "-vn", "-ac", "1", "-ar", "16000",
         "-c:a", "pcm_s16le", str(wav)],
        capture_output=True, text=True, timeout=30)
    if result.returncode:
        raise ValueError("Could not decode the recording; original audio is retained")
    with wave.open(str(wav), "rb") as decoded:
        duration = decoded.getnframes() / decoded.getframerate()
    if duration <= 0:
        raise ValueError("The recording contains no audio")
    if duration > 185:
        raise ValueError("Dictation must be at most three minutes")
    return duration


def recordings(folder):
    """Group retries of the same audio; expose a transcript when available."""
    found = {}
    for audio in sorted(folder.glob("dictation-*.webm")):
        ident = hashlib.sha256(audio.read_bytes()).hexdigest()
        item = found.setdefault(ident, {
            "id": ident, "audio": audio.name, "text": "", "anchor": None,
            "recordedAt": audio.stat().st_mtime})
        item['recordedAt'] = min(item['recordedAt'], audio.stat().st_mtime)
        if audio.with_suffix('.json').exists():
            item['text'] = json.loads(audio.with_suffix('.json').read_text(encoding='utf-8')).get('text', '')
        if audio.with_suffix('.anchor.json').exists():
            item['anchor'] = json.loads(audio.with_suffix('.anchor.json').read_text(encoding='utf-8'))
    state_path = folder / 'recording-state.json'
    states = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    for ident, item in found.items():
        item['deleted'] = states.get(ident, {}).get('deleted', False)
    return sorted(found.values(), key=lambda item: item['recordedAt'], reverse=True)


def validate_notes(doc, duration):
    ids = set()
    for note in doc['notes']:
        start, end = note['start'], note['end']
        unplaced = start is None and end is None
        if note['id'] in ids or (not unplaced and
                (start is None or end is None or not 0 <= start <= end <= duration)):
            raise ValueError('Invalid or duplicate note anchor')
        if note['status'] not in ('open', 'addressed', 'deleted') or len(note['text']) > 10000:
            raise ValueError('Invalid note')
        ids.add(note['id'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=pathlib.Path)
    parser.add_argument("--port", type=int, default=8768)
    args = parser.parse_args()
    project, base = load_project(args.project)
    root = base / "generated/animatic"
    notes_path = base / "generated/review/listening-notes.json"
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    ui = pathlib.Path(__file__).resolve().parent.parent / "review/listening.html"
    lock = threading.Lock()
    dictation_lock = threading.Lock()

    def notes():
        return json.loads(notes_path.read_text(encoding="utf-8")) if notes_path.exists() else {"revision":0,"notes":[]}

    class Handler(RangeHandler):
        def __init__(self,*a,**kw):
            super().__init__(*a,directory=str(root),**kw)

        def log_message(self,*a):
            pass

        def reply(self,data,status=200,kind="application/json; charset=utf-8"):
            body = data if isinstance(data,bytes) else json.dumps(data,ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type",kind)
            self.send_header("Content-Length",str(len(body)))
            self.send_header("Cache-Control","no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = urlsplit(self.path).path
            if path == "/":
                self.reply(ui.read_bytes(),kind="text/html; charset=utf-8")
            elif path == "/api/notes":
                with lock:
                    self.reply(notes())
            elif path == "/api/project":
                self.reply({"title":project["title"],"slug":project["slug"]})
            elif path == "/api/recordings":
                self.reply({"recordings": recordings(notes_path.parent)})
            elif path.startswith("/api/recordings/") and path.endswith("/audio"):
                ident = path.split('/')[3]
                item = next((r for r in recordings(notes_path.parent) if r['id'] == ident), None)
                if item:
                    self.reply((notes_path.parent/item['audio']).read_bytes(), kind='audio/webm')
                else:
                    self.reply({"error": "Recording not found"}, 404)
            elif path.startswith('/storyboard/'):
                self.directory = str(base/'generated/storyboard')
                self.path = self.path[len('/storyboard'):]
                super().do_GET()
            else:
                super().do_GET()

        def do_POST(self):
            path = urlsplit(self.path).path
            origin = self.headers.get("Origin")
            if origin and origin != f"http://127.0.0.1:{args.port}":
                self.reply({"error":"Unexpected origin"},403)
                return
            try:
                size = int(self.headers.get("Content-Length",0))
                limit = 20*1024*1024 if path=="/api/dictation" else 2*1024*1024
                if not 0<size<=limit:
                    raise ValueError("Invalid request size")
                body = self.rfile.read(size)
                if path == "/api/notes":
                    doc = json.loads(body)
                    duration = json.loads((root/"animatic-data.json").read_text(encoding="utf-8"))["duration"]
                    validate_notes(doc, duration)
                    with lock:
                        if doc["revision"]!=notes()["revision"]:
                            self.reply({"error":"Notes changed; reload before saving"},409)
                            return
                        doc["revision"]+=1
                        temp=notes_path.with_suffix(".tmp")
                        temp.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
                        temp.replace(notes_path)
                    self.reply(doc)
                elif path == '/api/recordings/state':
                    request = json.loads(body)
                    ident = request['id']
                    if not any(r['id'] == ident for r in recordings(notes_path.parent)):
                        raise ValueError('Recording not found')
                    if type(request['deleted']) is not bool:
                        raise ValueError('Invalid recording state')
                    with lock:
                        state_path = notes_path.parent / 'recording-state.json'
                        states = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
                        states[ident] = {'deleted': request['deleted']}
                        temp = state_path.with_suffix('.tmp')
                        temp.write_text(json.dumps(states, indent=2)+'\n', encoding='utf-8')
                        temp.replace(state_path)
                    self.reply({'ok': True})
                elif path in ("/api/dictation", "/api/dictation/retry"):
                    if not dictation_lock.acquire(blocking=False):
                        self.reply({"error":"Another local transcription is running"},409)
                        return
                    try:
                        # Retain recordings locally so a failed transcription is recoverable.
                        if path == "/api/dictation/retry":
                            ident = json.loads(body)['id']
                            item = next((r for r in recordings(notes_path.parent) if r['id'] == ident), None)
                            if not item:
                                raise ValueError('Recording not found')
                            audio = notes_path.parent / item['audio']
                        else:
                            audio = notes_path.parent / ("dictation-"+uuid.uuid4().hex+".webm")
                            audio.write_bytes(body)
                            anchor = self.headers.get('X-Note-Anchor')
                            if anchor:
                                audio.with_suffix('.anchor.json').write_text(
                                    json.dumps(json.loads(anchor)), encoding='utf-8')
                        with tempfile.TemporaryDirectory(prefix="dictation-") as folder:
                            wav = pathlib.Path(folder) / "recording.wav"
                            prepare_dictation(audio, wav)
                            result=subprocess.run([project["alignmentRuntime"]["python"],
                                                   str(pathlib.Path(__file__).with_name("transcribe_note.py")),
                                                   str(args.project.resolve()),str(wav)],capture_output=True,text=True,
                                                   encoding="utf-8",timeout=180,check=True)
                        transcript = json.loads(result.stdout.strip().splitlines()[-1])
                        audio.with_suffix(".json").write_text(
                            json.dumps(transcript, ensure_ascii=False)+"\n", encoding="utf-8")
                        transcript['recordingId'] = hashlib.sha256(audio.read_bytes()).hexdigest()
                        self.reply(transcript)
                    finally:
                        dictation_lock.release()
                else:
                    self.reply({"error":"Not found"},404)
            except (ValueError,KeyError,TypeError,subprocess.SubprocessError) as error:
                self.reply({"error":str(error)},400)

    print(f"Listening notes: http://127.0.0.1:{args.port}",flush=True)
    ThreadingHTTPServer(("127.0.0.1",args.port),Handler).serve_forever()


if __name__=="__main__":
    main()
