#!/usr/bin/env python3
"""Local storyboard reviewer. Keeps human choices in still_favorites.md."""

from __future__ import annotations

import argparse
import json
import os
import re
import threading
import webbrowser
from datetime import datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent
MANIFEST_PATH = ROOT.parent / "stills_manifest.json"
FAVORITES_PATH = ROOT / "still_favorites.md"


def load_setups() -> list[dict]:
    data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    return [{"index": i, "setup": item["setup"], "slate": item.get("slate", ""),
             "a": Path(item["outputs"][0]).name, "b": Path(item["outputs"][1]).name}
            for i, item in enumerate(data["setups"], start=1)]


def split_markdown_row(line: str) -> list[str]:
    if not line.startswith("|"):
        return []
    return [cell.replace(r"\|", "|").strip()
            for cell in re.split(r"(?<!\\)\|", line)[1:-1]]


def load_review(setups: list[dict]) -> dict[str, dict]:
    review = {s["setup"]: {"favorite": "", "regenerate": False, "direction": ""}
              for s in setups}
    if not FAVORITES_PATH.exists():
        return review
    for line in FAVORITES_PATH.read_text(encoding="utf-8").splitlines():
        cells = split_markdown_row(line)
        if len(cells) < 5 or not cells[0].isdigit():
            continue
        setup = cells[1].strip("`")
        if setup not in review:
            continue
        review[setup]["favorite"] = cells[3] if cells[3] in {"A", "B"} else ""
        if len(cells) >= 7:
            review[setup]["regenerate"] = cells[5].lower() == "yes"
            review[setup]["direction"] = cells[6] if cells[6] != "—" else ""
    return review


def clean_cell(value: str) -> str:
    return value.replace("|", r"\|").replace("\r", " ").replace("\n", " ").strip()


def write_review(setups: list[dict], review: dict[str, dict]) -> None:
    reviewed = sum(1 for item in review.values() if item["favorite"] in {"A", "B"})
    regen = sum(1 for item in review.values() if item["regenerate"])
    lines = [
        "# Storyboard Still Favorites", "",
        "Human selections and regeneration requests for the A/B still pairs in `out/`.",
        "This is the durable handoff file for future AI agents and production work.", "",
        f"- Reviewed: {reviewed} / {len(setups)}", f"- Marked for regeneration: {regen}",
        f"- Updated: {datetime.now().astimezone().isoformat(timespec='seconds')}",
        "- Favorite values: `A` or `B`; `—` means not reviewed yet.", "",
        "| # | Setup | Slate | Favorite | Selected file | Regenerate | Direction |",
        "|---:|---|---|:---:|---|:---:|---|",
    ]
    for s in setups:
        state = review[s["setup"]]
        favorite = state["favorite"]
        selected = s["a"] if favorite == "A" else s["b"] if favorite == "B" else ""
        selected_cell = f"`out/{selected}`" if selected else "—"
        lines.append(f"| {s['index']} | `{s['setup']}` | {clean_cell(s['slate'])} | "
                     f"{favorite or '—'} | {selected_cell} | "
                     f"{'Yes' if state['regenerate'] else 'No'} | "
                     f"{clean_cell(state['direction']) or '—'} |")
    lines += ["", "## Agent guidance", "",
              "- `Selected file` paths are relative to the `codex/` folder.",
              "- Use `Selected file` as the owner's approved still when `Favorite` is `A` or `B`.",
              "- Do not infer a preference where `Favorite` is `—`.",
              "- `Regenerate: Yes` requests a new A/B pair. Preserve the original manifest prompt",
              "  and lock block; apply `Direction` only as an explicit revision note.", ""]
    temp = ROOT / ".still_favorites.md.tmp"
    temp.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temp, FAVORITES_PATH)


