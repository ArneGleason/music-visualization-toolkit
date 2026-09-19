import json, subprocess
from pathlib import Path

o=Path(__file__).resolve().parent
r=o.parent.parent
def run(args):
    subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)

patrol=r/'video-tests/KLING-PATROL-001/KLING-PATROL-001-01.mp4'
reaction=o/'Harper-reaction-announcement-v002.mp4'
pa=o/'Arctic-PA-v001.mp4'
inputs=[]
for p in (patrol,pa,reaction,r/'master.wav'):
    inputs+=['-i',str(p)]
graph=(
    '[0:v]trim=start_frame=12:end_frame=151,setpts=PTS-STARTPTS,scale=1280:720,setsar=1[a];'
    '[1:v]trim=start_frame=0:end_frame=108,setpts=PTS-STARTPTS,setsar=1[b];'
    '[2:v]trim=start_frame=12:end_frame=171,setpts=PTS-STARTPTS,setsar=1[c];'
    '[a][b][c]concat=n=3:v=1:a=0[v];'
    '[3:a]atrim=start_sample=1252000:end_sample=2064000,asetpts=PTS-STARTPTS[audio]'
)
# Master WAV sample rate is queried; frame-derived boundaries remain authoritative.
info=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=sample_rate','-of','json',str(r/'master.wav')]))
sr=int(info['streams'][0]['sample_rate'])
graph=graph.replace('1252000',str(round(626*sr/24))).replace('2064000',str(round(1032*sr/24)))
run([*inputs,'-filter_complex',graph,'-map','[v]','-map','[audio]','-c:v','libx264','-crf','17','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','320k','-movflags','+faststart',str(o/'Arctic-patrol-announcement-reaction-v002.mp4')])

for name,end in [('KLING-PATROL-001',151),('KLING-REACTION-002',171)]:
    p=r/'video-tests'/name/'timing.json'
    d=json.loads(p.read_text())
    media=r/'video-tests'/name/(name+'-01.mp4')
    probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=nb_frames,r_frame_rate,width,height','-of','json',str(media)]))
    d.update(actual_source_in_frame=12,actual_source_out_frame_exclusive=end,probe=probe)
    d['actual_available_post_roll_frames']=int(probe['streams'][0]['nb_frames'])-end
    p.write_text(json.dumps(d,indent=2)+'\n')

p=r/'shots/shotlist.json'
d=json.loads(p.read_text())
new=[
    dict(id='HARPER-ROPE-PATROL',start_frame=627,end_frame_exclusive=766,source=str(patrol.relative_to(r)).replace('\\','/'),source_in_frame=12,assumed_pre_roll_frames=12,status='generated_for_review',timing_record='video-tests/KLING-PATROL-001/timing.json'),
    dict(id='PA-ANNOUNCEMENT-CLOSEUP',start_frame=766,end_frame_exclusive=874,source=str(pa.relative_to(r)).replace('\\','/'),source_in_frame=0,assumed_pre_roll_frames=0,status='motion_effect_for_review',timing_record='motion-graphics/ARCTIC-PA-001/timing.json'),
    dict(id='HARPER-ARCTIC-REACTION',start_frame=874,end_frame_exclusive=1033,source=str(reaction.relative_to(r)).replace('\\','/'),source_in_frame=12,assumed_pre_roll_frames=12,status='generated_with_announcement_for_review',timing_record='video-tests/KLING-REACTION-002/timing.json')
]
ids={v['id'] for v in new}
d['shots']=[v for v in d['shots'] if v['id'] not in ids]+new
for c in d['generation_candidates']:
    if c['id'] in ids:
        c['status']='generated_for_review'
        c['video_source']=next(v['source'] for v in new if v['id']==c['id'])
d['scope']='Opening through Arctic patrol, interrupted PA and Harper reaction; new Arctic sequence awaiting review'
d['planned_scene3_revision']['preview']='motion-graphics/ARCTIC-PA-001/Arctic-patrol-announcement-reaction-v002.mp4'
p.write_text(json.dumps(d,indent=2)+'\n')
(o/'timing.json').write_text(json.dumps({
    'fps':24,'frame_convention':'Master one-based, end exclusive; source zero-based',
    'master_start_frame':766,'master_end_frame_exclusive':874,
    'timing_basis':'DAWproject animatic-data.json: bar17 beat2 to bar19 beat1, rounded to24fps',
    'assumed_pre_roll_frames':0,'assumed_post_roll_frames':0,
    'handle_note':'Procedural Blender shot rendered exactly to edit; can extend freely without paid regeneration.',
    'pa_bubble_ranges_one_based':[[6,36],[42,71],[77,108]],
    'reaction_overlay_source_ranges_one_based':[[1,51],[66,88]],
    'reaction_source_in_frame':12,
    'audio':'Original master music only; announcement represented visually, no added synthesized speech',
    'credits':{'patrol':56,'reaction':64,'total':184,'reaction_retry':64}
},indent=2)+'\n')
print('Composed review sequence; source timing and shotlist updated.')
