import json, subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
out = root / 'KLING-KEEPER-001'
out.mkdir(exist_ok=True)
receipt = out / 'submission.json'
if receipt.exists():
    raise SystemExit('Existing receipt; do not resubmit.')
prompt = '''One continuous five-second shot introducing Harper, the red-haired freckled zookeeper in the supplied image. Preserve her identity, curly bob, olive uniform, gloves, badge and natural proportions. Preserve the illustrated graphic-novel style, bold ink outlines, crosshatching, restrained halftone, cool teal moonlight and warm amber lamps throughout.
Very gentle steady camera push toward Harper, maintaining the same viewing direction and leaving the enclosure number 2 and nighttime compound readable. First half-second: relaxed breathing and a natural blink, her gloved hand resting steadily on the gate. Over the next three seconds, she makes a small, natural head turn and eye movement toward the visitors approaching from offscreen right, then gives a subtle knowing closed-mouth smile. She looks competent, welcoming and quietly alert. Her body stays grounded; her hand remains in contact with the gate. The final second continues the same subtle breathing and camera drift, giving comfortable editing room; no final pose freeze or fade.
No singing, speech, lip-sync or exaggerated mouth movement. No broad gesture, walking, lasso, new people, visible monsters, opening or closing gate, scene transition, camera orbit or pullback. Preserve the rigid enclosure geometry, laboratory, moon, matte paving, signage and lighting. No morphing, new limbs, cartoon motion lines or photorealistic restyling. No audio.'''
(out/'prompt.txt').write_text(prompt,encoding='utf-8')
timing = {
    'clip_id':'KLING-KEEPER-001','scene':'SCN-002','status':'generation_planned',
    'edit_fps':24,'requested_duration_seconds':5,
    'assumed_pre_roll_frames':12,'assumed_pre_roll_seconds':0.5,
    'minimum_assumed_post_roll_frames':12,'minimum_assumed_post_roll_seconds':0.5,
    'planned_source_in_frame':12,'planned_source_out_frame_exclusive':97,
    'planned_remaining_tail_frames':23,
    'master_in_frame':207,'master_out_frame_exclusive':292,
    'master_frame_convention':'one-based, end exclusive',
    'source_frame_convention':'zero-based, end exclusive',
    'source_zero_master_frame':195,'source_zero_master_seconds':194/24,
    'actual_source_in_frame':None,'actual_source_out_frame_exclusive':None,
    'lip_sync':False,'audio_reference':None,
    'notes':'Flexible handle convention. Cut spans original animatic first keeper still. Actual source trims pending review; retain generation assumptions when editing.'
}
(out/'timing.json').write_text(json.dumps(timing,indent=2),encoding='utf-8')
args=['image_to_video','--image',str(root.parent/'assets'/'ANCH-002-v001.png'),'--model','kling-video-v3_0','--duration','5','--resolution','1080p','--imageCount','1','--enable_audio','false','--prefer_multi_shots','false',prompt]
(out/'request.json').write_text(json.dumps({'source':'assets/ANCH-002-v001.png','expected_credits_based_on_previous_test':40,'cli_args':args},indent=2),encoding='utf-8')
receipt.write_text('{"local_status":"submission_started"}',encoding='utf-8')
r=subprocess.run(['C:/Program Files/nodejs/node.exe','C:/Users/arneg/AppData/Roaming/npm/node_modules/@klingai/cli-global/dist/cli.js',*args],capture_output=True,text=True,encoding='utf-8')
receipt.write_text(r.stdout,encoding='utf-8')
(out/'submission-stderr.txt').write_text(r.stderr,encoding='utf-8')
print(r.stdout)
print('Exit:',r.returncode)
