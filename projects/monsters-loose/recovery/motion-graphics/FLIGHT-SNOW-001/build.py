import bpy,math,random
from pathlib import Path
o=Path(__file__).resolve().parent;random.seed(27)
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE'
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=37
s.render.film_transparent=True;s.view_settings.view_transform='Standard';s.view_settings.look='None'
bpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1280;s.camera.data.clip_end=2000
for i in range(24):
 bpy.ops.mesh.primitive_plane_add(size=2);ob=bpy.context.object;ob.name='Dispersing snow puff %02d'%i
 m=bpy.data.materials.new(ob.name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();L=m.node_tree.links
 coord=n.new('ShaderNodeTexCoord');dist=n.new('ShaderNodeVectorMath');dist.operation='DISTANCE';dist.inputs[1].default_value=(.5,.5,0);L.new(coord.outputs['UV'],dist.inputs[0])
 edge=n.new('ShaderNodeMapRange');edge.clamp=True;edge.interpolation_type='SMOOTHERSTEP';edge.inputs['From Min'].default_value=.12;edge.inputs['From Max'].default_value=.5;edge.inputs['To Min'].default_value=1;edge.inputs['To Max'].default_value=0;L.new(dist.outputs['Value'],edge.inputs['Value'])
 noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=5;noise.inputs['Detail'].default_value=3;L.new(coord.outputs['UV'],noise.inputs['Vector'])
 mul=n.new('ShaderNodeMath');mul.operation='MULTIPLY';L.new(edge.outputs[0],mul.inputs[0]);L.new(noise.outputs['Fac'],mul.inputs[1])
 fade=n.new('ShaderNodeMath');fade.operation='MULTIPLY';L.new(mul.outputs[0],fade.inputs[0])
 trans=n.new('ShaderNodeBsdfTransparent');em=n.new('ShaderNodeEmission');v=random.uniform(.72,.95);em.inputs['Color'].default_value=(v*.86,v*.94,v,1)
 mix=n.new('ShaderNodeMixShader');out=n.new('ShaderNodeOutputMaterial');L.new(fade.outputs[0],mix.inputs[0]);L.new(trans.outputs[0],mix.inputs[1]);L.new(em.outputs[0],mix.inputs[2]);L.new(mix.outputs[0],out.inputs['Surface']);ob.data.materials.append(m)
 delay=random.randint(0,4);ox=random.uniform(-16,18);oy=random.uniform(-16,14);vx=random.uniform(-7,2.7);vy=random.uniform(-2,5);radius=random.uniform(45,100)
 for f in range(1,38):
  age=f-4-delay;t=max(0,age)
  px=1130+ox+vx*t;py=335+oy+vy*t+.065*t*t
  ob.location=(px-640,360-py,i*.02);rad=radius*(.25+min(t,23)/15)
  ob.scale=(rad,rad*.8,1);ob.keyframe_insert('location',frame=f);ob.keyframe_insert('scale',frame=f)
  gain=0 if age<0 else min(1,(age+1)/3)*max(0,1-max(0,age-11)/24)*.95
  fade.inputs[1].default_value=gain;fade.inputs[1].keyframe_insert('default_value',frame=f)
# Holdout silhouette keeps generated beast in front of powder; interpolated padded outlines.
keys=[
 (0,[(515,90),(690,20),(880,45),(1010,90),(1115,200),(1170,360),(1040,425),(830,430),(630,390),(510,280)]),
 (10,[(450,150),(620,45),(805,55),(1000,130),(1098,215),(1080,335),(1000,402),(730,420),(500,390),(405,315)]),
 (20,[(390,195),(565,65),(800,75),(1005,150),(1050,230),(1040,375),(905,440),(650,500),(405,475),(350,360)]),
 (30,[(540,100),(690,-50),(1090,-50),(1370,0),(1400,200),(1390,530),(1280,780),(930,790),(650,640),(530,410)]),
 (36,[(830,-60),(1000,-100),(1390,-90),(1450,0),(1450,210),(1440,540),(1400,800),(1190,820),(1050,650),(840,390)])]
me=bpy.data.meshes.new('Beast holdout');me.from_pydata([(x-640,360-y,5) for x,y in keys[0][1]],[],[tuple(range(10))]);ob=bpy.data.objects.new('Protect snow beast foreground',me);s.collection.objects.link(ob)
m=bpy.data.materials.new('Transparent foreground holdout');m.use_nodes=True;n=m.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(h.outputs[0],out.inputs['Surface']);me.materials.append(m);ob.shape_key_add(name='Basis')
for idx,(f,points) in enumerate(keys):
 k=ob.shape_key_add(name='Silhouette '+str(f))
 for v,(x,y) in zip(k.data,points):v.co=(x-640,360-y,5)
 for j,(at,_) in enumerate(keys):k.value=1 if idx==j else 0;k.keyframe_insert('value',frame=at+1)
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';(o/'overlay').mkdir(exist_ok=True);s.render.filepath=str(o/'overlay/snow-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Flight-cliff-snow-v001.blend'));bpy.ops.render.render(animation=True)
