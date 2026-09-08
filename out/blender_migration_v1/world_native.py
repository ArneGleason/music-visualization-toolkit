"""Native silhouette departure, procedural sphere/space, orbital message trails."""
import bpy,sys,math,ast
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parents[1];sys.path.insert(0,str(O))
from native_nodes import Builder,Field
args=sys.argv[sys.argv.index('--')+1:];W=int(args[0]);D=O/'world';D.mkdir(exist_ok=True)
dest=D/f'native_{W}';dest.mkdir(exist_ok=True);song=list(range(2122,2233))
def smooth(t):t=max(0,min(1,t));return t*t*(3-2*t)
def rad(sf):return math.exp(math.log(1600)*(1-smooth((sf-2128)/21))+math.log(210)*smooth((sf-2128)/21))*(1-.035*smooth((sf-2199)/34))
bpy.ops.wm.read_factory_settings(use_empty=True);s=bpy.context.scene
s.render.engine='BLENDER_EEVEE';s.render.resolution_x=W;s.render.resolution_y=W*9//16;s.render.resolution_percentage=100
s.render.fps=24;s.frame_start=1;s.frame_end=111;s.render.film_transparent=True
s.view_settings.view_transform='Standard';s.view_settings.look='None';s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGB'
cam=bpy.data.cameras.new('Orthographic reveal');co=bpy.data.objects.new('Camera',cam);s.collection.objects.link(co);co.location=(0,0,10);cam.type='ORTHO';cam.ortho_scale=16;s.camera=co
collections={}
for name in ['World','Subject','Signals']:
 c=bpy.data.collections.new(name);s.collection.children.link(c);collections[name]=c
def mesh(name,verts,faces,collection):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();ob=bpy.data.objects.new(name,me);collections[collection].objects.link(ob);return ob
def material(ob,name):
 m=bpy.data.materials.new(name);m.use_nodes=True;m.node_tree.nodes.clear();ob.data.materials.append(m);return Builder(m.node_tree)
def emission(b,color):
 e=b.n.new('ShaderNodeEmission');b.plug(color,e.inputs[0]);out=b.n.new('ShaderNodeOutputMaterial');b.plug(e.outputs[0],out.inputs[0])
def image(b,file,coords):
 n=b.n.new('ShaderNodeTexImage');n.image=bpy.data.images.get(file) or bpy.data.images.load(str(R/file));n.image.name=file;n.extension='EXTEND';b.plug(coords,n.inputs[0]);return [b.display(v) for v in b.split(n.outputs['Color'],True)]
plane=mesh('Procedural world field',[(-8,-4.5,0),(8,-4.5,0),(8,4.5,0),(-8,4.5,0)],[(0,1,2,3)],'World')
uv=plane.data.uv_layers.new()
for loop,v in zip(uv.data,[(0,0),(1,0),(1,1),(0,1)]):loop.uv=v
b=material(plane,'Sphere, source garden and procedural nebula')
uvn=b.n.new('ShaderNodeTexCoord');sp=b.n.new('ShaderNodeSeparateXYZ');b.plug(uvn.outputs['UV'],sp.inputs[0]);u=Field(b,sp.outputs[0]);v=Field(b,sp.outputs[1]);x=u*1280;y=(1-v)*720
radius=b.animated('Approved globe radius',[rad(sf) for sf in song]);nx=(x-640)/radius;ny=(y-324)/radius
rr=(nx*nx+ny*ny)**.5;nz=b.op('MAXIMUM',0,1-nx*nx-ny*ny)**.5
lon=b.op('ARCTAN2',nx,b.op('MAXIMUM',nz,.001));lat=b.op('ARCSINE',b.op('MINIMUM',1,b.op('MAXIMUM',-1,ny)))
spin=b.animated('Late surface drift',[max(0,sf-2199)*.0006 for sf in song])
surface=image(b,'codex/out/signal_crossing_space_a.jpg',b.combine([(1060+(lon/math.pi+.5+spin)*475)/1536,1-(320+(lat/math.pi+.5)*694)/1024,0]))
shade=.34+.82*(-.4*nx-.28*ny+.82*nz).clamp();mask=((1-rr)*radius).clamp();rim=(-((rr-1)*radius/7)**2).exp()*.38
def noise(seed,scale):
 n=b.n.new('ShaderNodeTexNoise');n.noise_dimensions='4D';n.inputs['W'].default_value=seed;n.inputs['Scale'].default_value=scale;n.inputs['Detail'].default_value=3.4;n.inputs['Roughness'].default_value=.52
 b.plug(b.combine([u*1.78,v,0]),n.inputs['Vector']);return Field(b,n.outputs['Fac'])
