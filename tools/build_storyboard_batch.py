"""Blender-native note storyboard scenes, camera keys, handles and review renders.

blender -b --python tools/build_storyboard_batch.py -- <project.json> <batch.json>
Add --motion to render small per-shot review movies including their handles.
"""
import json
import math
import pathlib
import sys

import bpy
from mathutils import Vector
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from shell_field import add_shell_field


def main():
    args = sys.argv[sys.argv.index('--')+1:]
    only = args[args.index('--shot')+1] if '--shot' in args else None
    project_file, batch_file = map(pathlib.Path, args[:2])
    base = project_file.resolve().parent
    project = json.loads(project_file.read_text(encoding='utf-8'))
    spec = json.loads(batch_file.read_text(encoding='utf-8'))
    register = json.loads((base/'shots/shotlist.json').read_text(encoding='utf-8'))
    key = 'storyboardProposals' if spec.get('proposal') else 'shots'
    shots = [s for s in register.get(key, []) if s.get('batch')==spec['id']]
    out = base/spec['output']; out.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.open_mainfile(filepath=str(base/spec['baseBlend']))
    template = bpy.context.scene
    source_collections = list(template.collection.children)
    scenes = []

    # Approved field appearance: clear everywhere, registered by a faint
    # spherical network. No reflective glass arc from either side.
    shell_material=bpy.data.materials['Clear shell / transparent centre, reflective rim'].copy()
    shell_material.name='Storyboard ultra-thin field / fully clear'
    nodes=shell_material.node_tree.nodes;links=shell_material.node_tree.links
    nodes.clear()
    output=nodes.new('ShaderNodeOutputMaterial')
    transparent=nodes.new('ShaderNodeBsdfTransparent')
    links.new(transparent.outputs[0],output.inputs['Surface'])
    shell_material['purpose']='Ultra-thin active field; no solid refractive glass volume'

    def lerp(a,b,t):
        return Vector(a).lerp(Vector(b),t)

    def proxy_piece(name, at, scale, parent, coll, mat):
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=at)
        obj=bpy.context.object;obj.name=name;obj.scale=scale;obj.parent=parent
        for c in list(obj.users_collection):c.objects.unlink(obj)
        coll.objects.link(obj);obj.data.materials.append(mat)
        for polygon in obj.data.polygons:polygon.use_smooth=True
        return obj

    def folded_figure(scene, objects):
        root=objects['FIGURE ROOT / floating pose']
        root.location=(0,-2.05,.1)
        coll=next(c for c in scene.collection.children if 'FIGURE' in c.name)
        for obj in coll.objects:
            if obj.type!='EMPTY':obj.hide_render=True
        mat=bpy.data.materials['Warm figure proxy']
        proxy_piece('Folded torso',(0,0,.55),(.23,.17,.36),root,coll,mat)
        proxy_piece('Folded head',(0,-.10,1.04),(.19,.17,.24),root,coll,mat)
        proxy_piece('Face toward planet below',(0,-.24,1.0),(.12,.035,.12),root,coll,bpy.data.materials['Face direction patch'])
        paths=[('Left arm',[(-.20,0,.76),(-.40,-.30,.64),(-.43,-.77,.62)]),
               ('Right arm',[(.20,0,.76),(.40,-.30,.64),(.43,-.77,.62)]),
               ('Left leg',[(-.12,0,.24),(-.28,-.38,.12),(-.24,-.08,-.48)]),
               ('Right leg',[(.12,0,.24),(.28,-.38,.12),(.24,-.08,-.48)])]
        for name,points in paths:
            for i,(a,b) in enumerate(zip(points,points[1:])):
                av,bv=Vector(a),Vector(b)
                obj=proxy_piece(name+str(i),(av+bv)/2,(.075,.075,(bv-av).length/2+.07),root,coll,mat)
                obj.rotation_euler=(bv-av).to_track_quat('Z','Y').to_euler()
        for x in (-.43,.43):
            proxy_piece('Palm on glass',(x,-.77,.62),(.12,.04,.13),root,coll,mat)

    for shot in shots:
        blocking=shot['blocking']; h=shot['handles'];total=h['generatedFrames']
        scene=template.copy();scene.name=shot['id']+' / '+shot['title']
        scene.use_fake_user=True
        for coll in list(scene.collection.children):scene.collection.children.unlink(coll)
        objects={}
        for source in source_collections:
            if 'REFERENCES' in source.name or 'CAMERAS' in source.name:continue
            coll=bpy.data.collections.new(shot['id']+' / '+source.name)
            scene.collection.children.link(coll)
            for original in source.objects:
                obj=original.copy();obj.animation_data_clear()
                if obj.type=='LIGHT':obj.data=original.data.copy()
                if original.name=='Clear spherical cabin':
                    obj.data=original.data.copy()
                    obj.data.materials.clear();obj.data.materials.append(shell_material)
                coll.objects.link(obj);objects[original.name]=obj
        for name,obj in objects.items():
            original=bpy.data.objects.get(name)
            if original.parent:obj.parent=objects.get(original.parent.name)
            if name.startswith(('Latitude','Meridian','Globe north pole')):obj.hide_render=True
        add_shell_field(scene,objects['SHIP ROOT / bow -Y, engine +Y, up +Z'],
                        objects['Clear spherical cabin'].scale.x)
        camdata=bpy.data.cameras.new(shot['id']+' camera');camdata.clip_end=1000
        cam=bpy.data.objects.new(shot['id']+' camera',camdata);scene.collection.objects.link(cam)
        scene.camera=cam;scene.render.fps=project['render']['fps']
        # Small camera fill makes the blockout geometry legible. It is a
        # reference light, separate from the shared sun's directional cues.
        filldata=bpy.data.lights.new(shot['id']+' reference fill','AREA')
        filldata.energy=150;filldata.size=4
        fill=bpy.data.objects.new(filldata.name,filldata)
        scene.collection.objects.link(fill);fill.parent=cam
        scene.frame_start=1;scene.frame_end=total
        scene.timeline_markers.clear()
        for name,frame in [('HANDLE IN',1),('EDIT IN',h['editInLocalFrame']),
                           ('EDIT OUT',h['editOutLocalFrameExclusive']),('HANDLE END',total)]:
            scene.timeline_markers.new(name,frame=frame)
        scene['shot_id']=shot['id'];scene['source_note_id']=shot['sourceNoteId']
        scene['description']=shot['description'];scene['transition_intent']=blocking['transition']
        scene['master_edit_start_frame']=shot['startFrame'];scene['master_edit_end_exclusive']=shot['endFrameExclusive']
        scene['lead_in_frames']=h['leadInFrames'];scene['lead_out_frames']=h['leadOutFrames']
        bpy.context.window.scene=scene
        if blocking['figurePose']=='window':
            folded_figure(scene,objects)
            # Art-directed planet moves beneath/forward of her gaze; camera sees space.
            objects['PLANET ROOT / independent artistic scale'].location=(0,-18,-36)
        if blocking.get('hologram'):
            # Spatial diagram is a separate, editable effect, not real moons.
            mat=bpy.data.materials['Cyan orientation and engine light']
            center=Vector((.65,-.65,.85))
            for radius in (.26,.48,.72):
                curve=bpy.data.curves.new('Hologram orbit','CURVE');curve.dimensions='3D'
                curve.bevel_depth=.007
                spline=curve.splines.new('POLY');spline.points.add(63)
                for i,p in enumerate(spline.points):
                    angle=2*math.pi*i/64
                    p.co=(*(center+Vector((radius*math.cos(angle),radius*math.sin(angle),0))),1)
                spline.use_cyclic_u=True
                obj=bpy.data.objects.new('Hologram orbit',curve);scene.collection.objects.link(obj)
                obj.data.materials.append(mat)
            coll=bpy.data.collections.new(shot['id']+' hologram');scene.collection.children.link(coll)
            for i,offset in enumerate(((0,0,0),(.26,0,0),(-.48,0,0),(.45,.56,.10))):
                proxy_piece('Diagram node '+str(i),center+Vector(offset),(.04,.04,.04),None,coll,mat)
        if spec.get('proposal'):
            coll=next(c for c in scene.collection.children if 'FIGURE' in c.name)
            for x in (-.20,-.06):
                proxy_piece('Eye position cue',(x,-.195,1.09),(.028,.018,.025),
                            objects['FIGURE ROOT / floating pose'],coll,
                            bpy.data.materials['Cyan orientation and engine light'])
        move=blocking.get('moveFrames',shot['frames']-1)
        last_edit=h['editOutLocalFrameExclusive']-1
        keys=sorted(set([1,h['editInLocalFrame'],min(total,h['editInLocalFrame']+move),last_edit,total]))
        for frame in keys:
            t=(frame-h['editInLocalFrame'])/max(1,move)
            if 'moveFrames' in blocking:t=min(1,t)
            cam.location=lerp(blocking['cameraStart'],blocking['cameraEnd'],t)
            target=lerp(blocking['targetStart'],blocking['targetEnd'],t)
            cam.rotation_euler=(target-cam.location).to_track_quat('-Z','Y').to_euler()
            camdata.lens=blocking.get('lens',blocking.get('lensStart',42))+(blocking.get('lensEnd',blocking.get('lens',42))-blocking.get('lensStart',blocking.get('lens',42)))*t
            cam.keyframe_insert('location',frame=frame);cam.keyframe_insert('rotation_euler',frame=frame)
            camdata.keyframe_insert('lens',frame=frame)
            for name,start,end in [('SHIP ROOT / bow -Y, engine +Y, up +Z',blocking.get('shipStart',[0,0,0]),blocking.get('shipEnd',[0,0,0])),
                                   ('FIGURE ROOT / floating pose',blocking.get('figureStart',[0,0,0]),blocking.get('figureEnd',[0,0,0]))]:
                if blocking['figurePose']=='window' and name.startswith('FIGURE'):continue
                objects[name].location=lerp(start,end,t);objects[name].keyframe_insert('location',frame=frame)
            if 'sunStrengthEnd' in blocking:
                sun=objects['Shared distant sun'].data
                sun.energy=2.5+(blocking['sunStrengthEnd']-2.5)*max(0,min(1,t))
                sun.keyframe_insert('energy',frame=frame)
        # Check every generated frame of shots intended to remain inside.
        # Shot 003 intentionally crosses the thin shell during its reveal.
        if blocking['figurePose']=='window' or blocking.get('interior'):
            shell=objects['Clear spherical cabin']
            gaps=[]
            for frame in range(1,total+1):
                scene.frame_set(frame)
                local=shell.matrix_world.inverted() @ cam.matrix_world.translation
                gaps.append((1-local.length)*min(shell.scale))
            scene['minimum_camera_shell_clearance']=min(gaps)
            required_clearance=.1 if spec.get('proposal') else .2
            if min(gaps)<required_clearance:
                raise ValueError(f"{shot['id']}: interior camera is too close to shell ({min(gaps):.3f})")
            # Explicit art direction: moon identities and the shared sun stay
            # fixed, while positions may be composed for this interior angle.
            scene.frame_set(h['editInLocalFrame'])
            for placement in blocking.get('moonScreenPlacement',[]):
                root=next(o for o in objects.values() if o.get('celestial_id')==placement['id'] and o.type=='MESH').parent
                x,y,distance=placement['view']
                half_width=distance*math.tan(camdata.angle_x/2)
                offset=Vector((x*half_width,y*half_width*9/16,-distance))
                root.location=cam.location+cam.rotation_euler.to_quaternion() @ offset
        scene.render.resolution_x=960;scene.render.resolution_y=540
        scene.cycles.samples=8 if spec.get('proposal') else 16;scene.render.image_settings.file_format='PNG'
        scene.world=template.world.copy()
        scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.45
        scene.view_settings.exposure=.3
        scene.frame_set(h['editInLocalFrame'])
        scenes.append((shot,scene))
    bpy.context.window.scene=scenes[0][1]
    bpy.ops.wm.save_as_mainfile(filepath=str(out/(spec.get('blendFilename','opening-storyboard-v01.blend'))))
    manifest=[]
    for shot,scene in scenes:
        bpy.context.window.scene=scene
        stills = [] if '--motion-only' in args or (only and shot['id']!=only) else [('edit-in',shot['handles']['editInLocalFrame']),
                             ('edit-out',shot['handles']['editOutLocalFrameExclusive']-1)]
        if stills and not spec.get('proposal'):
            stills.insert(0,('lead-in',1))
        for label,frame in stills:
            scene.frame_set(frame);scene.render.filepath=str(out/(shot['id']+'-'+label+'.png'))
            bpy.ops.render.render(write_still=True)
        manifest.append({'id':shot['id'],'title':shot['title'],'frames':shot['frames'],
                         'handles':shot['handles'],'scene':scene.name})
    if '--motion' in args or '--motion-only' in args:
        for shot,scene in scenes:
            if only and shot['id']!=only:continue
            bpy.context.window.scene=scene
            scene.render.resolution_x=640;scene.render.resolution_y=360;scene.cycles.samples=4
            scene.render.engine='BLENDER_EEVEE'
            if hasattr(scene.eevee,'taa_render_samples'):scene.eevee.taa_render_samples=8
            scene.render.image_settings.media_type='VIDEO';scene.render.image_settings.file_format='FFMPEG'
            scene.render.ffmpeg.format='MPEG4';scene.render.ffmpeg.codec='H264'
            scene.render.ffmpeg.constant_rate_factor='MEDIUM'
            scene.render.filepath=str(out/(shot['id']+'-handles.mp4'))
            bpy.ops.render.render(animation=True)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('STORYBOARD COMPLETE',out,flush=True)


main()
