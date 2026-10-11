"""Assemble local Blender light-overlay A/B reviews at the registered shot frames."""
import argparse
import html
import json
from pathlib import Path
import shutil
import subprocess

from PIL import Image, ImageChops


def encode(sequence, output, fps, start, count, audio_frame, master):
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', str(fps),
        '-start_number', str(start), '-i', str(sequence), '-ss', str(audio_frame/fps),
        '-i', str(master), '-map', '0:v:0', '-map', '1:a:0',
        '-frames:v', str(count), '-t', str(count/fps), '-c:v', 'libx264',
        '-crf', '17', '-preset', 'fast', '-pix_fmt', 'yuv420p', '-c:a', 'aac',
        '-movflags', '+faststart', str(output)], check=True)
    check = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
        '-select_streams', 'v:0', '-count_frames', '-show_entries',
        'stream=width,height,r_frame_rate,nb_read_frames', '-of', 'json', str(output)]))['streams'][0]
    assert check == {'width':1920,'height':1080,'r_frame_rate':f'{fps}/1','nb_read_frames':str(count)}, check
    return check


def page(data,plan=None):
    # An A/B player, not a browser substitute for the Blender animation rig.
    plan=plan or {}
    version=plan.get('version','v01')
    data=dict(data)
    data['mediaRoots']={'previous':plan.get('previousReviewPath','')+'/rich'}
    previous=('<option value="previous">'+html.escape(plan.get('previousReviewLabel',
        'Previous · uniform cyan systems'))+'</option>') if plan.get('previousReviewPath') else ''
    description=plan.get('reviewDescription','Small oblique orbit planes grow around the departing star points. Three planetary lights run around each system; short brighter arcs sweep through their paths. The home system stays amber, the neighbors cyan.')
    selected=bool(plan.get('animaticSelection'))
    earlier_trim='Earlier source trim' if selected else 'Current song trim'
    later_trim='Selected animatic trim' if selected else 'Later trim test'
    timing_status=plan.get('animaticStatus','No speed change; animatic v07 still uses its accepted original take.')
    return '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hologram · Blender overlay v01</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#10151c;color:#e9edf3;font:15px system-ui}main{max-width:1420px;margin:auto;padding:20px 24px}h1{font-size:23px;margin:0 0 8px}p{line-height:1.5;color:#b7c6d5;margin:10px 0}a{color:#9cdbf0}.bar{display:flex;align-items:center;flex-wrap:wrap;gap:12px;margin:14px 0}button,select{font:inherit;padding:7px 10px;border:1px solid #44576b;border-radius:5px;background:#1b2733;color:#eef6ff}button:hover{border-color:#78bdd6}video{width:100%;display:block;aspect-ratio:16/9;background:#000}.stage{border:1px solid #384754;border-radius:5px;overflow:hidden}.transport{display:flex;gap:12px;align-items:center}.transport input{flex:1;min-width:160px}output{font-variant-numeric:tabular-nums;min-width:215px;color:#bfd5e5}.notes{display:grid;grid-template-columns:1fr 1fr;gap:24px;border-top:1px solid #354656;margin-top:16px;padding-top:10px}details img{width:100%}summary{cursor:pointer;padding:8px 0}h2{font-size:17px;margin:8px 0}@media(max-width:850px){.notes{grid-template-columns:1fr}.transport{flex-wrap:wrap}}
