from pathlib import Path
import json
r=Path('C:/audio/shared/amtw-runtime/jobs/monsters-loose-word-timing-20260913')
p=r/'animatic/build-opening-v28.py'
s=p.read_text().replace("MonstersLoose-v27-through-habitats.blend","MonstersLoose-v28-through-habitats.blend").replace("v28 swamp bridge","v29 swamp beacon lights").replace("MonstersLoose-v28-opening-through-habitats.mp4","MonstersLoose-v29-opening-through-habitats.mp4").replace("save_as_mainfile(filepath=str(o/'MonstersLoose-v28-through-habitats.blend'","save_as_mainfile(filepath=str(o/'MonstersLoose-v29-through-habitats.blend'")
(r/'animatic/build-opening-v29.py').write_text(s)
(r/'motion-graphics/SWAMP-LIGHTS-001/README.md').write_text('''# Swamp facility beacon lights v001
Seven tracked red warning lamps receive feathered suppression of their existing steady light and red glow overlays rendered in Blender. Gaussian pulses have a 29-frame period and 3.4-frame width, staggered by four frames across lamps, matching the opening beacon cadence. Warm architectural lights stay steady. No generation or credits.

Input: video-tests/KLING-SWAMP-FROG-002/Swamp-frog-snatch-v002.mp4 (227 frames). Output: Swamp-frog-lights-v001.mp4. Trim source 12..214 exclusive to master 1305..1507 exclusive, 24fps. Assumed handles 12 frames each; edit unchanged.

Run animatic/prepare-swamp-lights.py to regenerate tracking and build script; run Blender in background with --python motion-graphics/SWAMP-LIGHTS-001/build.py; composite overlay/lights-%04d.png at 24fps over the source with FFmpeg overlay=0:0:format=auto, libx264 crf18 yuv420p. Run animatic/build-opening-v29.py after restoring predecessor project/media.

The underlying frog snatch take002 is user approved. This light polish awaits review. Original footage and v28 remain available.
''')
p=r/'shots/shotlist.json';d=json.loads(p.read_text())
sh=next(x for x in d['shots'] if x['id']=='SWAMP-FROG-001')
sh['original_video_source']=sh['source'];sh['source']='motion-graphics/SWAMP-LIGHTS-001/Swamp-frog-lights-v001.mp4';sh['status']='lighting_polish_for_review';sh['approval_note']='User approved snatch take002; requested gradual facility warning-light flashes without regeneration.';sh['lighting_timing_record']='motion-graphics/SWAMP-LIGHTS-001/timing.json'
p.write_text(json.dumps(d,indent=2)+'\n')
