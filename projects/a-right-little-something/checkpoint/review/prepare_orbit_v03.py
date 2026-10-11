from pathlib import Path
import json, shutil

base=Path('projects/a-right-little-something').resolve()
def load(name): return json.loads((base/name).read_text(encoding='utf-8'))
def save(name,value): (base/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=load('orbit-blender-v02.json')
p.update(output='generated/storyboard/orbit-blender-v03',velocityModel='vis-viva-loops',samples=32,motionBlur=dict(shutterFrames=.65,keySamplesPerFrame=8,motionSteps=5),trailDecay=dict(brightFrames=2,tailFrames=12,tailWeight=.08,supportFrames=48),trailPowerScale=.25,sparkCount=48,sparkPower=2,sparkLifetimeFrames=26,headBeacon=dict(radius=.043,power=45))
for world,peri in zip(p['worlds'][1:],(330,340)):
    world.update(orbitEccentricity=.24,periapsisPhase=peri)
p['method']='Slightly eccentric authored loops. Vis-viva speed as a function of distance within each loop, with smooth authored approach/transfer timing and a global song time scale. Actual Cycles shutter blur, 8 transform key samples per frame and 16 motion intervals. Bright tracking core and rapid exponential wake falloff into a faint long tail. Not a full gravitational simulation.'
save('orbit-blender-v03.json',p)
s=load('revision-chorus-v04.json')
s.update(id='chorus-revision-v05',status='Orbit velocity, blur and trail revision in progress',output='generated/storyboard/chorus-revision-v05',sourceAnimatic='generated/animatic/A-Right-Little-Something-selected-motion-v24.mp4',orbitComposite='generated/storyboard/orbit-blender-v03/hybrid/orbit-composite-handles.mp4',nativeOrbitPlan='orbit-blender-v03.json',reviewTitle='Slingshot speed, motion blur and a fading comet wake',reviewIntro='The last orbit has distance-dependent speed on slightly eccentric looping passes, smooth connecting flight, native motion blur and a bright tracking core. Its short bright wake falls off quickly into a long faint tail. The illustrated world plate, fades, animated scale reveal and Ken Burns moves remain. This is an authored cinematic flight with Kepler-derived relative loop speeds, rather than a full gravity simulation.',continuationNotes='V25: last orbit uses distance-based vis-viva loop speeds, true Cycles shutter blur with subframe transform sampling, an emphasized bright ship core and rapid bright-to-faint exponential trail decay. Other v24 footage and fade language retained. Original phrase boundaries and master audio unchanged; no new paid generation.',cameraTrackNotes=p['method'],entryReviewNotes='Established v24 edit retained; final orbit speed, blur and trail balance revised.',reviewStatus='User-directed orbit velocity/blur/trail revision; playback review pending')
s['reviewLinks']=[dict(href='/storyboard/chorus-revision-v04/',title='Previous v24 review'),dict(href='/storyboard/orbit-blender-v03/hybrid/trajectory-study.png',title='Inspect the looping path and speed profile')]
s['entryOverrides']['orbit-pullback']=dict(reviewNotes=p['method'])
save('revision-chorus-v05.json',s)
out=base/s['output'];out.mkdir(parents=True,exist_ok=True)
r=load('shots/shotlist.json')
for entry in r['editProposals']['chorus-revision-v04']['entries']:
    if entry['id']!='orbit-pullback':
        shutil.copy2(base/'generated/storyboard/chorus-revision-v04'/(entry['id']+'.mp4'),out/(entry['id']+'.mp4'))
r['reviewEdits']['v24']['userReview']='User: all pretty good; last orbit pass fine, requests variable orbital speed, speed blur and faster bright trail falloff with a long faint tail.'
save('shots/shotlist.json',r)
print('Prepared new orbit and v25 recipes; nine approved shot chunks cached; current v24 preserved')
