import bpy,json
s=bpy.context.scene
print('SETTINGS',s.render.resolution_x,s.render.resolution_y,s.render.fps)
for st in s.sequence_editor.strips:
 if st.frame_final_start<361:
  print(json.dumps({'name':st.name,'type':st.type,'ch':st.channel,'a':st.frame_final_start,'b':st.frame_final_end,'text':getattr(st,'text',None),'size':getattr(st,'font_size',None),'xy':[st.transform.offset_x,st.transform.offset_y] if hasattr(st,'transform') else None,'loc':list(st.location) if hasattr(st,'location') else None,'keys':list(st.keys())}))
