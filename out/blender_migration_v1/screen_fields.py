"""Injected into the native mask shader before geometry setup."""
display_image=bpy.data.images.load(str(D/'screen_plates/0001.png')); display_image.source='SEQUENCE'
sf=b.animated('Screen song frame',[v['song_frame'] for v in rows])
centerx=b.animated('Tracked screen X',[v['transform'][0][0]*628+v['transform'][0][1]*260+v['transform'][0][2] for v in rows])
centery=b.animated('Tracked screen Y',[v['transform'][1][0]*628+v['transform'][1][1]*260+v['transform'][1][2] for v in rows])
radius=b.animated('Tracked screen radius',[99*v['transform'][0][0] for v in rows])
growth=((sf-1246)/12).smooth(); alpha=((sf-1201)/12).smooth()
grown_radius=radius+(820-radius)*growth
grown_x=centerx*(1-growth)+640*growth; grown_y=centery*(1-growth)+360*growth
smallmask=((radius-((x-centerx)**2+(y-centery)**2)**.5)/2).clamp()*alpha
largemask=((grown_radius-((x-grown_x)**2+(y-grown_y)**2)**.5)/3).clamp()*b.op('GREATER_THAN',sf,1246)
def reflection(v,last):return last-b.op('ABSOLUTE',b.op('FLOORED_MODULO',v,2*last)-last)
def image_at(px,py,reflect=False):
    if reflect:px=reflection(px,1279); py=reflection(py,719)
    node=b.n.new('ShaderNodeTexImage'); node.image=display_image; node.interpolation='Cubic'; node.extension='EXTEND'
    node.image_user.frame_duration=103; node.image_user.frame_start=13; node.image_user.use_auto_refresh=True
    b.plug(b.combine([(380+px*520/1280)/1280,1-(100+py*520/720)/720,0]),node.inputs['Vector'])
    return node.outputs['Color']
for name,color in [('ScreenFull',image_at(x,y)),('ScreenSmall',image_at((x-centerx+radius)*1280/(2*radius),(y-centery+radius)*720/(2*radius))),('ScreenExpanded',image_at((x-grown_x+grown_radius)*1280/(2*grown_radius),(y-grown_y+grown_radius)*720/(2*grown_radius),True))]:
    av=s.view_layers[0].aovs.add(); av.name=name; av.type='COLOR'; node=b.n.new('ShaderNodeOutputAOV'); node.aov_name=name; b.plug(color,node.inputs['Color'])
for name,value in [('ScreenMask',smallmask),('ExpandedMask',largemask)]:
    av=s.view_layers[0].aovs.add(); av.name=name; av.type='VALUE'; node=b.n.new('ShaderNodeOutputAOV'); node.aov_name=name; b.plug(value,node.inputs['Value'])
