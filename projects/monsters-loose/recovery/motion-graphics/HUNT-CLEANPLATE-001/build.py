from pathlib import Path
from PIL import Image,ImageDraw,ImageFilter
import subprocess,json
o=Path(__file__).resolve().parent;r=o.parents[1]
plate=Image.open(o/'plate.png').convert('RGBA');mask=Image.new('L',plate.size);ImageDraw.Draw(mask).rectangle((340,652,480,830),fill=255);mask=mask.filter(ImageFilter.GaussianBlur(12));plate.putalpha(mask);plate.save(o/'patch.png')
for name,src,count,enable in [('search',r/'motion-graphics/HUNT-PULLBACK-001/Hunt-pullback-v001.mp4',112,",enable='gte(n,107)'"),('lurch',r/'video-tests/KLING-HUNT-B-001/KLING-HUNT-B-001-01.mp4',84,'')]:
 filt='[0:v]'+('trim=start_frame=12:end_frame=96,setpts=PTS-STARTPTS,' if name=='lurch' else '')+'format=rgba[base];[base][1:v]overlay=0:0'+enable.replace(',enable',':enable')+',format=yuv420p[out]'
 subprocess.run(['ffmpeg','-y','-v','error','-i',str(src),'-loop','1','-i',str(o/'patch.png'),'-filter_complex',filt,'-map','[out]','-frames:v',str(count),'-r','24','-an','-c:v','libx264','-crf','17',str(o/(name+'-clean-v001.mp4'))],check=True)
(o/'timing.json').write_text(json.dumps({'plate_source':'KLING-HUNT-A-001 source frame110','mask_core_pixels':[340,652,480,830],'feather_sigma':12,'search_patch_from_master':2277,'lurch_source_in':12,'lurch_source_out_exclusive':96},indent=2))
