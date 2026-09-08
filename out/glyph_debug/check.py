import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.render.engine='BLENDER_EEVEE';sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100
sc.world.color=(0,0,0);sc.view_settings.view_transform='Standard'
font=bpy.data.fonts.load(str(ROOT/'assets/fonts/fredoka/Fredoka[wdth,wght].ttf'))
mat=bpy.data.materials.new('white');mat.use_nodes=True
n=mat.node_tree.nodes;n.clear();out=n.new('ShaderNodeOutputMaterial');em=n.new('ShaderNodeEmission');mat.node_tree.links.new(em.outputs[0],out.inputs[0])
records=[]
for row,offset in enumerate([.018,0.]):
 for col,char in enumerate('mrMR'):
  c=bpy.data.curves.new(char,'FONT');c.body=char;c.font=font if row==0 else bpy.data.fonts.load(str(ROOT/'assets/fonts/fredoka/Fredoka-Bold.ttf'));c.size=44*.66/74;c.align_x='CENTER';c.align_y='CENTER';c.offset=offset;c.extrude=.001;c.resolution_u=8
  o=bpy.data.objects.new(char,c);sc.collection.objects.link(o);o.location=((col-1.5)*2,1.4-row*2.8,0);o.data.materials.append(mat)
  for sel in bpy.context.selected_objects:sel.select_set(False)
  o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH')
  records.append({'char':char,'offset':offset,'ymax':max(v.co.y for v in o.data.vertices),'ymin':min(v.co.y for v in o.data.vertices)})
  o.scale=(3.8,3.8,3.8)
bpy.ops.object.camera_add(location=(0,0,14));sc.camera=bpy.context.object;sc.camera.data.lens=42
sc.render.filepath=str(OUT/'offset_comparison.png');bpy.ops.render.render(write_still=True)
(OUT/'geometry.json').write_text(json.dumps(records,indent=2))
