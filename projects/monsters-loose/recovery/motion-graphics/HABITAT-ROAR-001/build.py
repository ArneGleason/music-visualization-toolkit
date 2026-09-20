import bpy,math,json
from pathlib import Path
# Blender bundled Python may not have Pillow; masks are prepared separately.

o=Path(__file__).resolve().parent;bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene;s.render.engine='BLENDER_EEVEE';s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=56;s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
bpy.ops.object.camera_add(location=(0,0,1000));s.camera=bpy.context.object;s.camera.data.type='ORTHO';s.camera.data.ortho_scale=1280;s.camera.data.clip_end=2000
cols,rows=256,144;points=[(-640+x*1280/cols,-360+y*720/rows,0) for y in range(rows+1) for x in range(cols+1)];faces=[]
for y in range(rows):
 for x in range(cols):
  a=y*(cols+1)+x;faces.append((a,a+1,a+cols+2,a+cols+1))
me=bpy.data.meshes.new('Pressure-refraction grid');me.from_pydata(points,[],faces);me.update();ob=bpy.data.objects.new('Subtle enclosed roar',me);s.collection.objects.link(ob);uv=me.uv_layers.new()
for p in me.polygons:
 for li in p.loop_indices:
  v=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=((v.x+640)/1280,(v.y+360)/720)
m=bpy.data.materials.new('Existing lit habitat movie');m.use_nodes=True;n=m.node_tree.nodes;n.clear();tex=n.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(o/'source/frame-0001.png'));tex.image.source='SEQUENCE';tex.image_user.frame_duration=56;tex.image_user.frame_start=1;tex.image_user.use_auto_refresh=True;em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);m.node_tree.links.new(em.outputs[0],out.inputs['Surface']);me.materials.append(m)
ob.shape_key_add(name='Basis');records=json.loads((o/'tracking.json').read_text());starts=[16,23,30,37,44,51]
for rec in records:
 f=rec['local_frame'];cx,cy=rec['mouth'];gain=rec['gain']
 if gain<=0:continue
 key=ob.shape_key_add(name=f'Roar master{2036+f}')
 for v,(x,y,z) in zip(key.data,points):
  px=x+640;py=360-y;dx=px-cx;dy=(py-cy)/.72;radius=math.hypot(dx,dy)
  if dx<3 or dx>175 or abs(py-cy)>100:continue
  cone=max(0,min(1,(dx-3)/14))*max(0,min(1,(175-dx)/35))*math.exp(-((py-cy)/75)**4)
  # Posts stay rigid even before compositing protection, including their edges.
  protect=min(1,max(0,(abs(px-465)-17)/9))*min(1,max(0,(abs(px-552)-9)/7))
  strength=0
  for start in starts:
   age=f-start
   if 0<=age<22:
    band=(radius-(10+age*8.5))/9;strength+=1.9*math.exp(-.5*band*band)*math.cos(band*1.8)*(1-age/26)
  amount=strength*cone*protect*gain
  if radius>1:v.co.x+=amount*dx/radius;v.co.y-=amount*dy/radius*.72
 for at,value in [(f,0),(f+1,1),(f+2,0)]:key.value=value;key.keyframe_insert('value',frame=at)
# Composite the original outside the tracked air pocket and across foreground posts.
nt=bpy.data.node_groups.new('Architecture protected roar composite','CompositorNodeTree');s.compositing_node_group=nt;nt.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');nodes=nt.nodes;links=nt.links;out=nodes.new('NodeGroupOutput');render=nodes.new('CompositorNodeRLayers')
def seq(name,folder,prefix,color):
 n=nodes.new('CompositorNodeImage');n.name=name;n.image=bpy.data.images.load(str(o/folder/(prefix+'0001.png')));n.image.source='SEQUENCE';n.image.colorspace_settings.name=color;n.frame_duration=56;n.frame_start=1;n.use_auto_refresh=True;return n
src=seq('Original enclosure and beacons','source','frame-','sRGB');mask=seq('Air only, structure protected','masks','mask-','Non-Color');mix=nodes.new('ShaderNodeMix');mix.data_type='RGBA';links.new(mask.outputs['Image'],mix.inputs[0]);links.new(src.outputs['Image'],mix.inputs[6]);links.new(render.outputs['Image'],mix.inputs[7]);links.new(mix.outputs[2],out.inputs['Image'])
(o/'render').mkdir(exist_ok=True);s.render.filepath=str(o/'render/frame-');bpy.ops.wm.save_as_mainfile(filepath=str(o/'Habitat-enclosed-roar-v001.blend'),compress=True);bpy.ops.render.render(animation=True)
