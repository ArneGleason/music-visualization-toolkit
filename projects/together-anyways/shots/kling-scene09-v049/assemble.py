"""Select reviewed Scene 9 sources while preserving the musical edit."""
import html
import json
import shutil
import subprocess
from pathlib import Path

NOTES = Path(__file__).resolve().parent
PROJECT = NOTES.parents[1]
OUTPUT = PROJECT / 'generated/kling-scene09-v049'


def main():
    batch = json.loads((NOTES / 'batch.json').read_text())
    score = json.loads((PROJECT / 'shots/shotlist.json').read_text())
    cards = []
    for entry in batch['shots']:
        video = OUTPUT / (entry['shotId'] + '.mp4')
        media = json.loads(subprocess.check_output([
            'ffprobe', '-v', 'error', '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate,nb_frames,duration',
            '-of', 'json', str(video)]))['streams'][0]
        assert media['r_frame_rate'] == '24/1'
        shot = next(s for s in score['shots'] if s['id'] == entry['shotId'])
        start = entry['sourceInFrame']
        end = start + shot['frames']
        count = int(media['nb_frames'])
        assert start >= 24 and count - end >= 24
        shot['videoSource'] = str(video.relative_to(PROJECT))
        shot['videoEdit'] = {'sourceInFrame': start}
        shot['status'] = 'motion_review'
        shot['videoHandles'].update(
            status='generated', editInSourceFrame=start,
            editOutSourceFrameExclusive=end, availableHeadFrames=start,
            availableTailFrames=count-end,
            sourceStartMasterFrame=shot['startFrame']-start,
            sourceEndMasterFrameExclusive=shot['startFrame']-start+count,
            note='Kling 4 v049; selected motion with at least one second of source handles.')
        entry.update(media=media, localVideo=shot['videoSource'], status='selected_for_review')
        cards.append(f'''<section><h2>{entry['displayId']} · {html.escape(shot['title'])}</h2>
<video controls loop preload="metadata" src="{video.name}"></video>
<p>Source in {start/24:.3f}s · Play length {shot['frames']/24:.3f}s ({shot['frames']} frames)</p>
<p>{html.escape(entry.get('reviewNote', ''))}</p>
<details><summary>Direction</summary><p>{html.escape(entry['prompt'])}</p></details></section>''')
    stable = PROJECT / 'generated/storyboard/first-run-starters-v001/first-run-clean-animatic-v001.mp4'
    before = OUTPUT / 'before-scene09-motion.mp4'
    if not before.exists():
        shutil.copy2(stable, before)
    (PROJECT / 'shots/shotlist.json').write_text(json.dumps(score, indent=2) + '\n')
    batch.update(status='complete_selected_for_review', creditsSpent=sum(e['credits'] for e in batch['shots']))
    (NOTES / 'batch.json').write_text(json.dumps(batch, indent=2) + '\n')
    (OUTPUT / 'review.html').write_text('''<!doctype html><html><meta charset="utf-8">
<title>Scene 9 · Clean motion review</title><style>
body{font:17px system-ui;background:#17201c;color:#eee;margin:30px}
main{display:grid;grid-template-columns:1fr 1fr;gap:24px}video{width:100%}
p{white-space:pre-wrap}a{color:#9ed7ca}</style><h1>Scene 9 · A fine find</h1>
<a href="http://127.0.0.1:8767/">Full-song animatic</a><main>''' + ''.join(cards) + '</main></html>')


if __name__ == '__main__':
    main()
