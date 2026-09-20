import bpy,math,bisect
from pathlib import Path
o=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=153
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
bpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1280;s.camera.data.clip_end=2000
cols,rows=256,144
points=[(-640+x*1280/cols,-360+y*720/rows,0) for y in range(rows+1) for x in range(cols+1)]
faces=[]
for y in range(rows):
 for x in range(cols):
  a=y*(cols+1)+x;faces.append((a,a+1,a+cols+2,a+cols+1))
me=bpy.data.meshes.new('Roar pressure refraction grid');me.from_pydata(points,[],faces);me.update()
ob=bpy.data.objects.new('Air ahead of lizard mouth',me);s.collection.objects.link(ob);uv=me.uv_layers.new()
for p in me.polygons:
 for li in p.loop_indices:
  v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=((v.x+640)/1280,(v.y+360)/720)
m=bpy.data.materials.new('Original duel footage');m.use_nodes=True;n=m.node_tree.nodes;n.clear()
tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(o/'source/frame-0001.png'));tex.image.source='SEQUENCE';tex.image_user.frame_duration=153;tex.image_user.frame_start=1;tex.image_user.use_auto_refresh=True
em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);me.materials.append(m)
ob.shape_key_add(name='Basis')
track=[(0,501,274),(8,501,252),(16,515,256),(24,541,292),(32,552,314),(40,555,326),(48,554,340),(56,550,344)]
for f in range(56):
 j=min(len(track)-2,max(0,bisect.bisect_right([k[0] for k in track],f)-1));a,b=track[j:j+2];q=(f-a[0])/(b[0]-a[0]);cx=a[1]+q*(b[1]-a[1]);cy=a[2]+q*(b[2]-a[2])
 gain=min(1,(f+1)/5,max(0,(56-f)/10))
 key=ob.shape_key_add(name='Roar master'+str(2638+f))
 for v,(x,y,z) in zip(key.data,points):
  px=x+640;py=360-y;dx=px-cx;dy=(py-cy)/.72;rad=math.hypot(dx,dy)
  if dx<5 or dx>185 or abs(py-cy)>85 or px>727:continue
  cone=min(1,(dx-5)/18)*min(1,(185-dx)/35)*math.exp(-((py-cy)/65)**4)*min(1,max(0,(727-px)/25))
  strength=0
  for start in range(0,54,7):
   age=f-start
   if 0<=age<22:
    band=(rad-(10+age*8.5))/9
    strength+=19*math.exp(-.5*band*band)*math.cos(band*1.8)*(1-age/26)
  amount=strength*cone*gain
  if rad>1:v.co.x+=amount*dx/rad;v.co.y-=amount*dy/rad*.72
 for at,val in [(f,0),(f+1,1),(f+2,0)]:key.value=val;key.keyframe_insert('value',frame=at)
(o/'render').mkdir(exist_ok=True);s.render.filepath=str(o/'render/frame-')
bpy.ops.wm.save_as_mainfile(filepath=str(o/'Duel-roar-v001.blend'),compress=True);bpy.ops.render.render(animation=True)