n1,n2,n3=noise(27.4,5),noise(9.12,4.3),noise(73.2,6.2)
diagonal=y-(570-.38*x+100*(n2-.5));band=(-(diagonal/145)**2).exp()
filament=b.op('MAXIMUM',0,n1-.24)**1.6;dust=(-((diagonal+20+90*(n3-.5))/28)**2).exp()*.72
center=1-.62*(-(((x-640)/320)**2+((y-324)/260)**2)).exp();density=band*filament*(1-dust)*center
blend=(x/1280*.75+n2*.4).clamp();patch=(-(((x-1080)/240)**2+((y-110)/135)**2)).exp()*b.op('MAXIMUM',0,n3-.28)
# Native Voronoi nuclei, softened at subpixel scale by Eevee sampling.
vn=b.n.new('ShaderNodeTexVoronoi');vn.distance='EUCLIDEAN';vn.inputs['Scale'].default_value=44;b.plug(b.combine([u*1.78,v,0]),vn.inputs['Vector'])
star=(-((Field(b,vn.outputs['Distance']))/.030)**2).exp()*(.10+.32*band)
space=[base+density*(a*(1-blend)+z*blend)*3.4+patch*p*.35+star for base,a,z,p in zip([.021,.016,.026],[.47,.28,.64],[.17,.43,.47],[.28,.20,.14])]
planet=[c**.91*shade*1.12 for c in surface];pic=[a*(1-mask)+z*mask+rim*c for a,z,c in zip(space,planet,[.16,.38,.62])]
garden=image(b,'codex/out/forest_walk_track_b.jpg',b.combine([u,1-((y+66)/853),0]))
fade=b.animated('Early garden dissolve',[(sf-2125)/6 for sf in song]);irregular=.5+.16*b.op('SINE',x*.013+y*.009)+.13*b.op('SINE',y*.025-x*.017)
ga=1-(fade+irregular*.26).smooth();pic=[a*(1-ga)+z*ga for a,z in zip(pic,garden)]
haze=b.animated('Optical reveal haze',[math.exp(-((sf-2136)/3)**2)*.13 for sf in song])*(-(((x-640)/420)**2+((y-324)/260)**2)).exp()
emission(b,b.combine([b.linear((a+haze*c).clamp()) for a,c in zip(pic,[.9,.85,.65])]))
av=s.view_layers[0].aovs.add();av.name='GardenAlpha';av.type='VALUE';ao=b.n.new('ShaderNodeOutputAOV');ao.aov_name='GardenAlpha';b.plug(ga,ao.inputs['Value'])
# The approved authored silhouette is mesh geometry, not a raster matte input.
text=(R/'out/world_pullback_refined_v2/render.py').read_text();outline=ast.literal_eval(text.split('outline=np.array(',1)[1].split(',np.int32)',1)[0])
lantern=[(550+23*math.cos(i*math.tau/64),510+46*math.sin(i*math.tau/64)) for i in range(64)]
for name,points in [('Woman silhouette',outline),('Carried lantern',lantern)]:
 ob=mesh(name,[((px-640)/80,(324-py)/80,0) for px,py in points],[tuple(range(len(points)))],'Subject');uv=ob.data.uv_layers.new()
 for loop in ob.data.loops:
  px,py=points[loop.vertex_index];uv.data[loop.index].uv=(px/1280,1-(py+66)/853)
 bb=material(ob,name+' original image');un=bb.n.new('ShaderNodeTexCoord');tex=bb.n.new('ShaderNodeTexImage');tex.image=bpy.data.images['codex/out/forest_walk_track_b.jpg'];bb.plug(un.outputs['UV'],tex.inputs[0]);emission(bb,tex.outputs['Color'])
 ob.location=(0,.45,0)
 for f,sf in enumerate(song,1):
  scale=math.exp(-3.7*smooth((sf-2126)/17));ob.scale=(scale,scale,1);ob.keyframe_insert('scale',frame=f)
