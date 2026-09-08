"""Static spring concept on phrase, preserving underwater footage for following line."""
from pathlib import Path
import copy,json,subprocess
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
def run(args,**kw):subprocess.run([str(x) for x in args],cwd=ROOT,check=True,**kw)
run(['ffmpeg','-v','error','-y','-loop','1','-framerate','24','-i',OUT/'first_frame.png','-vf','scale=1280:720:force_original_aspect_ratio=increase,crop=1280:720,setsar=1','-frames:v','78','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',OUT/'still.mp4'])
edl=json.loads((ROOT/'out/opening_aerial_glimmer_v1/assembly_shotlist.json').read_text())
cues=json.loads((ROOT/'out/opening_aerial_glimmer_v1/overlay_cues.json').read_text())
fountain=next(s for s in edl['shots'] if s['id']=='s048')
under=next(s for s in edl['shots'] if s['id']=='s049')
newshots=[]; newcues=[]
for template,ident,start,end in [(fountain,'s048',3710,3752),(fountain,'spring_falls_heaven',3752,3830),(under,'underwater_senses',3830,3897)]:
    s=copy.deepcopy(template);s.update(id=ident,start_sec=start/24,end_sec=end/24,dur_sec=(end-start)/24,frames=end-start)
    cue=copy.deepcopy(next(c for c in cues['shots'] if c['id']==template['id']));cue.update(id=ident,start=start,end=end)
    if ident=='spring_falls_heaven':
        s['setup']='spring_splash_new';s['clip']={'file':'out/springs_splash_review_v1/still.mp4','in_sec':0,'speed':1}
        s['lyric']='Whatever falls from heaven';s['description']='STATIC CONCEPT: natural geothermal spray falling into familiar spring pool'
    if ident=='underwater_senses':
        s['clip']['in_sec']=0;s['lyric']='leaves the senses behind.'
        s['description']='Preserved underwater footage moved onto following phrase, no retime or repeat'
    newshots.append(s);newcues.append(cue)
edl['shots']=[s for s in edl['shots'] if round(s['start_sec']*24)<3710]+newshots
cues['shots']=[c for c in cues['shots'] if c['start']<3710]+newcues
for name,data in [('shotlist.json',edl),('overlay_cues.json',cues)]: (OUT/name).write_text(json.dumps(data,indent=2))
adapter=(ROOT/'out/probe_voice_trial/blender_review.py').read_text().replace('"probe_voice_trial"','"springs_splash_review_v1"')
(OUT/'blender_review.py').write_text(adapter)
with (OUT/'render.log').open('w') as log:
    run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','--python-exit-code','1','-P',OUT/'blender_review.py','--','--proxy','--start','3505','--end','3896','--shotlist',OUT/'shotlist.json','--lyric-flat','shots/lyric_motion_full.json','--out',OUT/'raw.mp4'],stdout=log,stderr=subprocess.STDOUT)
run(['ffmpeg','-v','error','-y','-i',OUT/'raw.mp4','-i',ROOT/'audio/song.wav','-filter_complex',f'[1:a]atrim=start={3505/24}:end={3897/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','392','-c:v','copy','-c:a','aac','-b:a','256k','-movflags','+faststart',OUT/'preview.mp4'])
run(['ffmpeg','-v','error','-i',OUT/'preview.mp4','-f','null','-'])
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(OUT/'preview.mp4')]))['streams'][0]
assert int(info['nb_frames'])==392 and info['r_frame_rate']=='24/1'
(OUT/'verification.json').write_text(json.dumps({'preview_song_frames':[3505,3897],'spring_static_song_frames':[3752,3830],'spring_frames':78,'underwater_song_frames':[3830,3897],'underwater_source_frames':[0,67],'status':'concept and timing review pending','spring_motion':'none, still only','new_Flow_submissions':0},indent=2))
