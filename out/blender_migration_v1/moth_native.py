"""Native wing light, centered optical warp, spectral contours and bloom."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
import gzip,numpy as np
s.cycles.samples=16
def aov(name,value):
    av=s.view_layers[0].aovs.add();av.name=name;av.type='VALUE';n=b.n.new('ShaderNodeOutputAOV');n.aov_name=name;b.plug(value,n.inputs['Value'])
matte=((b.op('MINIMUM',r,g)-.46)*4).clamp()*((r-blue+.04)*3).clamp()*b.op('LESS_THAN',y,425)*b.op('GREATER_THAN',x,70)*b.op('LESS_THAN',x,1210)
aov('Wing',matte)
sf=b.animated('Song time',[v['song_frame']+.5 for v in rows]);t=(sf-1524)/24
strength=((sf-1521)/13).smooth()*(1-((sf-1549)/12).smooth())
body=(-((x-640)/160)**2-((y-300)/245)**2).exp()
freedom=(-((x-640)/430)**2-((y-290)/300)**2).exp()*(1-.60*body)
breath=.075*b.op('SINE',t*7)*strength
dx=(22*b.op('SINE',y/94-t*6)+13*b.op('SINE',x/135+y/150+t*4))*strength*freedom+(x-640)*breath*freedom
dy=(18*b.op('SINE',x/110+t*5)+12*b.op('COSINE',y/140-x/170-t*4))*strength*freedom+(y-300)*breath*freedom
mx=b.op('MINIMUM',1273,b.op('MAXIMUM',6,x+dx))
my=b.op('MINIMUM',713,b.op('MAXIMUM',6,y+dy));active=b.op('GREATER_THAN',strength,0)
mx=mx*active+x*(1-active);my=my*active+y*(1-active);fringe=4.5*strength*freedom
for ch,sign in enumerate([-1,0,1]):
    aov(f'DX{ch}',(x-mx-sign*fringe)*W/1280);aov(f'DY{ch}',(my-sign*fringe*.3-y)*W/1280)
aov('EdgeEnvelope',strength*freedom)
distance=(((x-640)/640)**2+((y-300)/420)**2)**.5;aov('EdgeTint',.5+.5*b.op('SINE',distance*8-t*3))
em=b.n.new('ShaderNodeEmission');em.inputs[0].default_value=(0,0,0,1);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
optics=bpy.data.collections.new('Optics');s.collection.children.link(optics)
for c in list(plane.users_collection):c.objects.unlink(plane)
optics.objects.link(plane)
ghost=bpy.data.collections.new('Ghost');s.collection.children.link(ghost)
with gzip.open(D/'particles.json.gz','rt') as f:paths=json.load(f)
for fi,points in enumerate(paths):
    if not points:continue
    verts=[];faces=[];colors=[]
    for j,p in enumerate(points):
        start=len(verts);px,py=p['xy'];radius=p['radius']+.25
        for k in range(10):
            q=k*math.tau/10;verts.append(((px+radius*math.cos(q)-640)/80,(360-py-radius*math.sin(q))/80,j*.00001));colors.append((*p['rgb'],1))
        faces.append(tuple(range(start,start+10)))
    mesh=bpy.data.meshes.new(f'Wing particles{fi+1}');mesh.from_pydata(verts,[],faces)
    attr=mesh.color_attributes.new(name='Ink',type='FLOAT_COLOR',domain='POINT');attr.data.foreach_set('color',np.array(colors,dtype=np.float32).ravel())
    mat=bpy.data.materials.new(mesh.name);mat.use_nodes=True;mat.node_tree.nodes.clear();nb=Builder(mat.node_tree)
    color=nb.n.new('ShaderNodeVertexColor');color.layer_name='Ink';em=nb.n.new('ShaderNodeEmission');nb.plug(color.outputs[0],em.inputs[0]);mo=nb.n.new('ShaderNodeOutputMaterial');nb.plug(em.outputs[0],mo.inputs[0]);mesh.materials.append(mat)
    ob=bpy.data.objects.new(mesh.name,mesh);ghost.objects.link(ob)
    for at,hide in [(0,True),(fi,True),(fi+1,False),(fi+2,True)]:ob.hide_render=hide;ob.keyframe_insert('hide_render',frame=at)
s.view_layers[0].name='Optics';s.view_layers[0].layer_collection.children['Ghost'].exclude=True
layer=s.view_layers.new('Ghost');layer.layer_collection.children['Optics'].exclude=True
tree=bpy.data.node_groups.new('Native spectral moth composite','CompositorNodeTree');tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=tree;b=Builder(tree)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image'])
pic=b.combine([b.display(v) for v in b.split(scale.outputs[0])]);rl=b.n.new('CompositorNodeRLayers');rl.layer='Optics'
mask=b.blur(rl.outputs['Wing'],1.5,W);maskv=b.split(mask)[0]
gain=b.animated('Wing vocal response',[.08+.18*v['voice']+.30*v['breath'] for v in rows])
halo=b.mix(b.mix(b.blur(mask,6,W),(.26,)*3+(1,),mode='MULTIPLY'),b.mix(b.blur(mask,22,W),(.30,)*3+(1,),mode='MULTIPLY'));halov=b.split(halo)[0]
lit=b.combine([(a+a*maskv*gain*.2+halov*c*gain).clamp() for a,c in zip(b.split(pic),[1,.79,.43])])
channels=[]
for ch in range(3):
    dis=b.n.new('CompositorNodeDisplace');dis.inputs['Interpolation'].default_value='Bilinear';dis.inputs['Extension X'].default_value='Extend';dis.inputs['Extension Y'].default_value='Extend'
    b.plug(lit,dis.inputs['Image']);b.plug(b.combine([rl.outputs[f'DX{ch}'],rl.outputs[f'DY{ch}'],0]),dis.inputs['Displacement']);channels.append(b.split(dis.outputs[0])[ch])
warped=b.combine(channels);gray=sum(a*w for a,w in zip(channels,[.299,.587,.114]));fil=b.n.new('CompositorNodeFilter');fil.inputs['Type'].default_value='Laplace';b.plug(b.combine([gray]*3),fil.inputs['Image'])
edge=(b.op('ABSOLUTE',b.split(fil.outputs[0])[0])*(W/1280)**2/.3).clamp()*.3
edge=b.split(b.blur(b.combine([edge]*3),2,W))[0]*b.split(rl.outputs['EdgeEnvelope'])[0]
tint=b.split(rl.outputs['EdgeTint'])[0];base=[a+edge*(c*tint+d*(1-tint))*.45 for a,c,d in zip(channels,[.55,.20,.8],[.18,.65,.15])]
gl=b.n.new('CompositorNodeRLayers');gl.layer='Ghost';ink=gl.outputs['Image'];glow=b.mix(ink,(1.4,)*3+(1,),mode='MULTIPLY')
for sigma,gain in [(2,2.8),(7,3.5)]:glow=b.mix(glow,b.mix(b.blur(ink,sigma,W),(gain,)*3+(1,),mode='MULTIPLY'))
end=b.n.new('NodeGroupOutput');b.plug(b.combine([b.linear((a+z).clamp()) for a,z in zip(base,b.split(glow))]),end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB';s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'moth_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
