import bpy,json,math
from pathlib import Path
o=Path(__file__).resolve().parent
tracks=json.loads((o/'tracks.json').read_text())
visibility=json.loads((o/'visibility.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=1916;s.render.resolution_y=1080;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=97
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
  master=f-1+1696
  # Smooth staggered 29-frame beacon cycle, matching opening aviation cadence.
  d=(master-7-i*4+14.5)%29-14.5
  visible=visibility[str(i)][f-1]
  ma.default_value=.94*visible;ma.keyframe_insert(data_path='default_value',frame=f)
  p=math.exp(-.5*(d/3.4)**2)*visible
  for z,ob in enumerate([mute,halo,core,hot]):
   ob.location=(x-480,270-y,1+z*.1);ob.keyframe_insert(data_path='location',frame=f)
  for a,v in [(ha,.9*p),(ca,(.08+.92*p)*visible),(wa,.98*p)]:
   a.default_value=v;a.keyframe_insert(data_path='default_value',frame=f)
for action in bpy.data.actions:
 for layer in action.layers:
  for strip in layer.strips:
   for bag in strip.channelbags:
    for cu in bag.fcurves:
     for k in cu.keyframe_points:k.interpolation='LINEAR'
folder=o/'overlay';folder.mkdir(exist_ok=True)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.filepath=str(folder/'lights-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Rope-demo-lights-v001.blend'))
bpy.ops.render.render(animation=True)
