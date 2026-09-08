"""Animated native ribbon geometry, three depth blooms, exact audio/radial controls."""
from pathlib import Path
O=Path(__file__).resolve().parent
prefix=(O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0]
exec(compile(prefix,str(O/'lights2_native.py'),'exec'))
import numpy as np
bpy.data.objects.remove(plane,do_unlink=True)
s.cycles.samples=32
materials=[]
for band in range(3):
    m=bpy.data.materials.new(f'Beam depth {band}');m.use_nodes=True;m.node_tree.nodes.clear();b=Builder(m.node_tree)
    color=b.n.new('ShaderNodeVertexColor');color.layer_name='Beam'
    em=b.n.new('ShaderNodeEmission');b.plug(color.outputs['Color'],em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
    a=s.view_layers[0].aovs.add();a.name=f'Band{band}';a.type='COLOR'
    av=b.n.new('ShaderNodeOutputAOV');av.aov_name=f'Band{band}';b.plug(color.outputs['Color'],av.inputs['Color']);materials.append(m)
theta=np.arange(512)*math.tau/512
for f,row in enumerate(rows):
    t=(data['song_frames'][0]+f)/24;signal=np.array(row['signal']);groups=[([],[],[]) for _ in range(3)]
    arrivals=[]
    for event_id,(hit,strength) in enumerate(data['events']):
        age=t-hit
        if -.5<=age<=.2:arrivals.append((75*(480/75)**np.clip((age+.5)/.5,0,1),math.exp(-max(age,0)/.075),event_id))
    for k,radius in enumerate(row['detected_radii']):
        travel=0;travelcolor=np.zeros(3)
        for rr,weight,event_id in arrivals:
            weight*=math.exp(-.5*(math.log(radius/rr)/.19)**2);travel+=weight;travelcolor+=np.array(data['pulse_colors_linear_rgb'][event_id])*weight
        offset=signal*(2+min(radius/70,5))*10+.35*np.sin(theta*53+f*.8)
        points=np.column_stack((630+(radius+offset)*np.cos(theta),315+(radius+offset)*np.sin(theta)*172/174))
        deriv=(np.roll(offset,-1)-np.roll(offset,1))/(2*math.tau/512*radius);dwell=1/np.sqrt(1+deriv**2)
        scan=.23+.77*np.exp(-((f/24*.65+k*.11-theta/math.tau)%1)/.38);depth=min(radius/480,1)
        verts,faces,colors=groups[0 if radius<160 else 1 if radius<320 else 2]
        for i in range(512):
            ambient=(.24+.22*depth)*scan[i]*np.array([.23,.39,.38])
            color=(ambient+travelcolor*2.5)*(.65+1.8*depth**1.4)*dwell[i]
            a=points[i];z=points[(i+1)%512];delta=z-a;normal=np.array([-delta[1],delta[0]])/max(np.linalg.norm(delta),1e-6)
            half=(1+int(2*dwell[i]+min(travel,1)*2)+int(depth*2))*.25
            corners=[a+normal*half,z+normal*half,z-normal*half,a-normal*half];j=len(verts)
            verts.extend([((p[0]-640)/80,(360-p[1])/80,0) for p in corners]);faces.append((j,j+1,j+2,j+3));colors.extend([(*color,1)]*4)
    for band,(verts,faces,colors) in enumerate(groups):
        if not verts:continue
        mesh=bpy.data.meshes.new(f'Frame{f+1} depth{band}');mesh.from_pydata(verts,[],faces);mesh.materials.append(materials[band])
        attr=mesh.color_attributes.new(name='Beam',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',np.asarray(colors,dtype=np.float32).ravel())
        ob=bpy.data.objects.new(mesh.name,mesh);s.collection.objects.link(ob)
        for at,hidden in [(0,True),(f,True),(f+1,False),(f+2,True)]:ob.hide_render=hidden;ob.keyframe_insert('hide_render',frame=at)
t=bpy.data.node_groups.new('Depth-dependent native beam scatter','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers');light=rl.outputs['Image']
for band in range(3):
    core=rl.outputs[f'Band{band}']
    for sigma,gain in [(2+band*1.5,1.2),(8+band*5,.65+band*.25),(22+band*9,.25+band*.15)]:light=b.mix(light,b.mix(b.blur(core,sigma,W),(gain,gain,gain,1),mode='MULTIPLY'))
end=b.n.new('NodeGroupOutput');b.plug(b.mix(pic,light),end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'tunnel_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
