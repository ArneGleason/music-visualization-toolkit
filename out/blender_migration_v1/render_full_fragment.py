"""Render an exact, silent interval from the verified full Blender edit."""
import bpy,sys
args=sys.argv[sys.argv.index('--')+1:];a,z=map(int,args[:2]);s=bpy.data.scenes['RiversOfMars'];bpy.context.window.scene=s
s.frame_start=a+1;s.frame_end=z;s.render.ffmpeg.audio_codec='NONE';s.render.filepath=args[2]
bpy.ops.render.render(animation=True)
