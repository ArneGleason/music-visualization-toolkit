from pathlib import Path
import json,sys,subprocess,hashlib
import numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(R/'out/fx_tracking_deps'))
import cv2
receipts=[]
for family,count,ref in [('receiver',51,'out/receiver_voice_review/fx/frames'),('specimen',106,'out/lipsync_followup_review_v1/frames')]:
    D=O/family;qa=[]
    for f in range(1,count+1):
        a=cv2.imread(str(D/f'native_1280/{f:04d}.png'));b=cv2.imread(str(R/ref/f'{f-1:04d}.png'))
        assert a is not None and b is not None
        delta=np.abs(a.astype(float)-b.astype(float));row={'source_frame':f-1,'mae':float(delta.mean()),'p99':float(np.percentile(delta,99))}
        hi=D/f'native_1920/{f:04d}.png'
        if hi.exists():
            h=cv2.resize(cv2.imread(str(hi)),(1280,720),interpolation=cv2.INTER_AREA)
            row['resolution_mae']=float(np.abs(h.astype(float)-a.astype(float)).mean())
        qa.append(row)
    (D/'qa.json').write_text(json.dumps(qa,indent=2))
    clean=D/'native_clean.mp4'
    subprocess.run(['ffmpeg','-v','error','-n','-framerate','24','-start_number','1','-i',str(D/'native_1280/%04d.png'),'-frames:v',str(count),'-an','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)],check=True)
    subprocess.run(['ffmpeg','-v','error','-i',str(clean),'-f','null','-'],check=True)
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=nb_frames,r_frame_rate','-of','json',str(clean)]))['streams'][0]
    assert int(info['nb_frames'])==count and info['r_frame_rate']=='24/1'
    receipts.append({'family':family,'status':'native_rendered_owner_review_pending','frames':count,'clean':str(clean.relative_to(R)),'sha256':hashlib.sha256(clean.read_bytes()).hexdigest(),'max_frame_mae':max(q['mae'] for q in qa),'recipe':'out/blender_migration_v1/lights2_native.py','resolution_samples':sum('resolution_mae' in q for q in qa)})
(O/'lights2_receipts.json').write_text(json.dumps(receipts,indent=2));print(json.dumps(receipts,indent=2))
snapshot=json.loads((O/'preview_shotlist.json').read_text())
for s in snapshot['shots']:
    if s['id']=='s010':s['clip']={'file':'out/blender_migration_v1/receiver/native_clean.mp4','in_sec':0,'speed':1}
    if s['id']=='exchange_listener_audition':s['clip']={'file':'out/blender_migration_v1/specimen/native_clean.mp4','in_sec':0,'speed':1}
(O/'lights2_shotlist.json').write_text(json.dumps(snapshot,indent=2))
decisions=json.loads((R/'out/receiver_voice_review/receiver_decision.json').read_text())
decisions['s010']['delivery_file']='out/blender_migration_v1/receiver/native_clean.mp4'
decisions['s010']['notes']='Isolated native-migration review. Original treatment approved; new render awaits contextual owner review. Not a production register update.'
(O/'lights2_receiver_decision.json').write_text(json.dumps(decisions,indent=2))
