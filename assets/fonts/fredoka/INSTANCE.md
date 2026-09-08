# Flat lyric weight

Fredoka-Bold.ttf is a static instance of the adjacent OFL-licensed variable
font, with wght=700 and wdth=100. It replaces synthetic outline thickening
in the flat lyric renderer. No change to lyric timing or animation.

Reproduce from the repository root with fontTools installed:

```powershell
python -m fontTools.varLib.instancer "assets/fonts/fredoka/Fredoka[wdth,wght].ttf" wght=700 wdth=100 --output "assets/fonts/fredoka/Fredoka-Bold.ttf"
```

Blender's curve.offset=0.018 created pointed self-intersections above lowercase
m and r and inside uppercase M at the actual 66% caption size. Native weight
with zero offset removes those points before mesh conversion and deformation.
The real weight is slightly different in dimensions, so geometry-based layout
is measured anew. Keep the existing tracking, type_scale and musical animation.
