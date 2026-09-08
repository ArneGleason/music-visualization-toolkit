"""Check original optical framing and high-resolution behavior, encode proof."""
import sys,json,subprocess,numpy as np
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'shop_optics'
sys.path.insert(0,str(R/'out/fx_tracking_deps'));import cv2
old=cv2.VideoCapture(str(R/'out/shop_wide_synced_v5/picture.mp4'));errors=[];res=[];tiles=[]
for i in range(85):
    ok,ref=old.read();assert ok
    new=cv2.imread(str(D/'native_1280'/f'{i+1:04d}.png'));assert new is not None
    errors.append(float(np.abs(ref.astype(float)-new).mean()))
    hipath=D/'native_1920'/f'{i+1:04d}.png'
    hi=cv2.imread(str(hipath)) if hipath.exists() else None
    if hi is not None:res.append({'frame':i+1,'mean_1080_downsample_difference':float(np.abs(cv2.resize(hi,(1280,720),interpolation=cv2.INTER_AREA).astype(float)-new).mean())})
    if i+1 in [1,26,29,31,32,33,34,38,60,85]:
        tile=cv2.resize(new,(384,216));cv2.putText(tile,f'29 / song {2399+i}',(10,22),cv2.FONT_HERSHEY_SIMPLEX,.5,(255,255,255),1,cv2.LINE_AA);tiles.append(tile)
old.release();cv2.imwrite(str(D/'contact.jpg'),np.vstack([np.hstack(tiles[i:i+5]) for i in [0,5]]))
subprocess.run(['ffmpeg','-v','error','-y','-framerate','24','-i',str(D/'native_1280/%04d.png'),'-i',str(R/'audio/song.wav'),'-filter_complex',f'[1:a]atrim=start={2399/24}:end={2484/24},asetpts=PTS-STARTPTS[a]','-map','0:v','-map','[a]','-frames:v','85','-c:v','libx264','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart',str(D/'preview_optics_only.mp4')],check=True)
subprocess.run(['ffmpeg','-v','error','-i',str(D/'preview_optics_only.mp4'),'-f','null','-'],check=True)
qa={'status':'optical_proof_not_full_shot_migration','frames':85,'fps':24,'song_frames':[2399,2484],
 'source_switch_frame':2431,'mean_reference_difference':float(np.mean(errors)),
 'max_reference_difference':max(errors),'resolution_checks':res,
 'limitations':['Approved decorative signal deliberately absent to isolate the transition.',
 'Native blur sampling and edge extension are not pixel-identical to original OpenCV.'],
 'production_promoted':False}
random_frame=D/'random/0033.png'
if random_frame.exists():
    delta=np.abs(cv2.imread(str(random_frame)).astype(float)-cv2.imread(str(D/'native_1280/0033.png')))
    qa['saved_scene_random_access_frame_33_max_pixel_error']=float(delta.max())
    assert delta.max()==0
(D/'qa.json').write_text(json.dumps(qa,indent=2));print(json.dumps(qa,indent=2))
