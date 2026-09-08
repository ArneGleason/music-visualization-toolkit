"""Native vector geometry, stateful trails, tracked lamp and receiver contours."""
from pathlib import Path
O=Path(__file__).resolve().parent
exec(compile((O/'lights2_native.py').read_text().split("if family=='receiver':",1)[0],str(O/'lights2_native.py'),'exec'))
import gzip,numpy as np
s.cycles.samples=8; s.cycles.transparent_max_bounces=64
with gzip.open(D/'paths.json.gz','rt') as stream:geometry=json.load(stream)
def smooth(t):
    t=max(0,min(1,t)); return t*t*(3-2*t)
def pulse(sf):
    t=sf-1175; return 0 if t<0 else (1-math.exp(-t/1.1))*math.exp(-max(0,t-3)/12)
h=[[b.animated(f'Track inverse{i}{j}',[v['inverse'][i][j] for v in rows]) for j in range(3)] for i in range(2)]
tx=h[0][0]*x+h[0][1]*y+h[0][2]; ty=h[1][0]*x+h[1][1]*y+h[1][2]
inside=b.op('LESS_THAN',((tx-640)/163)**2+((ty-557)/153)**2,1)*b.op('LESS_THAN',ty,536)
active=b.animated('Receiver active',[int(v['receiver']) for v in rows]); mask=inside*active*((r-blue-.12)*4).clamp()
guardmix=b.animated('Release face protection',[smooth((v['song_frame']+.5-1082)/24) for v in rows])
for name,val in [('Lamp',mask),('Guard0',1-((x-345)/35).smooth()*(1-guardmix)),('Guard1',((x-900)/35).smooth()*(1-guardmix)+guardmix)]:
    av=s.view_layers[0].aovs.add(); av.name=name; av.type='VALUE'; node=b.n.new('ShaderNodeOutputAOV'); node.aov_name=name; b.plug(val,node.inputs['Value'])
em=b.n.new('ShaderNodeEmission'); em.inputs[0].default_value=(0,0,0,1); mo=b.n.new('ShaderNodeOutputMaterial'); b.plug(em.outputs[0],mo.inputs[0]); plane.location.z=-1
collections={}
for kind in ['sprite','hardware','burst']:
    collection=bpy.data.collections.new(kind); s.collection.children.link(collection); collections[kind]=collection
for fi,subs in enumerate(geometry):
    for sub,paths in enumerate(subs):
        for kind in collections:
            selected=[p for p in paths if p['kind']==kind]
            if not selected:continue
            verts=[]; faces=[]; colors=[]
            for path_index,path in enumerate(selected):
                points=np.array(path['xy']); energies=path['energy']; side=path['side']; n=len(points); width=path['width']
                color=np.array(([1,0,0] if side==0 else [0,1,0]) if kind=='sprite' else ([.2,.8,1] if side==0 else [1,.5,.1]))
                for j in range(n if path['closed'] else n-1):
                    a=points[j]; z=points[(j+1)%n]; delta=z-a; norm=max(np.linalg.norm(delta),1e-6); normal=np.array([-delta[1],delta[0]])/norm*width*.5
                    corners=[a+normal,z+normal,z-normal,a-normal]; index=len(verts)
                    # Distinct depth prevents coplanar complementary paths from
                    # dropping one another at the shared cabinet border.
                    depth=.012*(fi*2+sub)+path_index*.0005
                    verts.extend([((p[0]-640)/80,(360-p[1])/80,depth) for p in corners]); faces.append((index,index+1,index+2,index+3)); colors.extend([(*[float(c*energies[j]) for c in color],1)]*4)
            mesh=bpy.data.meshes.new(f'{kind} {fi+1}.{sub}'); mesh.from_pydata(verts,[],faces)
            attr=mesh.color_attributes.new(name='Energy',type='FLOAT_COLOR',domain='POINT'); attr.data.foreach_set('color',np.array(colors,dtype=np.float32).ravel())
            mat=bpy.data.materials.new(mesh.name); mat.use_nodes=True; mat.node_tree.nodes.clear(); nb=Builder(mat.node_tree)
            vc=nb.n.new('ShaderNodeVertexColor'); vc.layer_name='Energy'; em=nb.n.new('ShaderNodeEmission'); nb.plug(vc.outputs['Color'],em.inputs[0])
            life=12 if kind=='sprite' else 1
            for at in [0,fi]+list(range(fi+1,fi+life+2)):
                age=at-fi-1
                if 0<=age<life:
                    gain=(.465*.55**(2*age) if sub==0 else .3 if age==0 else .465*.55**(2*age-1)) if kind=='sprite' else .5
                else:gain=0
                em.inputs[1].default_value=gain; em.inputs[1].keyframe_insert('default_value',frame=at)
            transparent=nb.n.new('ShaderNodeBsdfTransparent'); add=nb.n.new('ShaderNodeAddShader'); nb.plug(em.outputs[0],add.inputs[0]); nb.plug(transparent.outputs[0],add.inputs[1]); mo=nb.n.new('ShaderNodeOutputMaterial'); nb.plug(add.outputs[0],mo.inputs[0]); mesh.materials.append(mat)
            ob=bpy.data.objects.new(mesh.name,mesh); collections[kind].objects.link(ob)
            for at,hidden in [(0,True),(fi,True),(fi+1,False),(fi+life+1,True)]:ob.hide_render=hidden; ob.keyframe_insert('hide_render',frame=at)
