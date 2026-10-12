"""Assemble V65, retaining unchanged V64/V63 picture segments and master audio."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys

OUT=Path(__file__).resolve().parent
BASE=OUT.parents[2]
ROOT=BASE.parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from lyric_overlay import write_lyrics

def read(p):
    return json.loads(p.read_text(encoding='utf-8'))

def save(p,d):
    p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def run(a,cwd=None):
    subprocess.run(['ffmpeg','-y','-v','error',*a],check=True,cwd=cwd)

def probe(p):
    return json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_streams','-of','json',str(p)]))['streams'][0]

codec=['-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709','-color_range','tv']
plan=read(OUT/'assembly-plan.json')
entries=plan['entries']
for name in ['clips','segments','fonts']:
    (OUT/name).mkdir(exist_ok=True)
effects={}
counts={'opening':68,'travel':42,'planet-push':46,'system-departure':173,'finale':235}
for name,count in counts.items():
    folder=OUT/(name+'-frames')
    assert len(list(folder.glob('frame_*.png')))==count,(name,count)
    video=OUT/(name+'-effect.mp4')
    run(['-framerate','24','-i',str(folder/'frame_%04d.png'),'-frames:v',str(count),*codec,str(video)])
    effects[name]=video

for e in entries:
    if not e.get('effect'):
        continue
    lead=e['effectSourceIn']
    count=e['frames']+(0 if e['shot']=='contact-032' else 8)
    dest=OUT/'clips'/(e['shot']+'.mp4')
    run(['-i',str(effects[e['effect']]),'-vf',f'trim=start_frame={lead}:end_frame={lead+count},setpts=N/(24*TB),setsar=1',
         '-frames:v',str(count),*codec,str(dest)])
    assert int(probe(dest)['nb_frames'])==count
    e['clip']=dest.relative_to(BASE).as_posix()
    e['compositor']=(OUT/(e['effect']+'.blend')).relative_to(BASE).as_posix()

segments=[]
for i,e in enumerate(entries):
    n=e.get('transition',{}).get('frames',0) if i else 0
    if n:
        prev=entries[i-1]
        if not e.get('effect') and not prev.get('effect'):
            fade=BASE/e['priorSegmentsRoot']/(e['shot']+'-dissolve.mp4')
            assert fade.exists()
        else:
            fade=OUT/'segments'/(e['shot']+'-dissolve.mp4')
            fc=(f"[0:v]trim=start_frame={prev['frames']}:end_frame={prev['frames']+n},setpts=N/(24*TB)[a];"
                f"[1:v]trim=start_frame=0:end_frame={n},setpts=N/(24*TB)[b];"
                f"[a][b]blend=all_expr='A*(1-(T*24+1)/{n+1})+B*((T*24+1)/{n+1})'[v]")
            run(['-i',str(BASE/prev['clip']),'-i',str(BASE/e['clip']),'-filter_complex',fc,'-map','[v]','-frames:v',str(n),*codec,str(fade)])
        assert int(probe(fade)['nb_frames'])==n
        segments.append(fade)
    if e.get('effect'):
        body=OUT/'segments'/(e['shot']+'-body.mp4')
        run(['-i',str(BASE/e['clip']),'-vf',f"trim=start_frame={n}:end_frame={e['frames']},setpts=N/(24*TB)",
             '-frames:v',str(e['frames']-n),*codec,str(body)])
    else:
        body=BASE/e['priorSegmentsRoot']/(e['shot']+'-body.mp4')
        assert body.exists(),body
    assert int(probe(body)['nb_frames'])==e['frames']-n
    segments.append(body)
    print('Assembled',e['shot'],'revised' if e.get('effect') else 'retained',flush=True)
(OUT/'concat.txt').write_text(''.join("file '"+p.as_posix()+"'\n" for p in segments),encoding='utf-8')
run(['-f','concat','-safe','0','-i',str(OUT/'concat.txt'),'-an','-c','copy',str(OUT/'motion-picture.mp4')])
assert int(probe(OUT/'motion-picture.mp4')['nb_frames'])==2122

data=read(BASE/'generated/animatic/animatic-data.json')
captions=copy.deepcopy(data)
captions['phrases']=[p for p in captions['phrases'] if 3144<=p['startFrame']<5266]
for phrase in captions['phrases']:
    for item in [phrase]+phrase['words']:
        item['startFrame']-=3143
        item['endFrameExclusive']-=3143
style=read(BASE/'project.json')['production']['lyricPresentation']
write_lyrics(captions,style,OUT/'lyrics.ass')
shutil.copy2(style['fontFile'],OUT/'fonts'/Path(style['fontFile']).name)
title='''[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
ScaledBorderAndShadow: yes
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Bahnschrift,68,&H00FFF3E4,&H00FFF3E4,&H00201610,&H80201610,0,0,0,0,100,100,3,0,1,1.5,2,8,50,50,50,1
Style: Credit,Bahnschrift,30,&H00FFF3E4,&H00FFF3E4,&H00201610,&H80201610,0,0,0,0,100,100,1,0,1,1,1,8,50,50,50,1
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:01:25.04,0:01:28.42,Title,,0,0,0,,{\\pos(960,850)\\fad(500,0)}A RIGHT LITTLE SOMETHING
Dialogue: 0,0:01:25.04,0:01:28.42,Credit,,0,0,0,,{\\pos(960,945)\\fad(500,0)}© 2026 Arne Gleason
'''
(OUT/'title.ass').write_text(title,encoding='utf-8')
source=BASE/'generated/animatic/A-Right-Little-Something-selected-motion-v64.mp4'
run(['-reinit_filter','0','-i','motion-picture.mp4','-i',str(source),'-filter_complex',
     '[0:v]ass=lyrics.ass:fontsdir=fonts,ass=title.ass:fontsdir=fonts[v];[1:a]atrim=start=130.958333333333:end=219.375,asetpts=PTS-STARTPTS[a]',
     '-map','[v]','-map','[a]','-frames:v','2122','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart','timed-still-board.mp4'],cwd=OUT)
assert int(probe(OUT/'timed-still-board.mp4')['nb_frames'])==2122

before=read(BASE/'shots/shotlist.json')
register=copy.deepcopy(before)
prior_shots={s['id']:copy.deepcopy(s) for s in before['storyboardProposals']}
for e in entries:
    s=next(s for s in register['storyboardProposals'] if s['id']==e['shot'])
    if not e.get('effect'):
        continue
    s['motionSelection']=dict(id=e['shot']+'-v65',motionRef=e['clip'],sourceEditStartFrame=1,editFrames=e['frames'],
                              compositor=e['compositor'],draftForReview=True,userSelected=False,status='V65 local revision for review')
    s['motionRef']=e['clip']
    if e['effect'] in ['opening','travel']:
        s['motionSelection']['layerStack']=['Warp background','Masked tint and refraction of background only','Unchanged ship and Harper foreground']
    if e['shot']=='contact-032':
        s['compositePlan'].update(portraitSourceStartFrame=73,portraitSourceAdvanceFrames=48,compositor=e['compositor'])
        s['compositePlan']['endTitle'].update(font='Bahnschrift',displayText='A RIGHT LITTLE SOMETHING',fontSize=68,tracking=3)
    if e['shot']=='contact-027':
        s['motionSelection']['departureLight']=dict(twinkleStartFrame=4550,twinklePeakFrame=4567,escapeStartFrame=4583,escapeEndFrame=4648)
spec=dict(id='first-contact-v01',output=OUT.relative_to(BASE).as_posix(),sourceAnimatic=source.relative_to(BASE).as_posix(),useMotion=True,
          shotIds=[e['shot'] for e in entries],motionShotIds=[e['shot'] for e in entries],draftForReview=True,
          mediaLabel='Sphere optics / departure light and refined ending',
          presentation='Stronger underlay-only sphere transmission in both plated warp shots; central-world departure twinkle and curved accelerating light; planet-side camera push; Harper portrait source advanced two seconds; clean sans-serif closing title.',
          continuationNotes='V65: local revisions only, no new credits. Foreground plates untouched; stronger middle-layer cyan optics affect background only. Departure light, rear-view planet push, advanced portrait and Bahnschrift end title. V64 timings, reversed Travel28 and 3:34–3:36 portrait fade preserved.')
save(OUT/'review-options.json',spec)
save(BASE/'shots/shotlist.json',register)
try:
    subprocess.run([sys.executable,str(ROOT/'tools/insert_still_storyboard.py'),str(BASE/'project.json'),str(OUT/'review-options.json'),'--version','v65'],check=True)
except BaseException:
    save(BASE/'shots/shotlist.json',before)
    raise
register=read(BASE/'shots/shotlist.json')
register['reviewEdits']['v65'].update(type='Local optical and ending refinements',newPaidCredits=0,preservedVersion='v64',reviewStatus='Pending user review',reviewNotes='outro-v64-review.json')
register['firstContactSequence'].update(animaticVersion='v65',status='V65 refinements assembled; review pending',reviewUrl='http://127.0.0.1:8768/?v=v65',motionReviewUrl='http://127.0.0.1:8768/storyboard/outro-polish-v02/')
for e in entries:
    s=next(s for s in register['storyboardProposals'] if s['id']==e['shot'])
    if e.get('effect'):
        s['animaticPlacement']['kind']='Blender local revision / '+e['effect']
        s['status']='V65 local revision review pending'
    else:
        s['animaticPlacement']['kind']=prior_shots[s['id']].get('animaticPlacement',{}).get('kind','Retained V64 motion')
        s['status']=prior_shots[s['id']]['status']
    for stored in register['reviewEdits']['v65']['entries']:
        if stored['shot']==e['shot']:
            stored.update(s['animaticPlacement'])
save(BASE/'shots/shotlist.json',register)
save(OUT/'assembly-plan.json',plan)
save(OUT/'verification.json',dict(fullFrames=5265,fps=24,width=1920,height=1080,sectionFrames=2122,newPaidCredits=0,
      unchangedTimeline=True,portraitSourceAdvanceFrames=48,portraitSourceStartFrame=73,harperFadeStartFrame=5137,harperFadeEndFrame=5185,
      titleFirstFrame=5185,titleFullyVisibleFrame=5197,titleFont='Bahnschrift',sphereForeground='Original keyed ship and Harper graph retained; optics modify background only',
      v64Preserved=source.exists(),audio='Original V64 AAC packets verified identical by insertion tool',reviewStatus='Pending user review'))
(OUT/'index.html').write_text('''<!doctype html><meta charset="utf-8"><title>V65 refinements</title><style>body{background:#10242a;color:#eee4d2;font:16px/1.5 system-ui;max-width:1100px;margin:30px auto;padding:0 24px}a{color:#9cdfea}video{width:100%}</style><h1>V65 · Sphere optics and ending</h1><p><a href="/?v=v65">Full animatic</a> · <a href="/?v=v64">V64 comparison</a></p><p>Darker underlay-only sphere optics, central-world departure light, planet-side push, advanced Harper portrait and sans-serif closing title. No new generation credits.</p><video controls src="timed-still-board.mp4"></video>''',encoding='utf-8')
print('V65 assembled: 5265 frames; original audio; no new credits.',flush=True)
