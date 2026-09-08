"""Receiver and specimen light recipes, rendered/composited entirely in Blender."""
from pathlib import Path
import bpy,sys,json,math
O=Path(__file__).resolve().parent;sys.path.insert(0,str(O))
from native_nodes import Builder,Field
args=sys.argv[sys.argv.index('--')+1:];family=args[0];W=int(args[1])
D=O/family;data=json.loads((D/'controls.json').read_text());rows=data['frames'];count=len(rows)
frames=list(map(int,args[2].split(','))) if len(args)>2 else list(range(1,count+1))
out=D/f'native_{W}';out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=8
s.render.resolution_x=W;s.render.resolution_y=W*9//16;s.render.resolution_percentage=100;s.render.fps=24;s.frame_start=1;s.frame_end=count
s.view_settings.view_transform='Standard';s.view_settings.look='None'
s.world=bpy.data.worlds.new('Black');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
cam=bpy.data.cameras.new('Normalized camera');co=bpy.data.objects.new('Camera',cam);s.collection.objects.link(co);co.location=(0,0,10);cam.type='ORTHO';cam.ortho_scale=16;s.camera=co
bpy.ops.mesh.primitive_plane_add(size=2);plane=bpy.context.object;plane.scale=(8,4.5,1)
m=bpy.data.materials.new('Native source mask');m.use_nodes=True;plane.data.materials.append(m);m.node_tree.nodes.clear();b=Builder(m.node_tree)
uv=b.n.new('ShaderNodeTexCoord');sep=b.n.new('ShaderNodeSeparateXYZ');b.plug(uv.outputs['UV'],sep.inputs[0]);x=Field(b,sep.outputs[0])*1280;y=(1-Field(b,sep.outputs[1]))*720
img=bpy.data.images.load(str(D/'plates/0001.png'));img.source='SEQUENCE'
tex=b.n.new('ShaderNodeTexImage');tex.image=img;tex.image_user.frame_duration=count;tex.image_user.frame_start=1;tex.image_user.use_auto_refresh=True;b.plug(uv.outputs['UV'],tex.inputs['Vector'])
r,g,blue=[b.display(v) for v in b.split(tex.outputs['Color'],True)]
if family=='receiver':
    h=[[b.animated(f'Inverse H {i},{j}',[v['inverse'][i][j] for v in rows]) for j in range(3)] for i in range(3)]
    den=h[2][0]*x+h[2][1]*y+h[2][2]
    tx=(h[0][0]*x+h[0][1]*y+h[0][2])/den;ty=(h[1][0]*x+h[1][1]*y+h[1][2])/den
    ellipse=((tx-621)/155)**2+((ty-557)/149)**2
    aperture=b.op('LESS_THAN',ellipse,1)*b.op('LESS_THAN',ty,536)
    signal=aperture*((r-blue-.12)*4).clamp()
else:
    roi=(-(((x-829)/74)**6+((y-239)/93)**6)).exp()
    warm=((g-blue-.035)*12).clamp()*((r-blue-.09)*9).clamp()*((g-.48)*5).clamp()*(1-((r-g-.19)/.09).smooth())*roi
    hi=b.op('MAXIMUM',r,b.op('MAXIMUM',g,blue));lo=b.op('MINIMUM',r,b.op('MINIMUM',g,blue))
    visible=1-(1-((hi-lo-.035)/.065).smooth())*((y-265)/30).smooth()*((g-.27)/.12).smooth()
    cx=b.animated('Visible prop centroid X',[v['cx'] for v in rows]);cy=b.animated('Visible prop centroid Y',[v['cy'] for v in rows])
    phase=b.animated('Circulating highlight',[(v['song_frame']-2065)*.24 for v in rows])
    theta=b.op('ARCTAN2',y-cy,x-cx);sweep=(-b.op('FLOORED_MODULO',phase-theta,math.tau)/.85).exp()
    def sm(t):t=max(0,min(1,t));return t*t*(3-2*t)
    acquired=b.animated('Acquisition',[sm((v['song_frame']-2062)/8) for v in rows])
    levels=[]
    for v in rows:
        sf=v['song_frame'];a=sm((sf-2062)/8);e=v['vocal_envelope']
        levels.append((.13+.42*e+a*(.30+1.05*e)+math.exp(-((sf-2087)/5)**2)*.45)*(1-.38*sm((sf-2111)/10)))
    gain=b.animated('Vocal response / discovery accent',levels)
    signal=warm*visible*gain*(.6+acquired*.8*sweep)
    confinement=(-(((x-829)/84)**6+((y-239)/104)**6)).exp()*visible
    aov=s.view_layers[0].aovs.add();aov.name='Confinement';aov.type='VALUE'
    node=b.n.new('ShaderNodeOutputAOV');node.aov_name='Confinement';b.plug(confinement,node.inputs['Value'])
em=b.n.new('ShaderNodeEmission');b.plug(signal,em.inputs[0]);mo=b.n.new('ShaderNodeOutputMaterial');b.plug(em.outputs[0],mo.inputs[0])
t=bpy.data.node_groups.new('Native light composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
plate=b.n.new('CompositorNodeImage');plate.image=img;plate.frame_duration=count;plate.frame_start=1;plate.use_auto_refresh=True
scale=b.n.new('CompositorNodeScale');scale.inputs['Type'].default_value='Render Size';b.plug(plate.outputs[0],scale.inputs['Image']);pic=scale.outputs[0]
rl=b.n.new('CompositorNodeRLayers');mask=b.blur(rl.outputs['Image'],1.4 if family=='receiver' else .8,W)
if family=='receiver':
    strength=b.animated('Verified lead vocal strength',[v['strength'] for v in rows])
    core=b.mix(b.mix(pic,mask,mode='MULTIPLY'),(.65,.65,.65,1),mode='MULTIPLY')
    halo=b.mix(b.mix(b.blur(mask,10,W),(.18,.18,.18,1),mode='MULTIPLY'),b.mix(b.blur(mask,30,W),(.10,.10,.10,1),mode='MULTIPLY'))
    light=b.mix(core,b.mix(halo,(1,.46,.10,1),mode='MULTIPLY'))
    result=b.mix(pic,b.mix(light,b.combine([strength]*3),mode='MULTIPLY'))
else:
    core=b.mix(mask,(1,.62,.18,1),mode='MULTIPLY')
    bloom=b.mix(b.mix(b.blur(core,4,W),(.9,.9,.9,1),mode='MULTIPLY'),b.mix(b.blur(core,11,W),(.65,.65,.65,1),mode='MULTIPLY'))
    emitted=b.mix(b.mix(core,bloom),rl.outputs['Confinement'],mode='MULTIPLY')
    source=[b.display(v) for v in b.split(pic)];light=b.split(emitted)
    result=b.combine([b.linear((a+(1-a)*(1-(-e*1.25).exp())).clamp()) for a,e in zip(source,light)])
end=b.n.new('NodeGroupOutput');b.plug(result,end.inputs['Image'])
s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
s.render.filepath=str(out)+'/'
bpy.ops.wm.save_as_mainfile(filepath=str(D/f'{family}_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(out/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