layernames={}
for k,kind in enumerate(collections):
    layer=s.view_layers[0] if k==0 else s.view_layers.new(kind); layer.name=kind; layernames[kind]=kind
    for other in collections:layer.layer_collection.children[other].exclude=other!=kind
tree=bpy.data.node_groups.new('Native stateful message composite','CompositorNodeTree'); tree.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor'); s.compositing_node_group=tree; b=Builder(tree)
plate=b.n.new('CompositorNodeImage'); plate.image=img; plate.frame_duration=count; plate.frame_start=1; plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale'); scale.inputs['Type'].default_value='Render Size'; b.plug(plate.outputs[0],scale.inputs['Image']); pic=scale.outputs[0]
rl={}
for kind in collections:rl[kind]=b.n.new('CompositorNodeRLayers'); rl[kind].layer=kind
mask=b.blur(rl['sprite'].outputs['Lamp'],1.4,W); strength=b.animated('Lead-vocal dial energy',[.035+2.8*v['voice'] if v['receiver'] else 0 for v in rows])
core=b.mix(b.mix(pic,mask,mode='MULTIPLY'),b.combine([strength*.65]*3),mode='MULTIPLY')
halo=b.mix(b.mix(b.blur(mask,10,W),(.18,.18,.18,1),mode='MULTIPLY'),b.mix(b.blur(mask,30,W),(.1,.1,.1,1),mode='MULTIPLY'))
lit=b.mix(b.mix(pic,core),b.mix(halo,b.combine([strength,strength*.46,strength*.1]),mode='MULTIPLY'))
lit=b.combine([b.display(v.clamp()) for v in b.split(lit)])
encoded=rl['sprite'].outputs['Image']; glow=None
for sigma,gain in [(.7,1.5),(math.sqrt(9+.49),1.8),(math.sqrt(121+.49),2.5)]:
    term=b.mix(b.blur(encoded,sigma,W),(gain,gain,gain,1),mode='MULTIPLY'); glow=term if glow is None else b.mix(glow,term)
left,right,_=b.split(glow); guard0=b.split(rl['sprite'].outputs['Guard0'])[0]; guard1=b.split(rl['sprite'].outputs['Guard1'])[0]
boost=b.animated('NOW sprite accent',[1+2.2*(pulse(v['song_frame']+.25)+pulse(v['song_frame']+.75))/2 for v in rows])
glow=b.combine([(left*guard0*a+right*guard1*z)*boost for a,z in zip([.2,.8,1],[1,.5,.1])])
for kind,coregain,settings in [('hardware',1.4,[(2,2),(7,2.5)]),('burst',1.7,[(3,3.5),(12,6)])]:
    layer=rl[kind].outputs['Image']; light=b.mix(layer,(coregain,)*3+(1,),mode='MULTIPLY')
    for sigma,gain in settings:light=b.mix(light,b.mix(b.blur(layer,sigma,W),(gain,)*3+(1,),mode='MULTIPLY'))
    glow=b.mix(glow,light)
result=b.combine([b.linear((a+z).clamp()) for a,z in zip(b.split(lit),b.split(glow))]); end=b.n.new('NodeGroupOutput'); b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG'; s.render.image_settings.color_mode='RGB'; s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'message_{W}.blend'))
for f in frames:s.frame_set(f); s.render.filepath=str(out/f'{f:04d}.png'); bpy.ops.render.render(write_still=True)