# Native per-frame line meshes retain exact source choreography and back-half occlusion.
signal_material=bpy.data.materials.new('Message light vertex energy');signal_material.use_nodes=True;bb=Builder(signal_material.node_tree);bb.n.clear()
attr=bb.n.new('ShaderNodeVertexColor');attr.layer_name='energy';emission(bb,attr.outputs['Color'])
for f,sf in enumerate(song,1):
 verts=[];faces=[];colors=[]
 def line(p,q,color,width=2):
  dx=q[0]-p[0];dy=q[1]-p[1];length=math.hypot(dx,dy)
  if length<.001:return
  ox=-dy/length*width/2;oy=dx/length*width/2;k=len(verts)
  for px,py in [(p[0]+ox,p[1]+oy),(p[0]-ox,p[1]-oy),(q[0]-ox,q[1]-oy),(q[0]+ox,q[1]+oy)]:verts.append(((px-640)/80,(360-py)/80,0))
  faces.append((k,k+1,k+2,k+3));colors.extend([(*color,1)]*4)
 for entry,color,tilt in [(2149,(1,.70,.25),-.25),(2157,(.30,.85,1),.35)]:
  amount=smooth((sf-entry)/6)*(1-smooth((sf-2173)/22))
  if amount<=0:continue
  def point(theta):return (640+300*math.cos(theta)*math.cos(tilt)-98*math.sin(theta)*math.sin(tilt),324+300*math.cos(theta)*math.sin(tilt)+98*math.sin(theta)*math.cos(tilt))
  for j in range(499):
   theta=j*math.tau/499;p=point(theta);q=point((j+1)*math.tau/499)
   if math.sin(theta)<0 and (p[0]-640)**2+(p[1]-324)**2<rad(sf)**2:continue
   strength=(.34+1.3*math.exp(-(((sf-entry)*.14-theta)%math.tau)/1.1))*amount;line(p,q,[c*strength for c in color])
 for entry,landing,p0,p1,target,color in [(2147,2161,(-60,95),(260,30),(-.4,-.25),(1,.72,.28)),(2155,2170,(1340,195),(1010,65),(.42,.12),(.35,.85,1))]:
  if sf<entry:continue
  end=(640+210*target[0],324+210*target[1])
  def point(t):return tuple((1-t)**2*p0[k]+2*t*(1-t)*p1[k]+t*t*end[k] for k in range(2))
  if sf<=landing:
   progress=max(0,min(1,(sf-entry)/(landing-entry)))
   for j in range(24):
    t=max(0,progress-j*.011);line(point(t),point(max(0,t-.011)),[c*1.65*math.exp(-j/7) for c in color])
   p=point(progress);line((p[0]-2,p[1]),(p[0]+2,p[1]),[c*1.7 for c in color],6)
  if landing<=sf<landing+13:
   age=sf-landing
   def ring(t):
    xx=(5+age*2)*math.cos(t);yy=(3+age)*math.sin(t);a=-20*math.pi/180
    return (end[0]+xx*math.cos(a)-yy*math.sin(a),end[1]+xx*math.sin(a)+yy*math.cos(a))
   for j in range(64):line(ring(j*math.tau/64),ring((j+1)*math.tau/64),[c*.65*(1-age/13) for c in color],1)
 if not verts:continue
 ob=mesh(f'Message geometry {sf}',verts,faces,'Signals');ob.data.materials.append(signal_material);attribute=ob.data.color_attributes.new(name='energy',type='FLOAT_COLOR',domain='CORNER');attribute.data.foreach_set('color',[v for c in colors for v in c])
 for at,hidden in [(0,True),(f,False),(f+1,True)]:ob.hide_render=hidden;ob.keyframe_insert('hide_render',frame=at)
layers={}
for i,name in enumerate(collections):
 layer=s.view_layers[0] if i==0 else s.view_layers.new(name);layer.name=name;layers[name]=layer
 for child in layer.layer_collection.children:child.exclude=child.name!=name
t=bpy.data.node_groups.new('Native reveal composite','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
rl={}
for name in collections:n=b.n.new('CompositorNodeRLayers');n.layer=name;rl[name]=n
world=[b.display(v) for v in b.split(rl['World'].outputs['Image'])]
subject=[b.display(v) for v in b.split(rl['Subject'].outputs['Image'])]
alpha=Field(b,rl['Subject'].outputs['Alpha'])*b.animated('Figure disappears',[1-smooth((sf-2137)/7) for sf in song])*(1-Field(b,rl['World'].outputs['GardenAlpha']))
pic=[a*(1-alpha)+z*alpha for a,z in zip(world,subject)]
light=rl['Signals'].outputs['Image'];glow=b.mix(b.mix(light,(1.15,1.15,1.15,1),mode='MULTIPLY'),b.mix(b.blur(light,5,W),(1.7,1.7,1.7,1),mode='MULTIPLY'));glow=b.mix(glow,b.mix(b.blur(light,17,W),(1.05,1.05,1.05,1),mode='MULTIPLY'))
out=b.n.new('NodeGroupOutput');b.plug(b.combine([b.linear((a+z).clamp()) for a,z in zip(pic,b.split(glow))]),out.inputs['Image'])
s.frame_set(1);s.render.filepath=str(dest/'0001.png');bpy.ops.wm.save_as_mainfile(filepath=str(D/f'world_{W}.blend'))
selected=list(map(int,args[1].split(','))) if len(args)>1 else range(1,112)
for f in selected:s.frame_set(f);s.render.filepath=str(dest/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
