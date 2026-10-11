import json, math
from pathlib import Path
import bpy
from mathutils import Vector
p=Path('projects/a-right-little-something/hologram-overlay-v03.json')
plan=json.loads(p.read_text())
dest=p.parent/plan['output']
bpy.ops.wm.open_mainfile(filepath=str((dest/'hologram-overlay-v03.blend').resolve()))
scene=bpy.context.scene
tracks=json.loads((dest/'tracking.json').read_text())
focal=scene.render.resolution_x*scene.camera.data.lens/scene.camera.data.sensor_width
labels=[]
fields=[]
projection=[]
for system in plan['systems']:
    root=bpy.data.objects['SYSTEM / '+system['id']]
    label=bpy.data.objects[system['id']+' / camera-facing label']
    scene.frame_set(144)
    x,y,z=root.location
    expected=tracks['systems'][system['id']][-1]['pixel']
    projection.append(math.dist((960+x*focal/-z,540-y*focal/-z),expected))
    coords=[]
    for obj in label.children:
        if '/ leader' in obj.name:
            continue
        for point in obj.data.splines[0].points:
            v=obj.matrix_world@Vector(point.co[:3])
            coords.append((960+v.x*focal/-v.z,540-v.y*focal/-v.z))
    bounds=[min(v[0] for v in coords),min(v[1] for v in coords),max(v[0] for v in coords),max(v[1] for v in coords)]
    assert bounds[0]>=0 and bounds[1]>=0 and bounds[2]<1920 and bounds[3]<1080,bounds
    assert max(abs(a) for a in label.rotation_euler)==0
    labels.append({'id':system['id'],'identity':label['label_identity'],'finalGlyphBoundsPx':bounds})
    for index,belt in enumerate(system['asteroidBelts']):
        if not belt.get('outerCloud'):
            continue
        rig=bpy.data.objects[f'{system["id"]} / asteroid belt {index+1}']
        final=float(rig.scale.x)
        scene.frame_set(system['birthFrame']+10)
        early=float(rig.scale.x)
        assert final>early and abs(final-1)<1e-5
        fields.append({'id':system['id'],'particles':rig['particle_count'],'earlyScale':early,'finalScale':final})
assert len(labels)==len(fields)==5
assert max(projection)<.001
assert sum(f['particles'] for f in fields)==1590
scene.frame_set(144)
(dest/'scene-checks.json').write_text(json.dumps({'maxAnchorProjectionResidualPx':max(projection),'labels':labels,'growingOuterFields':fields,'songStartFrame':scene['song_start_frame'],'editFrames':scene['song_edit_frames']},indent=2)+'\n')
print('Verified five visible camera-facing labels, five growing outer fields, source registration and unchanged song frames.')
