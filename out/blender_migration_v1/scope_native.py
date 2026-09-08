"""Resolution-independent phosphor ribbons and original imperfect camera push."""
import sys,json,gzip,math,random
from pathlib import Path
import bpy,numpy as np
O=Path(__file__).resolve().parent;R=O.parents[1];D=O/'scope';sys.path.insert(0,str(O));sys.path.insert(0,str(R/'tools'))
from native_nodes import Builder,Field
import screen_sync_pilot as base
import screen_sync_refine as refined
import screen_sync_phosphor as old
args=sys.argv[sys.argv.index('--')+1:];W=int(args[0]);frames=list(map(int,args[1].split(','))) if len(args)>1 else list(range(1,70));dest=D/f'native_{W}';dest.mkdir(exist_ok=True)
s,co=base.setup('replacement');refined.textured_glass()
for obj in list(s.objects):
 if obj.type=='FONT' or obj.name.startswith(('Horizontal grid','Vertical grid','Grid tick')):bpy.data.objects.remove(obj,do_unlink=True)
s.render.engine='CYCLES';s.cycles.samples=8;s.cycles.transparent_max_bounces=512;s.render.film_transparent=True;s.frame_start=1;s.frame_end=69;s.render.resolution_x=W;s.render.resolution_y=W*9//16;co.data.clip_end=2000
# Reuse the authored peripheral calibration and scratches, omitting its raster dirt.
import inspect,textwrap
glass=textwrap.dedent(inspect.getsource(old.glass_details));glass='def native_marks():\n'+glass[glass.index('    dark ='):]
ns={'base':base,'np':np,'math':math};exec(glass,ns);ns['native_marks']()
for f in range(1,70):
 i=f-1;p=i/68;ease=p*p*(3-2*p);co.data.ortho_scale=(base.W/1.012)*(610/(base.W/1.012))**ease
 co.location.x=(base.CX-base.W/2)*ease;co.location.y=(base.H/2-base.CY)*ease
 dx,dy,roll,travel=old.rail_motion(i/24);co.location.x+=dx*co.data.ortho_scale;co.location.y+=dy*co.data.ortho_scale;co.rotation_euler.z=math.radians(roll);co.data.ortho_scale*=1+travel
 co.keyframe_insert('location',frame=f);co.keyframe_insert('rotation_euler',frame=f);co.data.keyframe_insert('ortho_scale',frame=f)
collections={}
for name in ['Base','Amber','Cyan']:
 c=bpy.data.collections.new(name);s.collection.children.link(c);collections[name]=c
for ob in list(s.collection.objects):
 if ob!=co:s.collection.objects.unlink(ob);collections['Base'].objects.link(ob)
# Base's original setup uses the default Collection too.
for c in list(s.collection.children):
 if c.name not in collections:
  for ob in list(c.objects):
   if ob!=co:c.objects.unlink(ob);collections['Base'].objects.link(ob)
s.view_layers[0].name='Base'
for name in ['Amber','Cyan']:s.view_layers.new(name)
for layer in s.view_layers:
 for name in collections:layer.layer_collection.children[name].exclude=name!=layer.name
