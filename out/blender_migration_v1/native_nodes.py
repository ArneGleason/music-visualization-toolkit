"""Small native Blender math-node helpers; values remain procedural."""
import bpy
class Field:
    def __init__(self,b,value):self.b,self.v=b,value
    def __add__(self,x):return self.b.op('ADD',self,x)
    def __radd__(self,x):return self+x
    def __sub__(self,x):return self.b.op('SUBTRACT',self,x)
    def __rsub__(self,x):return self.b.op('SUBTRACT',x,self)
    def __mul__(self,x):return self.b.op('MULTIPLY',self,x)
    def __rmul__(self,x):return self*x
    def __truediv__(self,x):return self.b.op('DIVIDE',self,x)
    def __pow__(self,x):return self.b.op('POWER',self,x)
    def __neg__(self):return self*-1
    def clamp(self):return self.b.op('MINIMUM',1,self.b.op('MAXIMUM',0,self))
    def exp(self):return self.b.op('EXPONENT',self)
    def smooth(self):
        a=self.clamp();return a*a*(3-2*a)
class Builder:
    def __init__(self,tree):self.n,self.l=tree.nodes,tree.links
    def plug(self,value,socket):
        if isinstance(value,Field):value=value.v
        if isinstance(value,(int,float,tuple,list)):socket.default_value=value
        else:self.l.new(value,socket)
    def op(self,name,*values):
        n=self.n.new('ShaderNodeMath');n.operation=name
        for i,v in enumerate(values):self.plug(v,n.inputs[i])
        return Field(self,n.outputs[0])
    def animated(self,name,values):
        n=self.n.new('ShaderNodeValue');n.label=name
        for f,v in enumerate(values,1):n.outputs[0].default_value=float(v);n.outputs[0].keyframe_insert('default_value',frame=f)
        return Field(self,n.outputs[0])
    def display(self,v):
        gate=self.op('GREATER_THAN',v,.0031308)
        return v*12.92*(1-gate)+(1.055*v**(1/2.4)-.055)*gate
    def linear(self,v):
        gate=self.op('GREATER_THAN',v,.04045)
        return v/12.92*(1-gate)+((v+.055)/1.055)**2.4*gate
    def mix(self,a,b,factor=1,mode='ADD'):
        n=self.n.new('ShaderNodeMix');n.data_type='RGBA';n.blend_type=mode;n.clamp_result=False
        self.plug(factor,n.inputs[0]);self.plug(a,n.inputs[6]);self.plug(b,n.inputs[7]);return n.outputs[2]
    def blur(self,a,sigma,width):
        n=self.n.new('CompositorNodeBlur');n.inputs['Size'].default_value=(3*sigma*width/1280,)*2;self.plug(a,n.inputs['Image']);return n.outputs[0]
    def split(self,a,shader=False):
        n=self.n.new('ShaderNodeSeparateColor' if shader else 'CompositorNodeSeparateColor');self.plug(a,n.inputs[0]);return [Field(self,v) for v in list(n.outputs)[:3]]
    def combine(self,values):
        n=self.n.new('ShaderNodeCombineXYZ')
        for i,v in enumerate(values):self.plug(v,n.inputs[i])
        return n.outputs[0]
