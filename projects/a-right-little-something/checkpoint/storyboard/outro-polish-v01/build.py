"""Assemble V64 with original audio, exact cues, and preserved V63."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT = Path(__file__).resolve().parent
BASE = OUT.parents[2]
ROOT = BASE.parents[1]
sys.path.insert(0, str(ROOT/'tools'))
from lyric_overlay import write_lyrics

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, data):
    path.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def run(args, cwd=None):
    subprocess.run(['ffmpeg','-y','-v','error',*args],check=True,cwd=cwd)

def probe(path):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(path)]))['streams'][0]

codec = ['-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv']
plan = read(OUT/'assembly-plan.json')
entries = plan['entries']
for name in ['clips','segments','fonts']:
    (OUT/name).mkdir(exist_ok=True)

for e in entries:
    count = e['frames']+(0 if e['shot']=='contact-032' else 8)
    if e.get('effect'):
        folder = OUT/(e['effect']+'-frames')
        assert len(list(folder.glob('frame_*.png'))) == count, (folder,count)
        source = OUT/(e['effect']+'-effect.mp4')
        run(['-framerate','24','-i',str(folder/'frame_%04d.png'),'-frames:v',str(count),*codec,str(source)])
        e['revisedSource'] = source.relative_to(BASE).as_posix()
        e['compositor'] = (OUT/(e['effect']+'.blend')).relative_to(BASE).as_posix()
        lead = 0
    else:
        source = BASE/e['source']
        lead = e['sourceIn']
    if e.get('reverse'):
        # Preserve the exact V63 33-frame source interval, in reverse. The
        # following dissolve uses preceding source frames as outgoing handles.
        start = lead-8
        end = lead+e['frames']
        vf = f'trim=start_frame={start}:end_frame={end},reverse,setpts=N/(24*TB)'
        e['reverseFrameMap'] = dict(sourceFirstFrame=end,sourceLastFrame=lead+1,editFrames=e['frames'],outgoingHandleFrames=list(range(lead,lead-8,-1)))
    else:
        vf = f'trim=start_frame={lead}:end_frame={lead+count},setpts=N/(24*TB)'
    vf += ',scale=1920:1080,setsar=1'
    dest = OUT/'clips'/(e['shot']+'.mp4')
    run(['-reinit_filter','0','-i',str(source),'-vf',vf,'-frames:v',str(count),*codec,str(dest)])
    assert int(probe(dest)['nb_frames']) == count
    e['clip'] = dest.relative_to(BASE).as_posix()
    print('Prepared clip',e['shot'],count,flush=True)

segments = []
for i,e in enumerate(entries):
    n = e.get('transition',{}).get('frames',0) if i else 0
    if n:
        prev = entries[i-1]
        dest = OUT/'segments'/(e['shot']+'-dissolve.mp4')
        fc = (f"[0:v]trim=start_frame={prev['frames']}:end_frame={prev['frames']+n},setpts=N/(24*TB)[a];"
              f"[1:v]trim=start_frame=0:end_frame={n},setpts=N/(24*TB)[b];"
              f"[a][b]blend=all_expr='A*(1-(T*24+1)/{n+1})+B*((T*24+1)/{n+1})'[v]")
        run(['-i',str(BASE/prev['clip']),'-i',str(BASE/e['clip']),'-filter_complex',fc,'-map','[v]','-frames:v',str(n),*codec,str(dest)])
        assert int(probe(dest)['nb_frames']) == n
        segments.append(dest)
    dest = OUT/'segments'/(e['shot']+'-body.mp4')
    run(['-i',str(BASE/e['clip']),'-vf',f"trim=start_frame={n}:end_frame={e['frames']},setpts=N/(24*TB)",'-frames:v',str(e['frames']-n),*codec,str(dest)])
    assert int(probe(dest)['nb_frames']) == e['frames']-n
    segments.append(dest)
(OUT/'concat.txt').write_text(''.join("file '"+p.as_posix()+"'\n" for p in segments),encoding='utf-8')
run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-an','-c','copy',str(OUT/'motion-picture.mp4')])
assert int(probe(OUT/'motion-picture.mp4')['nb_frames']) == 820

data = read(BASE/'generated/animatic/animatic-data.json')
captions = copy.deepcopy(data)
captions['phrases'] = [p for p in captions['phrases'] if p['endFrameExclusive']>4446 and p['startFrame']<5266]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame'] -= 4445
        item['endFrameExclusive'] -= 4445
style = read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
shutil.copy2('C:/Windows/Fonts/georgia.ttf',OUT/'fonts/georgia.ttf')
title = '''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Georgia,72,&H00E9F2FF,&H00E9F2FF,&H00201610,&H80201610,0,0,0,0,100,100,0,0,1,1.5,2,8,50,50,50,1
Style: Credit,Georgia,30,&H00E9F2FF,&H00E9F2FF,&H00201610,&H80201610,0,0,0,0,100,100,0,0,1,1,1,8,50,50,50,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:30.79,0:00:34.17,Title,,0,0,0,,{\\pos(960,850)\\fad(500,0)}A Right Little Something
Dialogue: 0,0:00:30.79,0:00:34.17,Credit,,0,0,0,,{\\pos(960,945)\\fad(500,0)}© 2026 Arne Gleason
'''
(OUT/'title.ass').write_text(title,encoding='utf-8')
source = BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v63.mp4'
run(['-reinit_filter','0','-i','motion-picture.mp4','-i',str(source),'-filter_complex',
     '[0:v]ass=lyrics.ass:fontsdir=fonts,ass=title.ass:fontsdir=fonts[v];[1:a]atrim=start=185.208333333333:end=219.375,asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v','820','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'],cwd=OUT)
assert int(probe(OUT/'timed-still-board.mp4')['nb_frames']) == 820

before = read(BASE/'shots/shotlist.json')
register = copy.deepcopy(before)
for e in entries:
    s = next(s for s in register['storyboardProposals'] if s['id']==e['shot'])
    s.update(startFrame=e['startFrame'],endFrameExclusive=e['endFrameExclusive'],frames=e['frames'])
    s['motionSelection'] = dict(id=e['shot']+'-v64',motionRef=e['clip'],sourceEditStartFrame=1,editFrames=e['frames'],draftForReview=True,userSelected=False,status='V64 local editorial revision for review')
    if 'compositor' in e:
        s['motionSelection']['compositor'] = e['compositor']
    s['motionRef'] = e['clip']
    if e.get('transition'):
        s['editorialTransition'] = e['transition']
    if e.get('reverse'):
        s['motionSelection']['reverseFrameMap'] = e['reverseFrameMap']
    if e['shot'] in ['contact-026','contact-027']:
        s['timingRevision'] = 'V64: System View advances to DAW bar 71 beat 2, frame 4484 / 3:06.792; four-frame dissolve; next travel cue stays frame 4649.'
    if e['shot']=='contact-032':
        s['compositePlan'].update(harperFade=dict(startFrame=5137,endFrame=5185),endTitle=dict(text='A Right Little Something',copyright='© 2026 Arne Gleason',startFrame=5185,fullyVisibleFrame=5197),compositor=e['compositor'])
spec = dict(id='first-contact-v01',output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=source.relative_to(BASE).as_posix(),useMotion=True,
            shotIds=[e['shot'] for e in entries],motionShotIds=[e['shot'] for e in entries],draftForReview=True,
            mediaLabel='Outro polish / earlier system, sphere optics and end title',
            presentation='Earlier system cut, local camera moves, reversed Travel 28, cyan sphere transmission/refraction, Harper fade and closing title.',
            continuationNotes='V64 local outro polish; no new generation credits. System cut frame 4484, reverse Travel 28, sphere optics on Travel 27, extra spectacle motion. Harper fades 3:34–3:36; title and copyright then appear. V63 retained.')
save(OUT/'review-options.json',spec)
save(BASE/'shots/shotlist.json',register)
try:
    subprocess.run([sys.executable,str(ROOT/'tools/insert_still_storyboard.py'),str(BASE/'project.json'),str(OUT/'review-options.json'),'--version','v64'],check=True)
except BaseException:
    save(BASE/'shots/shotlist.json',before)
    raise
register = read(BASE/'shots/shotlist.json')
register['reviewEdits']['v64'].update(type='Local editorial and Blender outro polish',newPaidCredits=0,preservedVersion='v63',reviewStatus='Pending user review',reviewNotes='outro-v63-review.json')
register['firstContactSequence'].update(animaticVersion='v64',status='V64 outro polish assembled; review pending',reviewUrl='http://127.0.0.1:8768/?v=v64')
for e in entries:
    s = next(s for s in register['storyboardProposals'] if s['id']==e['shot'])
    kind = 'Blender composite or local camera move' if e.get('effect') else 'Reversed native motion' if e.get('reverse') else 'Retained native motion'
    s['animaticPlacement']['kind'] = kind
    s['status'] = 'V64 local revision review pending'
    for stored in register['reviewEdits']['v64']['entries']:
        if stored['shot']==e['shot']:
            stored.update(s['animaticPlacement'])
save(BASE/'shots/shotlist.json',register)
save(OUT/'assembly-plan.json',plan)
save(OUT/'verification.json',dict(fullFrames=5265,fps=24,width=1920,height=1080,sectionFrames=820,newPaidCredits=0,
      systemStartFrame=4484,systemFirstFullFrame=4488,harperFadeStartFrame=5137,harperFadeEndFrame=5185,titleFirstFrame=5185,titleFullyVisibleFrame=5197,
      reversedShot='contact-028-travel',v63Preserved=source.exists(),audio='V63 original AAC packets verified identical by insertion tool',reviewStatus='Pending user review'))
(OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>V64 outro polish</title><style>body{background:#10242a;color:#eee4d2;font:16px/1.5 system-ui;max-width:1100px;margin:30px auto;padding:0 24px}a{color:#9cdfea}video{width:100%}</style><h1>V64 · Outro polish</h1><p><a href="/?v=v64">Full animatic</a> · <a href="/?v=v63">V63 comparison</a></p><p>Earlier system view, more motion, reverse travel, subtle sphere optics, and closing title. No new generation credits.</p><video controls src="timed-still-board.mp4"></video>''',encoding='utf-8')
print('V64 assembled: 5265 frames; original audio; no new credits.',flush=True)