</style><main>
<h1>Local stars unfolding into planetary systems · v01</h1>
<p><a href="/">Animatic / listening notes</a> · <a href="BASETAKE">Accepted base take</a> · <a href="hologram-overlay-v01.blend" download>Editable Blender scene</a></p>
<div class="bar"><label>View <select id="variant" aria-label="Overlay version"><option value="rich">B · Brighter systems + foreground mask</option><option value="restrained">A · Restrained systems + foreground mask</option>PREVIOUS<option value="source">Original Kling take</option><option value="unmasked">Diagnostic · brighter, no mask</option><option value="light">Diagnostic · Blender light only</option></select></label>
<label>Range <select id="range" aria-label="Playback range"><option value="handles">Full take · 6 s with handles</option><option value="edit">EARLIERTRIM · 104 frames</option><option value="later">LATERTRIM · same 104 frames</option></select></label>
<button id="reveal">Play system reveal</button><button id="swap">Compare with original</button></div>
<div class="stage"><video id="video" controls playsinline preload="auto" poster="rich/frame_0125Image.png" src="rich-handles.mp4"></video></div>
<div class="bar transport"><button id="back" aria-label="Previous frame">← Frame</button><input id="scrub" type="range" min="1" max="144" value="1" step="1" aria-label="Source frame"><button id="forward" aria-label="Next frame">Frame →</button><output id="clock"></output></div>
<p>Space: play/pause · ←/→: one frame · Shift+←/→: half a second. A/B changes keep the same source frame. No retiming or new generated footage.</p>
<div class="notes"><section><h2>What to look for</h2><p>DESCRIPTION</p><p>The new light is added in Blender in linear space. The masked versions place overlapping rings behind Harper. Her existing acting, the cabin and the original display remain the source footage.</p></section>
<section><h2>Timing and limits</h2><p>The registered song shot is frames 633–736 at 24 fps. The earlier trim uses source frames 13–116; the six-second test retains 12 lead-in frames and 28 trailing frames. New star points arrive late, so that trim shows only the first systems unfolding. The later trim uses source frames 29–132 at the same song position, retains a half-second tail, and shows more of the reveal. TIMINGSTATUS</p><p>Point tracking is guided by source-image light cores. Depth and orbit tilt are inferred for composition; the foreground mask is an initial hand-authored silhouette. Watch the shoulder, hair and moving hand for edge mismatch.</p></section></div>
<details><summary>Tracking / foreground-mask reference</summary><img src="tracking-0144.png" alt="Measured star centers and the foreground silhouette holdout"><p>Pink marks only the new-light holdout. It does not alter or replace any pixels of Harper in the original video.</p></details>
</main><script>
const config=CONFIG;const video=document.querySelector('#video'),variant=document.querySelector('#variant'),range=document.querySelector('#range'),scrub=document.querySelector('#scrub'),clock=document.querySelector('#clock');let prior='rich',activeRange='handles';
const lead=()=>activeRange==='handles'?0:activeRange==='edit'?config.leadInFrames:config.laterLeadFrames;const count=()=>activeRange==='handles'?config.sourceFrames:config.editFrames;
function frame(){return Math.max(1,Math.min(config.sourceFrames,Math.round(video.currentTime*config.fps)+lead()+1))}
function update(){scrub.min=lead()+1;scrub.max=lead()+count();scrub.value=frame();const sourceOffset=activeRange==='handles'?config.leadInFrames:lead();clock.textContent=`Source ${frame()} · song ${config.songStartFrame+frame()-sourceOffset-1} · ${video.currentTime.toFixed(2)} s`}
function seek(n){video.pause();video.currentTime=Math.max(0,Math.min((count()-1)/config.fps,(n-lead()-1)/config.fps));update()}
function change(){const n=frame(),playing=!video.paused;video.pause();activeRange=range.value;video.src=`${config.mediaRoots[variant.value]||variant.value}-${range.value}.mp4`;video.onloadedmetadata=()=>{seek(n);if(playing)video.play().catch(()=>{});};video.load()}
variant.addEventListener('change',change);range.addEventListener('change',change);scrub.addEventListener('input',()=>seek(Number(scrub.value)));video.addEventListener('timeupdate',update);video.addEventListener('loadedmetadata',update);
document.querySelector('#back').onclick=()=>seek(frame()-1);document.querySelector('#forward').onclick=()=>seek(frame()+1);document.querySelector('#reveal').onclick=()=>{seek(86);video.play().catch(()=>{})};document.querySelector('#swap').onclick=()=>{if(variant.value==='source')variant.value=prior;else{prior=variant.value;variant.value='source'}change()};
document.addEventListener('keydown',e=>{if(e.repeat||/INPUT|TEXTAREA|SELECT/.test(e.target.tagName)||e.target.isContentEditable)return;if(e.code==='Space'&&e.target.tagName!=='VIDEO'){e.preventDefault();video.paused?video.play().catch(()=>{}):video.pause()}if(e.code==='ArrowLeft'||e.code==='ArrowRight'){e.preventDefault();seek(frame()+(e.code==='ArrowRight'?1:-1)*(e.shiftKey?12:1))}});update();
</script></html>'''.replace('v01',version).replace('BASETAKE',html.escape(plan.get('baseTakeReview','../kling-hologram-star-centered-v01/'),quote=True)).replace('CONFIG',json.dumps(data)).replace('PREVIOUS',previous).replace('DESCRIPTION',html.escape(description)).replace('EARLIERTRIM',earlier_trim).replace('LATERTRIM',later_trim).replace('TIMINGSTATUS',html.escape(timing_status))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan',type=Path)
    args=parser.parse_args()
    project=args.plan.resolve().parent
    plan=json.loads(args.plan.read_text())
    dest=project/plan['output']
    data=json.loads((dest/'tracking.json').read_text())
    # Latest legal source trim with the same shot length and a 12-frame tail.
    data['laterLeadFrames']=data['sourceFrames']-12-data['editFrames']
    master=project/'generated/animatic/A-Right-Little-Something-lyric-timing-v03.mp4'
    checks=[]
    for variant in ('source','restrained','rich','unmasked','light'):
        folder=dest/variant
        folder.mkdir(exist_ok=True)
        for frame in range(1,plan['sourceFrames']+1):
            if variant=='source':
                continue
            path=folder/f'frame_{frame:04d}Image.png'
            if frame < plan['renderStartFrame']:
                if variant=='light':
                    Image.new('RGB',(plan['width'],plan['height'])).save(path)
                else:
                    shutil.copy2(dest/'source'/f'frame_{frame:04d}.png',path)
            assert path.exists(),f'Missing Blender frame {path}'
        for mode,start,count,song in (
            ('handles',1,data['sourceFrames'],data['songStartFrame']-1-data['leadInFrames']),
            ('edit',data['leadInFrames']+1,data['editFrames'],data['songStartFrame']-1),
            ('later',data['laterLeadFrames']+1,data['editFrames'],data['songStartFrame']-1)):
            pattern='frame_%04d.png' if variant=='source' else 'frame_%04dImage.png'
            result=encode(folder/pattern,dest/f'{variant}-{mode}.mp4',data['fps'],start,count,song,master)
            checks.append({'variant':variant,'mode':mode,**result})
    masked=Image.open(dest/'rich/frame_0144Image.png')
    unmasked=Image.open(dest/'unmasked/frame_0144Image.png')
    assert ImageChops.difference(masked,unmasked).getbbox(),'Foreground holdout did not change the composite'
    (dest/'review-checks.json').write_text(json.dumps(checks,indent=2)+'\n')
    (dest/'index.html').write_text(page({k:data[k] for k in ('fps','songStartFrame','editFrames','leadInFrames','sourceFrames','laterLeadFrames')},plan),encoding='utf-8')
    print(dest/'index.html')


if __name__=='__main__':
    main()
