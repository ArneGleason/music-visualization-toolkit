#!/usr/bin/env python3
"""
Build the review galleries for the storyboard.

    ./.venv/bin/python3 tools/board_gallery.py refs      -> board/refs.html
    ./.venv/bin/python3 tools/board_gallery.py contact   -> board/contact.html
    ./.venv/bin/python3 tools/board_gallery.py both

Dependency-light on purpose: plain HTML referencing the PNGs on disk, no
bundling, no copying. Missing images render as a labelled gap rather than a
broken icon, so the gallery doubles as a progress report — open it at any
point and see exactly what is still to generate.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mvlib import ROOT, load  # noqa: E402

CSS = """
:root{color-scheme:dark;--bg:#0b0c10;--panel:#13151b;--line:#262b36;
      --text:#d7dbe3;--muted:#858d9b;--gold:#d2aa65;--blue:#8db8ff}
*{box-sizing:border-box}
body{margin:0;padding:26px;background:var(--bg);color:var(--text);
     font:13px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
button,textarea{font:inherit}
h1{font-size:22px;margin:0 0 3px} h2{font-size:14px;margin:32px 0 11px;
   color:#9ca4b2;text-transform:uppercase;letter-spacing:.09em;font-weight:650}
.page-head{display:flex;align-items:flex-start;justify-content:space-between;gap:20px;
           margin-bottom:22px}
.sub{color:#727a88}.sub strong{color:#aeb5c1}
.toolbar{display:flex;align-items:center;gap:10px;flex:none}
.button{appearance:none;border:1px solid #343b49;border-radius:7px;background:#1b1f28;
        color:#e7eaf0;padding:8px 12px;cursor:pointer}
.button:hover{background:#242a35;border-color:#465063}.button:focus-visible,
.frame-card:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.button.primary{background:#d9e4f7;color:#111722;border-color:#d9e4f7;font-weight:650}
.button.primary:hover{background:#fff}.note-count{color:#7f8795;min-width:58px}
.grid{display:grid;gap:14px}
.g4{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}
.g6{grid-template-columns:repeat(auto-fill,minmax(212px,1fr))}
.card{position:relative;background:var(--panel);border:1px solid #1f232c;
      border-radius:8px;overflow:hidden}
.frame-card{cursor:pointer;transition:transform .12s ease,border-color .12s ease,
            box-shadow .12s ease}
.frame-card:hover{transform:translateY(-2px);border-color:#3b4351;
                  box-shadow:0 8px 24px #0008}
.card img{display:block;width:100%;aspect-ratio:16/9;object-fit:cover;background:#0d0f14}
.card .miss{display:flex;align-items:center;justify-content:center;
     aspect-ratio:16/9;background:repeating-linear-gradient(45deg,#101219,
     #101219 9px,#141721 9px,#141721 18px);color:#464d5a}
.meta{padding:8px 10px}
.id{font-family:ui-monospace,Menlo,monospace;color:#e3e7ee}
.dim{color:#6c7381} .lyr{color:#b39a6a;font-style:italic;margin-top:3px}
.act{color:#8d949f;margin-top:4px}
.tag{display:inline-block;padding:1px 6px;border-radius:3px;background:#1c2029;
     color:#8b93a1;font-size:11px;margin-right:4px}
.note-badge{display:none;position:absolute;right:8px;top:8px;padding:3px 7px;
            border-radius:999px;background:#f1c779;color:#1b150b;font-size:11px;
            font-weight:700;box-shadow:0 2px 10px #0008}
.note-badge.on{display:block}
dialog{padding:0;border:1px solid #343b49;border-radius:12px;background:#101217;
       color:var(--text);width:min(1500px,96vw);height:min(920px,94vh);
       box-shadow:0 28px 90px #000d}
dialog::backdrop{background:#030408e8;backdrop-filter:blur(5px)}
.detail-shell{display:grid;grid-template-rows:auto minmax(0,1fr) auto;height:100%}
.detail-head{display:flex;align-items:center;justify-content:space-between;gap:16px;
             padding:12px 14px;border-bottom:1px solid var(--line)}
.detail-title{font-size:17px;font-weight:700}.detail-position{color:var(--muted);margin-left:9px}
.icon-button{appearance:none;border:0;background:transparent;color:#adb4c0;
             font-size:23px;line-height:1;padding:4px 8px;cursor:pointer;border-radius:6px}
.icon-button:hover{background:#252a34;color:white}
.detail-body{display:grid;grid-template-columns:minmax(0,2fr) minmax(300px,430px);
             min-height:0}
.image-stage{display:flex;align-items:center;justify-content:center;min-width:0;
             min-height:0;padding:18px;background:#08090c}
.image-stage img{display:block;max-width:100%;max-height:100%;object-fit:contain;
                 box-shadow:0 12px 44px #000b}
.detail-missing{color:#697180}.detail-side{overflow:auto;padding:20px;border-left:1px solid var(--line)}
.detail-kicker{color:#87909e;margin-bottom:13px}.detail-lyric{color:#d2ae70;
              font-style:italic;margin:0 0 12px}.detail-action{color:#b4bac4;margin:0 0 22px}
.note-label{display:block;color:#e0e4eb;font-weight:650;margin-bottom:7px}
.note-help{color:#737c8a;font-weight:400;float:right}
textarea{display:block;width:100%;min-height:220px;resize:vertical;border:1px solid #343b49;
         border-radius:8px;background:#0b0d12;color:#eef1f5;padding:12px;line-height:1.5}
textarea:focus{outline:2px solid #729de0;border-color:transparent}
.save-state{color:#747d8b;margin-top:7px;min-height:20px}
.detail-nav{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:12px;
            padding:12px 14px;border-top:1px solid var(--line)}
.detail-nav .next{justify-self:end}.keys{color:#697180;text-align:center}
@media(max-width:820px){body{padding:16px}.page-head{display:block}.toolbar{margin-top:14px}
  dialog{width:100vw;height:100vh;max-width:none;max-height:none;border-radius:0}
  .detail-body{grid-template-columns:1fr;grid-template-rows:minmax(260px,48vh) 1fr}
  .detail-side{border-left:0;border-top:1px solid var(--line)}.keys{display:none}}
"""

CONTACT_JS = r"""
(() => {
  const source = document.getElementById('frame-data');
  if (!source) return;
  const frames = JSON.parse(source.textContent);
  const storageKey = 'mv-storyboard-frame-notes-v1';
  const cards = [...document.querySelectorAll('.frame-card')];
  const dialog = document.getElementById('detail');
  const image = document.getElementById('detail-image');
  const missing = document.getElementById('detail-missing');
  const title = document.getElementById('detail-title');
  const position = document.getElementById('detail-position');
  const kicker = document.getElementById('detail-kicker');
  const lyric = document.getElementById('detail-lyric');
  const action = document.getElementById('detail-action');
  const note = document.getElementById('detail-note');
  const saveState = document.getElementById('save-state');
  const noteCount = document.getElementById('note-count');
  let active = 0;
  let lastTrigger = null;
  let storageAvailable = true;
  let notes = {};

  try { notes = JSON.parse(localStorage.getItem(storageKey) || '{}'); }
  catch (_) { notes = {}; storageAvailable = false; }

  function nonempty(value) { return Boolean((value || '').trim()); }
  function saveNotes() {
    try { localStorage.setItem(storageKey, JSON.stringify(notes)); }
    catch (_) { storageAvailable = false; }
  }
  function refreshBadges() {
    let count = 0;
    cards.forEach((card) => {
      const has = nonempty(notes[card.dataset.id]);
      card.querySelector('.note-badge').classList.toggle('on', has);
      if (has) count += 1;
    });
    noteCount.textContent = count ? `${count} noted` : 'No notes';
    document.getElementById('export-notes').textContent =
      count ? `Export notes (.md) · ${count}` : 'Export notes (.md)';
  }
  function render(index) {
    active = (index + frames.length) % frames.length;
    const frame = frames[active];
    title.textContent = frame.id;
    position.textContent = `${active + 1} of ${frames.length}`;
    kicker.textContent = `${frame.section.replaceAll('-', ' ')} · ${frame.t0.toFixed(1)}s · ${frame.dur.toFixed(1)}s · ${frame.world} / ${frame.cam}`;
    lyric.textContent = frame.lyric || '';
    lyric.hidden = !frame.lyric;
    action.textContent = frame.action || 'No action specified.';
    image.hidden = !frame.exists;
    missing.hidden = frame.exists;
    if (frame.exists) {
      image.src = frame.image;
      image.alt = `${frame.id}: ${frame.action || 'storyboard frame'}`;
    }
    note.value = notes[frame.id] || '';
    saveState.textContent = storageAvailable ? 'Notes save automatically in this browser.' : 'Browser storage unavailable; export before closing.';
  }
  function openFrame(index, trigger) {
    lastTrigger = trigger || cards[index];
    render(index);
    if (!dialog.open) dialog.showModal();
    document.getElementById('detail-close').focus();
  }
  function closeDetail() { dialog.close(); }
  function move(delta) { render(active + delta); }

  cards.forEach((card, index) => {
    card.addEventListener('click', () => openFrame(index, card));
    card.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault(); openFrame(index, card);
      }
    });
  });
  document.getElementById('detail-close').addEventListener('click', closeDetail);
  document.getElementById('prev-frame').addEventListener('click', () => move(-1));
  document.getElementById('next-frame').addEventListener('click', () => move(1));
  dialog.addEventListener('click', (event) => { if (event.target === dialog) closeDetail(); });
  dialog.addEventListener('close', () => { if (lastTrigger) lastTrigger.focus(); });
  document.addEventListener('keydown', (event) => {
    if (!dialog.open || event.target === note) return;
    if (event.key === 'ArrowLeft') { event.preventDefault(); move(-1); }
    if (event.key === 'ArrowRight') { event.preventDefault(); move(1); }
  });
  note.addEventListener('input', () => {
    const id = frames[active].id;
    if (nonempty(note.value)) notes[id] = note.value;
    else delete notes[id];
    saveNotes(); refreshBadges();
    saveState.textContent = storageAvailable ? 'Saved locally.' : 'Stored for this session only; export before closing.';
  });

  document.getElementById('export-notes').addEventListener('click', () => {
    const selected = frames.filter((frame) => nonempty(notes[frame.id]));
    if (!selected.length) { alert('Add a note to at least one frame first.'); return; }
    const lines = ['# Storyboard revision notes', '',
      `Exported ${new Date().toLocaleString()}. ${selected.length} frame(s) noted.`, ''];
    selected.forEach((frame) => {
      const end = frame.t0 + frame.dur;
      lines.push(`## ${frame.id} — ${frame.section.replaceAll('-', ' ')}`, '',
        `- Time: ${frame.t0.toFixed(1)}s–${end.toFixed(1)}s`,
        `- World / camera: ${frame.world} / ${frame.cam}`,
        `- Image: ${frame.file}`, '',
        `**Current action:** ${frame.action || '—'}`, '',
        '**Revision notes:**', '', notes[frame.id].trim(), '');
    });
    const blob = new Blob([lines.join('\n')], {type: 'text/markdown;charset=utf-8'});
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url; link.download = 'storyboard-feedback.md'; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });
  refreshBadges();
})();
"""


def card(img_rel, title, lines, classes="", attrs="", alt=""):
    p = ROOT / img_rel
    if p.exists():
        media = (f'<img src="{html.escape(img_rel.split("board/",1)[-1])}" '
                 f'loading="lazy" alt="{html.escape(alt)}">')
    else:
        media = ('<div class="miss" style="color:#464d5a">not generated</div>')
    body = "".join(lines)
    extra = f" {attrs}" if attrs else ""
    return (f'<article class="card {classes}"{extra}>{media}'
            f'<div class="meta">{title}{body}</div></article>')


def build_refs(d):
    out = [f'<h1>Reference sheets</h1><div class="sub">'
           f'{len(d["sheets"])} canonical files · each is ONE image containing '
           f'the stated number of views · rejects live in board/rejects/</div>']
    for kind, label in (("character", "Character"), ("world", "World plates"),
                        ("object", "Object plates")):
        group = [s for s in d["sheets"] if s["kind"] == kind]
        if not group:
            continue
        out.append(f"<h2>{label}</h2><div class='grid g4'>")
        for s in group:
            out.append(card(s["file"], f'<span class="id">{s["id"]}</span>', [
                f'<div class="dim">{s["views"]} view(s) · '
                f'{" ".join(f"<span class=tag>{l}</span>" for l in s["locks"])}</div>',
                f'<div class="dim">{s["file"]}</div>',
                (f'<div class="act">attaches {", ".join(s["attach"])}</div>'
                 if s["attach"] else ""),
            ]))
        out.append("</div>")
    return "".join(out)


def build_contact(d):
    frames = d["frames"]
    have = sum(1 for f in frames if (ROOT / f["file"]).exists())
    out = [f'<header class="page-head"><div><h1>Storyboard</h1><div class="sub">'
           f'<strong>{have} of {len(frames)}</strong> frames generated · click any '
           f'frame to review it large · notes save locally</div></div><div class="toolbar">'
           f'<span class="note-count" id="note-count">No notes</span>'
           f'<button class="button primary" id="export-notes" type="button">'
           f'Export notes (.md)</button></div></header>']
    cur = None
    frame_data = []
    for index, f in enumerate(frames):
        if f["section"] != cur:
            if cur is not None:
                out.append("</div>")
            cur = f["section"]
            out.append(f"<h2>{cur.replace('-', ' ')}</h2><div class='grid g6'>")
        frame_data.append({
            "id": f["id"], "section": f["section"], "t0": f["t0"],
            "dur": f["dur"], "world": f["world"], "cam": f["cam"],
            "lyric": f["lyric"], "action": f["action"], "file": f["file"],
            "image": f["file"].split("board/", 1)[-1],
            "exists": (ROOT / f["file"]).exists(),
        })
        out.append(card(f["file"], f'<span class="id">{f["id"]}</span> '
                        f'<span class="dim">{f["t0"]:.1f}s · {f["dur"]:.1f}s</span>', [
            f'<div class="dim">{f["world"]} / {f["cam"]}</div>',
            (f'<div class="lyr">{html.escape(f["lyric"])}</div>' if f["lyric"] else ""),
            (f'<div class="act">{html.escape(f["action"])}</div>' if f["action"] else ""),
            '<span class="note-badge">Note</span>',
        ], classes="frame-card", attrs=(f'tabindex="0" role="button" '
             f'data-index="{index}" data-id="{f["id"]}" '
             f'aria-label="Open {f["id"]} detail view"'),
             alt=f'{f["id"]}: {f["action"]}') )
    if cur is not None:
        out.append("</div>")
    payload = json.dumps(frame_data, ensure_ascii=False).replace("<", "\\u003c")
    out += [
        '<dialog id="detail"><div class="detail-shell">'
        '<header class="detail-head"><div><span class="detail-title" id="detail-title">'
        '</span><span class="detail-position" id="detail-position"></span></div>'
        '<button class="icon-button" id="detail-close" type="button" aria-label="Close">×</button>'
        '</header><div class="detail-body"><div class="image-stage">'
        '<img id="detail-image" alt=""><div class="detail-missing" id="detail-missing" hidden>'
        'Frame not generated</div></div><aside class="detail-side">'
        '<div class="detail-kicker" id="detail-kicker"></div>'
        '<p class="detail-lyric" id="detail-lyric"></p>'
        '<p class="detail-action" id="detail-action"></p>'
        '<label class="note-label" for="detail-note">Revision notes '
        '<span class="note-help">autosaved</span></label>'
        '<textarea id="detail-note" placeholder="What should change? Mention composition, '
        'performance, continuity, props, lighting, camera, or story clarity…"></textarea>'
        '<div class="save-state" id="save-state"></div></aside></div>'
        '<footer class="detail-nav"><button class="button" id="prev-frame" type="button">'
        '← Previous</button><div class="keys">←/→ navigate · Esc closes</div>'
        '<button class="button next" id="next-frame" type="button">Next →</button></footer>'
        '</div></dialog>',
        f'<script type="application/json" id="frame-data">{payload}</script>',
        f'<script>{CONTACT_JS}</script>',
    ]
    return "".join(out)


def page(title, body):
    return (f"<!doctype html><html><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{title}</title><style>{CSS}</style></head><body>{body}</body></html>")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("what", nargs="?", default="both",
                    choices=["refs", "contact", "both"])
    a = ap.parse_args()

    d = load(ROOT / "board" / "prompts.json")
    if a.what in ("refs", "both"):
        (ROOT / "board" / "refs.html").write_text(
            page("Reference sheets", build_refs(d)))
        n = sum(1 for s in d["sheets"] if (ROOT / s["file"]).exists())
        print(f"  board/refs.html      {n}/{len(d['sheets'])} sheets present")
    if a.what in ("contact", "both"):
        (ROOT / "board" / "contact.html").write_text(
            page("Storyboard", build_contact(d)))
        n = sum(1 for f in d["frames"] if (ROOT / f["file"]).exists())
        print(f"  board/contact.html   {n}/{len(d['frames'])} frames present")


if __name__ == "__main__":
    main()
