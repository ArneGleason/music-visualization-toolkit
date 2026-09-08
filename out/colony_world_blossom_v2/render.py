"""More dimensional independent signals and a three-turn accelerating spin."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
ns={};exec(compile((OUT/'shape.py').read_text(),'shape.py','exec'),ns)
p=ROOT/'out/colony_world_blossom_v1/render.py';s=p.read_text().replace('colony_world_blossom_v1','colony_world_blossom_v2')
marker='norm=max(float(np.quantile(np.abs(audio),.94)),.001)'
s=s.replace(marker,marker+'''
guitar_stem=next(Path(local['sources']['stems']).glob('*Guitar*restored.wav'))
guitar_audio=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(guitar_stem),'-af',
    f'atrim=start={2265/24-.178348}:duration=7,asetpts=PTS-STARTPTS,highpass=f=80,lowpass=f=1500',
    '-ac','1','-ar','8000','-f','f32le','-']),dtype=np.float32)
guitar_norm=max(float(np.quantile(np.abs(guitar_audio),.94)),.001)
guitar_level=0.;guitar_radial=np.zeros(512)
''')
start=s.index('    light=np.zeros((720,1280,3)')
end=s.index('    pic=f.astype',start)
s=s[:start]+'''    guitar_chunk=guitar_audio[center-128:center+128]
    guitar_level=max(min(1,float(np.sqrt(np.mean(guitar_chunk**2)))/guitar_norm*2),guitar_level*.70)
    guitar_wave=np.interp(np.linspace(0,len(guitar_chunk)-1,512),np.arange(len(guitar_chunk)),guitar_chunk)/guitar_norm
    guitar_radial=.5*guitar_radial+.5*np.tanh(np.abs(guitar_wave)*1.7)
    light=draw(cv2,sf,angle,radial,level,guitar_radial,guitar_level,trail)
    formation=smooth((sf-2330)/34)
    spin=6*np.pi*smooth((sf-2366)/33)
'''+s[end:]
s=s.replace("'vocal_level':level,", "'vocal_level':level,'guitar_level':guitar_level,")
exec(compile(s,str(p),'exec'),{'__name__':'__main__','__file__':str(OUT/'render.py'),'draw':ns['draw']})
r=json.loads((OUT/'recipe.json').read_text())
r.update(method='Independent cyan vocal and amber guitar deformation in radius and out-of-plane depth; counter-phase breathing, stronger bloom. Three revolutions with smooth acceleration/deceleration on spin..around, six temporal samples over .84frame shutter; reduced persistence while spinning and sparse departing sparks.',
         drivers={'cyan':'restored lead vocal','amber':'restored guitar'},spin=[2366,2399],spin_turns=3,
         temporal_samples_fast=6,shutter_frames=.84,status='owner_review_pending')
(OUT/'recipe.json').write_text(json.dumps(r,indent=2))
