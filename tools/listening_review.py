"""Serve the existing listening/range-note workflow with local Whisper dictation."""
import argparse
from http.server import ThreadingHTTPServer
import json
import pathlib
import subprocess
import tempfile
import threading
import uuid
from urllib.parse import urlsplit

from timeline import load_project
from serve import Handler as RangeHandler


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
                    ids = set()
                    for note in doc["notes"]:
                        if note["id"] in ids or not 0<=note["start"]<=note["end"]<=duration:
                            raise ValueError("Invalid or duplicate note anchor")
                        if note["status"] not in ("open","addressed") or len(note["text"])>10000:
                            raise ValueError("Invalid note")
                        ids.add(note["id"])
                    with lock:
                        if doc["revision"]!=notes()["revision"]:
                            self.reply({"error":"Notes changed; reload before saving"},409)
                            return
                        doc["revision"]+=1
                        temp=notes_path.with_suffix(".tmp")
                        temp.write_text(json.dumps(doc,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
                        temp.replace(notes_path)
                    self.reply(doc)
                elif path == "/api/dictation":
                    if not dictation_lock.acquire(blocking=False):
                        self.reply({"error":"Another local transcription is running"},409)
                        return
                    try:
                        # Retain recordings locally so a failed transcription is recoverable.
                        audio = notes_path.parent / ("dictation-"+uuid.uuid4().hex+".webm")
                        audio.write_bytes(body)
                        probe=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration",
                                              "-of","csv=p=0",str(audio)],capture_output=True,text=True,timeout=15,check=True)
                        if float(probe.stdout)>185:
                            raise ValueError("Dictation must be at most three minutes")
                        result=subprocess.run([project["alignmentRuntime"]["python"],
                                               str(pathlib.Path(__file__).with_name("transcribe_note.py")),
                                               str(args.project.resolve()),str(audio)],capture_output=True,text=True,
                                               encoding="utf-8",timeout=180,check=True)
                        self.reply(json.loads(result.stdout.strip().splitlines()[-1]))
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
