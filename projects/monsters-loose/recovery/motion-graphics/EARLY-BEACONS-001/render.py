from pathlib import Path
import json,subprocess,concurrent.futures
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913');o=Path(__file__).resolve().parent

def render(sh):
 d=o/sh['id']
 with (d/'render.log').open('w') as log:subprocess.run(['C:/Program Files/Blender Foundation/Blender 5.2/blender.exe','-b','-t','4','--python',str(d/'build.py')],stdout=log,stderr=subprocess.STDOUT,check=True)
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(r/sh['input_source']),'-framerate','24','-i',str(d/'overlay/lights-%04d.png'),'-filter_complex','[0:v][1:v]overlay=0:0:format=auto','-an','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-frames:v',str(sh['frames']),str(r/sh['output_source'])],check=True)
 print('Rendered and composited',sh['id'],flush=True)
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(render,json.loads((o/'shots.json').read_text())))
