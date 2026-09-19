import bpy, json, math, random, sys
from pathlib import Path

o=Path(__file__).resolve().parent
name=sys.argv[sys.argv.index('--')+1]
tracks=json.loads((o/'tracks.json').read_text())[name]
landing=name=='KLING-OPEN-003'
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=121
s.render.film_transparent=True;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object
s.camera.data.type='ORTHO';s.camera.data.ortho_scale=960;s.camera.data.clip_end=2000

def patch(label,col,ripple=False):
    m=bpy.data.materials.new(label);m.use_nodes=True;n=m.node_tree.nodes;n.clear();lk=m.node_tree.links
    uv=n.new('ShaderNodeTexCoord');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE'
    dist.inputs[1].default_value=(.5,.5,0);lk.new(uv.outputs['UV'],dist.inputs[0])
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=0;ramp.color_ramp.elements[0].color=(1,1,1,1)
    ramp.color_ramp.elements[1].position=.5;ramp.color_ramp.elements[1].color=(0,0,0,1)
    ramp.color_ramp.interpolation='EASE';lk.new(dist.outputs['Value'],ramp.inputs[0]);factor=ramp.outputs[0]
    if ripple:
        vec=n.new('ShaderNodeVectorMath');vec.operation='MULTIPLY';vec.inputs[1].default_value=(5,95,1);lk.new(uv.outputs['UV'],vec.inputs[0])
        noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=1;noise.inputs['Detail'].default_value=2;lk.new(vec.outputs[0],noise.inputs[0])
        contrast=n.new('ShaderNodeValToRGB');contrast.color_ramp.elements[0].position=.34;contrast.color_ramp.elements[0].color=(.04,.04,.04,1);contrast.color_ramp.elements[1].position=.62;lk.new(noise.outputs['Fac'],contrast.inputs[0])
        mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';lk.new(factor,mul.inputs[0]);lk.new(contrast.outputs[0],mul.inputs[1]);factor=mul.outputs[0]
    alpha=n.new('ShaderNodeMath');alpha.operation='MULTIPLY';lk.new(factor,alpha.inputs[0])
    e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*col,1)
    tr=n.new('ShaderNodeBsdfTransparent');mix=n.new('ShaderNodeMixShader');lk.new(alpha.outputs[0],mix.inputs[0]);lk.new(tr.outputs[0],mix.inputs[1]);lk.new(e.outputs[0],mix.inputs[2])
    out=n.new('ShaderNodeOutputMaterial');lk.new(mix.outputs[0],out.inputs[0])
    me=bpy.data.meshes.new(label);me.from_pydata([(-1,-1,0),(1,-1,0),(1,1,0),(-1,1,0)],[],[(0,1,2,3)]);me.update()
    ob=bpy.data.objects.new(label,me);s.collection.objects.link(ob);me.materials.append(m)
    u=me.uv_layers.new()
    for poly in me.polygons:
        for li in poly.loop_indices:
            v=me.vertices[me.loops[li].vertex_index].co;u.data[li].uv=((v.x+1)/2,(v.y+1)/2)
    return ob,alpha.inputs[1]

def pulse(f,phase,width):
    d=(f-phase+14.5)%29-14.5
    return math.exp(-.5*(d/width)**2)

specs=[('beacon',(1,.008,.003),3.3 if landing else 1.4,11 if landing else 4.5),('tail',(.8,.92,1),2.7 if landing else 1.1,10 if landing else 4),('nav',(1,.012,.004),1.7 if landing else .8,6 if landing else 2.5)]
for label,col,core,halo in specs:
    elements=[]
    for suffix,radius,opacity,color in [('halo',halo,.52,col),('core',core,1,col),('hot center',core*.44,1,(1,.65,.5) if label!='tail' else (1,1,1))]:
        ob,a=patch(label+' '+suffix,color);elements.append((ob,a,radius,opacity))
    reflected=[]
    if landing:
        for suffix,rx,ry,power in [('broad wet bloom',17,38,.40),('broken reflection',8,40,.9),('thin highlight',2.5,33,.65)]:
            ob,a=patch(label+' '+suffix,col,True);reflected.append((ob,a,rx,ry,power))
    for f in range(1,122):
        src=f-1;master=src+(86 if landing else 1)
        intensity=pulse(master,7,1.8) if label=='beacon' else min(1,pulse(master,17,.7)+pulse(master,20,.7)) if label=='tail' else .50
        x,y=tracks[label][src]
        for z,(ob,a,radius,opacity) in enumerate(elements):
            ob.location=(x-480,270-y,2+z*.1);ob.scale=(radius,radius,1)
            a.default_value=intensity*opacity;a.keyframe_insert(data_path='default_value',frame=f)
            ob.keyframe_insert(data_path='location',frame=f)
        for z,(ob,a,rx,ry,power) in enumerate(reflected):
            # Ground-space footprints are below skids, never painted over aircraft.
            if label=='beacon':cx,cy=x+3,467;sy=ry
            elif label=='tail':cx,cy=x-2,430;sy=ry*.48
            else:cx,cy=x+6,476;sy=ry
            ob.location=(cx-480,270-cy,1+z*.1);ob.scale=(rx,sy,1)
            a.default_value=intensity*power;a.keyframe_insert(data_path='default_value',frame=f)
            ob.keyframe_insert(data_path='location',frame=f)
for action in bpy.data.actions:
    for layer in action.layers:
        for strip in layer.strips:
            for bag in strip.channelbags:
                for cu in bag.fcurves:
                    for k in cu.keyframe_points:k.interpolation='LINEAR'
folder=o/(name+'-overlay');folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(folder/'lights-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/(name+'-lights-v001.blend')))
bpy.ops.render.render(animation=True)
