from pathlib import Path
import bpy
OUT=Path(__file__).resolve().parent
bpy.ops.wm.read_factory_settings(use_empty=True)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=8
sc.render.resolution_x=1280;sc.render.resolution_y=720;sc.render.resolution_percentage=100;sc.render.fps=24
sc.view_settings.view_transform='Standard';sc.view_settings.look='None'
cam=bpy.data.cameras.new('Camera');obj=bpy.data.objects.new('Camera',cam);sc.collection.objects.link(obj)
obj.location=(0,0,10);cam.type='ORTHO';cam.ortho_scale=16;sc.camera=obj
mesh=bpy.data.meshes.new('Artifact crop');mesh.from_pydata([(-8,-4.5,0),(8,-4.5,0),(8,4.5,0),(-8,4.5,0)],[],[(0,1,2,3)])
uv=mesh.uv_layers.new()
for loop,coord in zip(uv.data,[(445/1280,20/720),(845/1280,20/720),(845/1280,245/720),(445/1280,245/720)]):loop.uv=coord
plate=bpy.data.objects.new('Artifact source crop',mesh);sc.collection.objects.link(plate)
mat=bpy.data.materials.new('Unchanged picture');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear()
tex=n.new('ShaderNodeTexImage');em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(tex.outputs['Color'],em.inputs['Color']);mat.node_tree.links.new(em.outputs[0],out.inputs['Surface']);mesh.materials.append(mat)
def material(name,color):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=(*color,1);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);return m
bpy.ops.mesh.primitive_plane_add(size=2,location=(0,3.931,.1));bpy.context.object.scale=(8,.569,1);bpy.context.object.data.materials.append(material('Header black',(.0037,)*3))
white=material('Text',(.9,.9,.9))
def text(body,pos,size):
    c=bpy.data.curves.new('Label','FONT');c.body=body;c.size=size;o=bpy.data.objects.new('Label',c);sc.collection.objects.link(o);o.location=(*pos,.2);c.materials.append(white);return c
text('Exobiologist offscreen: To who?',(-7.8,4.12),.30)
text('Earlier artifact cutaway / source frames23..32',(-7.8,3.78),.21)
label=text('',(-7.8,3.48),.18);text('6',(7.2,3.92),.38)
(OUT/'extension_frames').mkdir(exist_ok=True)
sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGB'
for i in range(9):
    tex.image=bpy.data.images.load(str(OUT/'extension_plate'/f'{i+1:04}.png'))
    label.body=f'Song {4538+i} | {(4538+i)/24:.3f}s'
    sc.render.filepath=str(OUT/'extension_frames'/f'{i+1:04}.png');bpy.ops.render.render(write_still=True)
