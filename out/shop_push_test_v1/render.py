"""Verify returned plates and audition a twelve-frame local push, before lip sync."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'out/fx_tracking_deps'))
import cv2
handoff=json.loads((ROOT/'out/shop_performance_v1/handoff.json').read_text(encoding='utf-8'))
plates={};checks=[]
for take in handoff['takes']:
    p=ROOT/take['base'];r=take['claude_result']
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    assert digest==r['sha256']
    assert hashlib.sha256((ROOT/r['original']).read_bytes()).hexdigest()==digest
    info=json.loads(subprocess.check_output(['ffprobe','-v','error','-select_streams','v:0','-show_entries','stream=r_frame_rate,nb_frames,width,height,start_time','-of','json',str(p)]))['streams'][0]
    assert info['r_frame_rate']=='24/1' and int(info['nb_frames'])==192
    cap=cv2.VideoCapture(str(p));frames=[]
    while True:
        ok,f=cap.read()
        if not ok:break
        frames.append(f)
    cap.release();assert len(frames)==192
    plates[take['id']]=frames
    checks.append({'id':take['id'],'sha256':digest,'probe':info,'decoded_frames':len(frames)})
(OUT/'frames').mkdir(exist_ok=True)
y,x=np.mgrid[:720,:1280].astype(np.float32)
def smooth(t):
    t=np.clip(t,0,1);return t*t*(3-2*t)
for sf in range(2399,2484):
    if sf>=2437:
        frame=plates['close'][sf-2425]
    else:
        wide=plates['wide'][sf-2387]
        samples=[]
        for dt in np.linspace(-.4,.4,5):
            a=smooth((sf+dt-2425)/11)
            # Exact original reference crop converted from1536 to1280 pixels.
            left=520*a;top=(64/1.2)*a
            width=1280+(800/1.2-1280)*a
            height=720+(450/1.2-720)*a
            samples.append(cv2.remap(wide,(left+x*width/1280).astype(np.float32),(top+y*height/720).astype(np.float32),cv2.INTER_LINEAR))
        frame=np.mean(samples,axis=0)
        # Brief matched-framing dissolve; the mouth mismatch is not lip-synced yet.
        blend=smooth((sf-2433)/3)
        if blend>0:frame=frame*(1-blend)+plates['close'][sf-2425]*blend
        frame=np.clip(frame,0,255).astype(np.uint8)
    cv2.imwrite(str(OUT/'frames'/f'{sf-2399:04d}.png'),frame)
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(OUT/'frames/%04d.png'),'-frames:v','85','-an','-c:v','libx264','-crf','16','-pix_fmt','yuv420p',str(OUT/'clean.mp4')],check=True)
# Reuse the established contextual assembly, replacing only its shop plate.
p=ROOT/'out/shop_reply_review_v1/render.py'
s=p.read_text().replace('clips/raw/counterfeit_parade_v6.mp4','out/shop_push_test_v1/clean.mp4')
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py')})
(OUT/'verification.json').write_text(json.dumps({'status':'verified_candidates_owner_review_pending','checks':checks,
 'preview_song_frames':[2330,2484],'shop_song_frames':[2399,2484],
 'wide_origin_frame':2387,'close_origin_frame':2425,'close_lyric_source_frames':[12,59],
 'push_song_frames':[2425,2437],'close_blend_song_frames':[2434,2437],
 'lip_sync_applied':False,'production_merged':False},indent=2))