with gzip.open(D/'paths.json.gz','rt') as f:records=json.load(f)
for rec in records:
 birth=rec['step']/8
 for channel,path in enumerate(rec['paths']):
  a=np.array(path);xy=a[:,:2];speed=1/np.maximum((a[:,2]-.5)/1.08,.02)
  if channel==0:norm=np.column_stack([np.zeros(len(xy)),speed])
  else:norm=xy/np.maximum(np.linalg.norm(xy,axis=1)[:,None],1)*speed[:,None]
  verts=[];colors=[];faces=[]
  # Gaussian normal distance is a shader attribute, not a pixel-width image.
  for j,(point,normal,sigma,energy) in enumerate(zip(xy,norm,a[:,2],a[:,3])):
   for sign in [-1,1]:
    q=point+normal*sign*12;verts.append(base.point(base.CX+q[0],base.CY-q[1],.18+birth*.001));colors.append((sign*12,sigma,energy,1))
  for j in range(len(xy)-1):faces.append((2*j,2*j+1,2*j+3,2*j+2))
  me=bpy.data.meshes.new(f'Beam {channel} {birth}');me.from_pydata(verts,[],faces);at=me.attributes.new('Beam distance','FLOAT_VECTOR','POINT');at.data.foreach_set('vector',np.array(colors,dtype=np.float32)[:,:3].ravel())
  ob=bpy.data.objects.new(me.name,me);collections[['Amber','Cyan'][channel]].objects.link(ob)
  m=bpy.data.materials.new(me.name);m.use_nodes=True;m.node_tree.nodes.clear();b=Builder(m.node_tree);attr=b.n.new('ShaderNodeAttribute');attr.attribute_name='Beam distance';sep=b.n.new('ShaderNodeSeparateXYZ');b.plug(attr.outputs['Vector'],sep.inputs[0]);distance=Field(b,sep.outputs[0]);sigma=Field(b,sep.outputs[1]);energy=Field(b,sep.outputs[2]);dwell=((sigma-.5)/1.08).clamp()
  intensity=(-(distance/sigma)**2*.5).exp()*energy+(.21*(-(distance/(2.8+2.4*dwell))**2*.5).exp()+.045*(-(distance/9)**2*.5).exp())*dwell**1.5
  coord=b.n.new('ShaderNodeNewGeometry');ps=b.n.new('ShaderNodeSeparateXYZ');b.plug(coord.outputs['Position'],ps.inputs[0]);rx=(Field(b,ps.outputs[0])-(base.CX-base.W/2))/base.RX;ry=(Field(b,ps.outputs[1])-(base.H/2-base.CY))/base.RY;mask=((.990-(rx*rx+ry*ry)**.5)/.018).smooth()
  gains=[]
  for f in range(1,70):
   age=f-1-birth
   if age<-.99:g=0
   elif age<0:g=.70/4+.95*(1-math.exp(-math.log(2)/(.030*24*4)))/4+.30*(1-math.exp(-math.log(2)/(.160*24*4)))/4
   else:g=(.95*(1-math.exp(-math.log(2)/(.030*24*4)))*math.exp(-math.log(2)*age/(.030*24))+.30*(1-math.exp(-math.log(2)/(.160*24*4)))*math.exp(-math.log(2)*age/(.160*24)))/4
   if age>24:g=0
   p=(f-1)/68;g*=1+.2*p*p*(3-2*p);gains.append(g)
  gain=b.animated('Finite phosphor exposure',gains);em=b.n.new('ShaderNodeEmission');b.plug(intensity*mask*gain,em.inputs[0]);clear=b.n.new('ShaderNodeBsdfTransparent');add=b.n.new('ShaderNodeAddShader');b.plug(clear.outputs[0],add.inputs[0]);b.plug(em.outputs[0],add.inputs[1]);out=b.n.new('ShaderNodeOutputMaterial');b.plug(add.outputs[0],out.inputs[0]);me.materials.append(m)
  for f,value in [(1,True),(max(1,int(birth)+1),False),(min(70,int(birth)+26),True)]:ob.hide_render=value;ob.keyframe_insert('hide_render',frame=f)
t=bpy.data.node_groups.new('Native phosphor optical integration','CompositorNodeTree');t.interface.new_socket(name='Image',in_out='OUTPUT',socket_type='NodeSocketColor');s.compositing_node_group=t;b=Builder(t)
layers={}
for name in collections:n=b.n.new('CompositorNodeRLayers');n.layer=name;layers[name]=n
amber=b.split(layers['Amber'].outputs['Image'])[0];cyan=b.split(b.blur(layers['Cyan'].outputs['Image'],4.96,W))[0]
rgb=[amber*a+cyan*c for a,c in zip([1,.43,.075],[.065,.40,.38])];rgb=[v/(1+v*.25) for v in rgb]
out=b.n.new('NodeGroupOutput');b.plug(b.mix(layers['Base'].outputs['Image'],b.combine(rgb)),out.inputs['Image'])
s.render.engine='BLENDER_EEVEE'
for material in bpy.data.materials:material.surface_render_method='BLENDED'
s.frame_set(1);bpy.ops.wm.save_as_mainfile(filepath=str(D/f'scope_{W}.blend'))
for f in frames:s.frame_set(f);s.render.filepath=str(dest/f'{f:04d}.png');bpy.ops.render.render(write_still=True)
