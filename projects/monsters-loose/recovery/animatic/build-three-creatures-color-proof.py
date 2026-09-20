from pathlib import Path
import subprocess
r=Path(__file__).resolve().parent.parent
cmd=['ffmpeg','-y','-v','error']
for name in ['aviary','insectarium','exobiology']:cmd+=['-loop','1','-framerate','24','-i',str(r/f'assets/SCN-007-{name}-v003.png')]
cmd+=['-ss',str(2091/24),'-i',str(r/'master.wav')]
filters=[]
for i in range(3):filters.append(f'[{i}:v]scale=1280:720,setsar=1,trim=end_frame=26,setpts=PTS-STARTPTS[v{i}]')
filters.append('[v0][v1][v2]concat=n=3:v=1:a=0[v]')
cmd+=['-filter_complex',';'.join(filters),'-map','[v]','-map','3:a','-t','3.25','-r','24','-c:v','libx264','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-movflags','+faststart',str(r/'animatic/Three-creatures-color-proof-v003.mp4')]
subprocess.run(cmd,check=True)
