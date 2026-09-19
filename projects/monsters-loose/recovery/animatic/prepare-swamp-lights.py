from pathlib import Path
import subprocess,json,numpy as np
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913')
o=r/'motion-graphics/SWAMP-LIGHTS-001';o.mkdir(exist_ok=True)
src=r/'video-tests/KLING-SWAMP-FROG-002/Swamp-frog-snatch-v002.mp4'
a=np.frombuffer(subprocess.check_output(['ffmpeg','-v','error','-i',str(src),'-vf','scale=960:540','-f','rawvideo','-pix_fmt','rgb24','-']),np.uint8).reshape(-1,540,960,3)
tracks={}
for i,(x,y) in enumerate([(429,43),(330,113),(240,168),(492,167),(657,119),(783,106),(930,126)]):
 rows=[]
 for f in a:
  patch=f[y-7:y+8,x-7:x+8].astype(float);score=patch[:,:,0]-.7*patch[:,:,1]-.3*patch[:,:,2]
  yy,xx=np.unravel_index(score.argmax(),score.shape)
  bg=np.median(np.concatenate([patch[0],patch[-1],patch[:,0],patch[:,-1]]),axis=0)/255
  rows.append([int(x-7+xx),int(y-7+yy),bg.tolist()])
 tracks[str(i)]=rows
(o/'tracks.json').write_text(json.dumps(tracks))
base=(r/'motion-graphics/HELI-LIGHTS-001/build-v002.py').read_text()
patch=base[base.index('def patch('):base.index('def pulse(')]
head='''import bpy,json,math\nfrom pathlib import Path\no=Path(__file__).resolve().parent\ntracks=json.loads((o/'tracks.json').read_text())\nbpy.ops.wm.read_factory_settings(use_empty=True)\ns=bpy.context.scene;s.render.engine='BLENDER_EEVEE'\ns.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100\ns.render.fps=24;s.frame_start=1;s.frame_end=227\ns.render.film_transparent=True;s.view_settings.view_transform='Standard'\nbpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object\ns.camera.data.type='ORTHO';s.camera.data.ortho_scale=960;s.camera.data.clip_end=2000\n'''
tail='''
for i,rows in tracks.items():
 i=int(i)
 # Feathered dimming patch retains a faint red source, avoiding a black cutout.
 bg=rows[0][2]
 bg=[((v+.055)/1.055)**2.4 if v>.04045 else v/12.92 for v in bg]
 mute,ma=patch('Beacon %s original-light soft suppression'%i,bg)
 mute.scale=(7,7,1);ma.default_value=.94
 halo,ha=patch('Beacon %s bloom'%i,(1,.014,.002));halo.scale=(12,12,1)
 core,ca=patch('Beacon %s red lamp'%i,(1,.025,.004));core.scale=(3.2,3.2,1)
 hot,wa=patch('Beacon %s hot center'%i,(1,.35,.14));hot.scale=(1.5,1.5,1)
 for f,(x,y,bg) in enumerate(rows,1):
  master=f-1+1293
  # Smooth staggered 29-frame beacon cycle, matching opening aviation cadence.
  d=(master-7-i*4+14.5)%29-14.5
  p=math.exp(-.5*(d/3.4)**2)
  for z,ob in enumerate([mute,halo,core,hot]):
   ob.location=(x-480,270-y,1+z*.1);ob.keyframe_insert(data_path='location',frame=f)
  for a,v in [(ha,.9*p),(ca,.08+.92*p),(wa,.98*p)]:
   a.default_value=v;a.keyframe_insert(data_path='default_value',frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
folder=o/'overlay';folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(folder/'lights-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Swamp-lights-v001.blend'))
bpy.ops.render.render(animation=True)
'''
(o/'build.py').write_text(head+patch+tail)
(o/'timing.json').write_text(json.dumps({'fps':24,'source':str(src.relative_to(r)),'source_frames':227,'master_start_frame':1305,'master_end_frame_exclusive':1507,'source_in_frame':12,'assumed_pre_roll_frames':12,'assumed_post_roll_frames':12,'period_frames':29,'pulse_sigma_frames':3.4,'note':'Seven red facility beacons, staggered phase, feathered suppression plus Gaussian bloom. Windows and path lamps remain steady. Frog action unchanged.'},indent=2))
print('Prepared',len(a),'frames and',len(tracks),'tracked lamps')