HTML = r"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Storyboard A/B Review</title>
<style>
:root{color-scheme:dark;--bg:#101214;--panel:#1a1d20;--line:#31363b;--text:#f1eee7;--muted:#a5abb0;--gold:#efb65a;--green:#70d69a;--red:#ef8a78}*{box-sizing:border-box}body{margin:0;height:100vh;display:grid;grid-template-rows:82px minmax(0,1fr) 116px 60px;background:var(--bg);color:var(--text);font:15px/1.4 system-ui,-apple-system,"Segoe UI",sans-serif;overflow:hidden}button,textarea,input{font:inherit;color:inherit}.topbar{padding:12px 18px;display:grid;grid-template-columns:minmax(260px,1fr) auto minmax(300px,1fr);align-items:center;gap:18px;background:#15181b;border-bottom:1px solid var(--line)}.eyebrow{color:var(--gold);font-size:12px;font-weight:750;letter-spacing:.08em;text-transform:uppercase}h1{margin:2px 0 0;font-size:20px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.progress-wrap{width:min(390px,32vw)}.progress-copy{display:flex;justify-content:space-between;margin-bottom:6px;color:var(--muted);font-size:12px}.progress-track{height:7px;border-radius:99px;overflow:hidden;background:#292d31}.progress-fill{width:0;height:100%;background:linear-gradient(90deg,#c88a2f,var(--gold));transition:width .2s}.top-actions{justify-self:end;display:flex;align-items:center;gap:10px}.status{min-width:118px;text-align:right;color:var(--muted);font-size:13px}.status.saved{color:var(--green)}.secondary,.controls button{border:1px solid var(--line);background:#22262a;border-radius:8px;padding:8px 12px;cursor:pointer}.secondary:hover,.controls button:hover{border-color:#636a70;background:#292e32}main{padding:14px 18px;display:grid;grid-template-columns:1fr 1fr;gap:14px;min-height:0}.choice{position:relative;min-width:0;border:2px solid var(--line);border-radius:12px;background:var(--panel);overflow:hidden;cursor:pointer;display:flex;align-items:center;justify-content:center;transition:.13s}.choice:hover{border-color:#626970;transform:translateY(-1px)}.choice.selected{border-color:var(--gold);box-shadow:0 0 0 2px rgba(239,182,90,.18),0 16px 44px rgba(0,0,0,.3)}.choice img{width:100%;height:100%;object-fit:contain;background:#090a0b}.badge{position:absolute;z-index:1;top:14px;left:14px;width:46px;height:46px;border-radius:10px;display:grid;place-items:center;background:rgba(12,14,16,.84);border:1px solid rgba(255,255,255,.22);font-size:23px;font-weight:800}.choice.selected .badge{background:var(--gold);color:#231806;border-color:var(--gold)}.picked{display:none;position:absolute;z-index:1;right:14px;top:14px;padding:8px 11px;border-radius:999px;background:var(--gold);color:#231806;font-weight:800}.choice.selected .picked{display:block}.filename{position:absolute;left:14px;bottom:12px;padding:6px 9px;border-radius:7px;color:#d7dbde;background:rgba(12,14,16,.8);font:12px ui-monospace,Consolas,monospace}.inspector{padding:12px 18px;display:grid;grid-template-columns:230px minmax(300px,1fr) auto;align-items:center;gap:14px;background:#171a1d;border-top:1px solid var(--line)}.regen-toggle{height:56px;display:flex;align-items:center;gap:10px;padding:0 14px;border:1px solid var(--line);border-radius:10px;background:#202428;cursor:pointer}.regen-toggle:has(input:checked){border-color:var(--red);background:rgba(239,138,120,.08)}.regen-toggle input{width:19px;height:19px;accent-color:var(--red)}.regen-copy strong{display:block}.regen-copy span{color:var(--muted);font-size:12px}.direction{width:100%;height:70px;resize:none;border:1px solid var(--line);border-radius:10px;padding:10px 12px;background:#0f1113;outline:none}.direction:focus{border-color:#687078}.save-note{height:42px;border:1px solid var(--line);border-radius:9px;padding:0 15px;background:#292e32;cursor:pointer}.save-note.dirty{border-color:var(--gold);color:var(--gold)}.footer{padding:9px 18px;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:14px;background:#15181b;border-top:1px solid var(--line)}.controls{display:flex;gap:8px;justify-content:center}.shortcuts{color:var(--muted);font-size:12px}.shortcuts:last-child{text-align:right}kbd{padding:2px 6px;border:1px solid #4a5056;border-bottom-width:2px;border-radius:5px;color:#dce0e3;background:#202428;font:11px ui-monospace,monospace}.overlay{position:fixed;inset:0;z-index:10;background:rgba(8,10,11,.96);display:none;grid-template-rows:70px minmax(0,1fr)}.overlay.open{display:grid}.overview-head{padding:13px 20px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid var(--line)}.overview-head h2{margin:0;font-size:20px}.overview-grid{padding:18px;overflow:auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(245px,1fr));gap:12px;align-content:start}.pick-card{position:relative;text-align:left;border:1px solid var(--line);border-radius:10px;padding:0;background:#181b1e;overflow:hidden;cursor:pointer}.pick-card:hover{border-color:#697178}.pick-card img{width:100%;aspect-ratio:16/9;display:block;object-fit:cover;background:#090a0b}.pick-card .meta{display:block;padding:9px 10px}.pick-card strong{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}.pick-card small{color:var(--muted)}.pick-card .letter{position:absolute;top:8px;left:8px;background:var(--gold);color:#231806;font-weight:800;border-radius:7px;padding:4px 8px}.pick-card .regen{position:absolute;top:8px;right:8px;background:var(--red);color:#27100c;font-weight:750;border-radius:7px;padding:4px 8px}.pick-card.unpicked img{opacity:.3}.pick-card.unpicked .letter{background:#454b50;color:#fff}@media(max-width:900px){body{height:auto;min-height:100vh;display:block;overflow:auto}.topbar{grid-template-columns:1fr}.progress-wrap{width:100%}.top-actions{justify-self:start}main{min-height:900px;grid-template-columns:1fr}.choice{min-height:44vh}.inspector{grid-template-columns:1fr}.footer{position:sticky;bottom:0;grid-template-columns:1fr}.shortcuts{display:none}}
</style></head><body>
<header class="topbar"><div><div class="eyebrow" id="counter">Loading…</div><h1 id="title">Storyboard A/B Review</h1></div><div class="progress-wrap"><div class="progress-copy"><span id="reviewed">0 reviewed</span><span id="remaining">41 remaining</span></div><div class="progress-track"><div class="progress-fill" id="progress"></div></div></div><div class="top-actions"><button class="secondary" id="overviewButton">Review all picks</button><span class="status saved" id="status">Saved</span></div></header>
<main><button class="choice" id="choiceA" data-choice="A" aria-label="Choose A"><span class="badge">A</span><span class="picked">Favorite</span><img id="imageA" alt="Variant A"><span class="filename" id="fileA"></span></button><button class="choice" id="choiceB" data-choice="B" aria-label="Choose B"><span class="badge">B</span><span class="picked">Favorite</span><img id="imageB" alt="Variant B"><span class="filename" id="fileB"></span></button></main>
<section class="inspector"><label class="regen-toggle"><input id="regenerate" type="checkbox"><span class="regen-copy"><strong>Mark for regeneration</strong><span id="regenCount">0 setups marked</span></span></label><textarea class="direction" id="direction" placeholder="What should change in the next A/B pair? Enter saves; Shift+Enter adds a line."></textarea><button class="save-note" id="saveNote">Save direction</button></section>
<footer class="footer"><div class="shortcuts"><kbd>A</kbd>/<kbd>B</kbd> pick · <kbd>U</kbd> clear · <label><input id="autoAdvance" type="checkbox"> auto-advance</label></div><div class="controls"><button id="prev">← Previous</button><button id="unreviewed">Next unreviewed</button><button id="clear">Clear choice</button><button id="next">Next →</button></div><div class="shortcuts"><kbd>←</kbd>/<kbd>→</kbd> navigate</div></footer>
<aside class="overlay" id="overview"><div class="overview-head"><div><h2>Review all picks</h2><span id="overviewSummary"></span></div><button class="secondary" id="closeOverview">Close</button></div><div class="overview-grid" id="overviewGrid"></div></aside>
<script>
let setups=[],review={},current=0,pending=0,noteDirty=false;const $=id=>document.getElementById(id),state=()=>review[setups[current].setup];function setStatus(t,k=''){$('status').textContent=t;$('status').className=`status ${k}`}async function boot(){const r=await fetch('/api/state'),d=await r.json();setups=d.setups;review=d.review;const first=setups.findIndex(s=>!review[s.setup].favorite);current=first<0?0:first;render()}function counts(){const v=Object.values(review);return{done:v.filter(x=>x.favorite).length,regen:v.filter(x=>x.regenerate).length}}function render(){const s=setups[current],x=state(),c=counts();if(!s)return;$('counter').textContent=`Setup ${current+1} of ${setups.length}`;$('title').textContent=`${s.setup} — ${s.slate}`;$('imageA').src=`/image/${encodeURIComponent(s.a)}`;$('imageB').src=`/image/${encodeURIComponent(s.b)}`;$('fileA').textContent=s.a;$('fileB').textContent=s.b;document.querySelectorAll('.choice').forEach(el=>el.classList.toggle('selected',el.dataset.choice===x.favorite));$('reviewed').textContent=`${c.done} reviewed`;$('remaining').textContent=`${setups.length-c.done} remaining`;$('progress').style.width=`${c.done/setups.length*100}%`;$('regenerate').checked=x.regenerate;$('direction').value=x.direction;$('regenCount').textContent=`${c.regen} setup${c.regen===1?'':'s'} marked`;noteDirty=false;$('saveNote').classList.remove('dirty')}async function save(p){pending++;setStatus('Saving…');try{const r=await fetch('/api/update',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)});if(!r.ok)throw Error(await r.text());pending--;setStatus('Saved','saved');return true}catch(e){pending--;setStatus('Save failed');console.error(e);return false}}async function commitNote(){if(!noteDirty)return true;const s=setups[current],x=state();x.direction=$('direction').value.trim();noteDirty=false;$('saveNote').classList.remove('dirty');return save({setup:s.setup,direction:x.direction,regenerate:x.regenerate})}async function choose(v){await commitNote();const s=setups[current];state().favorite=v;render();await save({setup:s.setup,favorite:v});if(v&&$('autoAdvance').checked&&current<setups.length-1){current++;render()}}async function go(d){if(!await commitNote())return;current=(current+d+setups.length)%setups.length;render()}async function goUnreviewed(){if(!await commitNote())return;const start=current;do{current=(current+1)%setups.length;if(!state().favorite)break}while(current!==start);render()}async function toggleRegen(){const s=setups[current],x=state();x.regenerate=$('regenerate').checked;x.direction=$('direction').value.trim();noteDirty=false;render();await save({setup:s.setup,regenerate:x.regenerate,direction:x.direction})}function showOverview(){const c=counts();$('overviewSummary').textContent=`${c.done}/${setups.length} chosen · ${c.regen} marked for regeneration`;$('overviewGrid').innerHTML=setups.map((s,i)=>{const x=review[s.setup],file=x.favorite==='B'?s.b:s.a;return`<button class="pick-card ${x.favorite?'':'unpicked'}" data-index="${i}"><span class="letter">${x.favorite||'—'}</span>${x.regenerate?'<span class="regen">Regenerate</span>':''}<img src="/image/${encodeURIComponent(file)}" alt=""><span class="meta"><strong>${i+1}. ${s.setup}</strong><small>${s.slate}</small></span></button>`}).join('');$('overview').classList.add('open');$('overviewGrid').querySelectorAll('.pick-card').forEach(el=>el.onclick=async()=>{await commitNote();current=Number(el.dataset.index);$('overview').classList.remove('open');render()})}
$('choiceA').onclick=()=>choose('A');$('choiceB').onclick=()=>choose('B');$('prev').onclick=()=>go(-1);$('next').onclick=()=>go(1);$('unreviewed').onclick=goUnreviewed;$('clear').onclick=()=>choose('');$('regenerate').onchange=toggleRegen;$('direction').oninput=()=>{noteDirty=true;setStatus('Unsaved direction');$('saveNote').classList.add('dirty')};$('saveNote').onclick=commitNote;$('overviewButton').onclick=showOverview;$('closeOverview').onclick=()=>$('overview').classList.remove('open');$('autoAdvance').checked=localStorage.getItem('autoAdvance')==='true';$('autoAdvance').onchange=()=>localStorage.setItem('autoAdvance',$('autoAdvance').checked);addEventListener('keydown',e=>{if(e.repeat||e.ctrlKey||e.metaKey||e.altKey)return;if(e.target===$('direction')){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();commitNote().then(()=>$('choiceA').focus())}return}if(['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)||e.target.isContentEditable)return;if(e.key.toLowerCase()==='a')choose('A');else if(e.key.toLowerCase()==='b')choose('B');else if(e.key.toLowerCase()==='u')choose('');else if(e.key==='ArrowLeft')go(-1);else if(e.key==='ArrowRight')go(1);else if(e.key==='Escape')$('overview').classList.remove('open')});addEventListener('beforeunload',e=>{if(pending||noteDirty){e.preventDefault();e.returnValue=''}});boot().catch(e=>{setStatus('Could not load');console.error(e)});
</script></body></html>"""


class ReviewHandler(BaseHTTPRequestHandler):
    setups = load_setups()
    review = load_review(setups)
    lock = threading.Lock()
    allowed_images = {s[key] for s in setups for key in ("a", "b")}

    def log_message(self, format: str, *args) -> None:
        return

    def send_bytes(self, body: bytes, content_type: str, status=HTTPStatus.OK) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, value: object, status=HTTPStatus.OK) -> None:
        self.send_bytes(json.dumps(value).encode(), "application/json; charset=utf-8", status)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path == "/":
            self.send_bytes(HTML.encode(), "text/html; charset=utf-8")
        elif path == "/api/state":
            with self.lock:
                self.review = load_review(self.setups)
                self.send_json({"setups": self.setups, "review": self.review})
        elif path.startswith("/image/"):
            name = unquote(path.removeprefix("/image/"))
            image_path = ROOT / name
            if name not in self.allowed_images or not image_path.is_file():
                self.send_error(HTTPStatus.NOT_FOUND)
            else:
                self.send_bytes(image_path.read_bytes(), "image/jpeg")
        else:
            self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/update":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            payload = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
            setup = payload.get("setup")
            if setup not in {s["setup"] for s in self.setups}:
                raise ValueError("Invalid setup")
            with self.lock:
                self.review = load_review(self.setups)
                item = self.review[setup]
                if "favorite" in payload:
                    if payload["favorite"] not in {"", "A", "B"}:
                        raise ValueError("Invalid favorite")
                    item["favorite"] = payload["favorite"]
                if "regenerate" in payload:
                    item["regenerate"] = bool(payload["regenerate"])
                if "direction" in payload:
                    item["direction"] = str(payload["direction"]).strip()
                write_review(self.setups, self.review)
            self.send_json({"ok": True})
        except ValueError as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
        except Exception as exc:
            self.send_json({"error": str(exc)}, HTTPStatus.INTERNAL_SERVER_ERROR)


def main() -> None:
    parser = argparse.ArgumentParser(description="Review storyboard still pairs in a browser.")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    args = parser.parse_args()
    if not MANIFEST_PATH.is_file():
        raise SystemExit(f"Manifest not found: {MANIFEST_PATH}")
    write_review(ReviewHandler.setups, ReviewHandler.review)
    server = ThreadingHTTPServer(("127.0.0.1", args.port), ReviewHandler)
    url = f"http://127.0.0.1:{args.port}/"
    print(f"Storyboard reviewer: {url}")
    print(f"Selections file: {FAVORITES_PATH}")
    print("Close this window or press Ctrl+C when finished.")
    if not args.no_browser:
        threading.Timer(0.35, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
