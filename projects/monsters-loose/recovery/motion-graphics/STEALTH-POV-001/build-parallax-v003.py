import bpy,math,pathlib,json,bisect
root=pathlib.Path(__file__).resolve().parent;job=root.parent.parent
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=1;s.cycles.use_denoising=False
s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=193;s.view_settings.view_transform='Standard'
bpy.ops.object.camera_add(location=(0,0,20));cam=bpy.context.object;s.camera=cam
cam.data.lens=53.5;cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL'
# Projective UV shell: original screen rays intersect a shallow depth bowl.
# The moon region is distant; nearby lower/peripheral foliage is nearer.
nx,ny=96,54;verts=[];uvs=[]
for j in range(ny+1):
 for i in range(nx+1):
  u=i/nx;v=j/ny;r=math.sqrt(((u-.24)/.85)**2+((v-.85)/.85)**2)
  depth=20/(1+1.3*r**1.8)
  verts.append(((u-.5)*.72*depth,(v-.5)*.405*depth,20-depth));uvs.append((u,v))
faces=[]
for j in range(ny):
 for i in range(nx):
  a=j*(nx+1)+i;faces.append((a,a+1,a+nx+2,a+nx+1))
mesh=bpy.data.meshes.new('Projective curved depth surface');mesh.from_pydata(verts,[],faces);mesh.update()
uv=mesh.uv_layers.new(name='Source projection')
for poly in mesh.polygons:
 for loop in poly.loop_indices:uv.data[loop].uv=uvs[mesh.loops[loop].vertex_index]
ob=bpy.data.objects.new('Curved footage shell - moon far, edges near',mesh);s.collection.objects.link(ob)
mat=bpy.data.materials.new('Unlit source footage');mat.use_nodes=True
nodes=mat.node_tree.nodes;nodes.clear()
tex=nodes.new('ShaderNodeTexImage');tex.image=bpy.data.images.load(str(job/'video-tests'/'KLING-POV-002'/'KLING-POV-002-01.mp4'))
tex.image_user.frame_duration=193;tex.image_user.frame_start=1;tex.image_user.use_auto_refresh=True
emit=nodes.new('ShaderNodeEmission');emit.inputs['Strength'].default_value=1
out=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(tex.outputs['Color'],emit.inputs['Color']);mat.node_tree.links.new(emit.outputs[0],out.inputs['Surface']);ob.data.materials.append(mat)
grid=json.loads((job/'animatic'/'animatic-data.json').read_text())['beats'];times=[b['time'] for b in grid]
for f in range(1,194):
 t=367/24+(f-1)/24;i=max(0,min(len(grid)-2,bisect.bisect_right(times,t)-1))
 beat=grid[i]['project_beat']+(t-times[i])/(times[i+1]-times[i]);phase=math.pi*(beat-40)
 dx=.095*math.sin(phase*.5)+.018*math.sin(phase*.25)
 dy=.115*math.sin(phase)+.012*math.sin(phase*2+.6)
 cam.location=(dx,dy,20);cam.keyframe_insert(data_path='location',frame=f)
 # Off-axis compensation preserves the distant plane's screen position.
 cam.data.shift_x=-dx/(20*36/53.5);cam.data.shift_y=-dy/(20*36/53.5)
 for p in ('shift_x','shift_y'):cam.data.keyframe_insert(data_path=p,frame=f)
s.use_nodes=True;g=bpy.data.node_groups.new('Parallax with approved lens treatment','CompositorNodeTree');s.compositing_node_group=g
g.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor')
render=g.nodes.new('CompositorNodeRLayers');lens=g.nodes.new('CompositorNodeLensdist')
lens.inputs['Distortion'].default_value=.10;lens.inputs['Dispersion'].default_value=.002;lens.inputs['Fit'].default_value=True
out=g.nodes.new('NodeGroupOutput');g.links.new(render.outputs['Image'],lens.inputs['Image']);g.links.new(lens.outputs['Image'],out.inputs['Image'])
s.render.image_settings.media_type='IMAGE';s.render.image_settings.file_format='PNG';s.frame_set(70);s.render.filepath=str(root/'parallax-v003-check.png');bpy.ops.render.render(write_still=True)
s.render.image_settings.media_type='VIDEO';s.render.image_settings.file_format='FFMPEG';s.render.ffmpeg.format='MPEG4';s.render.ffmpeg.codec='H264';s.render.ffmpeg.constant_rate_factor='HIGH'
s.render.filepath=str(root/'Stealth-POV-parallax-v003.mp4');s.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'Stealth-POV-parallax-v003.blend'))
bpy.ops.render.render(animation=True)
