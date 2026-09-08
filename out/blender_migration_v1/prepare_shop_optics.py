"""Extract untreated, timestamp-conformed plates for an isolated optical proof."""
import hashlib,json,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent; R=O.parents[1]; D=O/'shop_optics'
D.mkdir(exist_ok=True)
sources={'wide':'out/shop_wide_synced_v5/wide_cfr.mp4',
         'close':'out/shop_performance_v1/close/base.mp4'}
records=[]
for name,file in sources.items():
    dest=D/name;dest.mkdir(exist_ok=True)
    # Keep all source frames and choose the shot's inpoint in Blender.
    if not (dest/'0001.png').exists():
        subprocess.run(['ffmpeg','-v','error','-n','-i',str(R/file),str(dest/'%04d.png')],check=True)
    records.append({'name':name,'file':file,'sha256':hashlib.sha256((R/file).read_bytes()).hexdigest(),
                    'frames':len(list(dest.glob('*.png')))})
(D/'inputs.json').write_text(json.dumps({'status':'optical_technique_proof_only',
 'sources':records,'song_frames':[2399,2484],'wide_origin':2387,'close_origin':2425,
 'switch':2431,'approved_signal_included':False},indent=2))
