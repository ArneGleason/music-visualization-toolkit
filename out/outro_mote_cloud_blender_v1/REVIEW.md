# Shot8: slower, denser, coherent clouds

900 motes (5x180), persistent throughout22frames, smooth rose-to-violet spatial color field so neighboring motes share colors. Only18% of the path toward artifact is traversed; there is no arrival or fade-out within the shot. Motion uses shape-key interpolation and half-frame shutter blur. No random per-particle color assignment.

New effect rendered in Blender5.2 Cycles (24samples) and composited additively in Blender's scene-linear compositor, with Fog Glow. Orthographic frame-space geometry and render-size plate scaling, saved as shot8.blend. This is an artistic2.5D layer, not recovered room geometry. No final mastering. 720p render; 1080p consistency test remains pending.

prepare.py extracts22 numbered base frames from the pre-atmosphere preview. build.py selects each source frame explicitly while rendering; use that script to reproduce the animation, since the saved blend's plate starts at frame1. finish.py only encodes/stitches the already-composited frames and copies the existing audio; it performs no effects compositing. Prior effects elsewhere remain baked previews until their separate Blender migration.

Timing unchanged: shot8 song[4622,4644), full review492frames at24fps. All other shots retained from outro_additive_green_v1. Missing lip sync in8 remains labelled. Previous short intake test is a spare, not this selection. Await owner review.

Creative Production source preservation: unchanged performance, background, edit and audio; this review revises only the requested atmosphere.
