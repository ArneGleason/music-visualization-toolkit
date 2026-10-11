"""Create an independent stronger variant; V57 remains a complete fallback."""
from pathlib import Path

OUT=Path(__file__).resolve().parent
old=OUT.with_name('departure-discovery-motion-v03')
text=(old/'build_zoom_overlap.py').read_text(encoding='utf-8')
text=text.replace("'v57'","'v58'").replace('V57','V58').replace('?v=v57','?v=v58')
text=text.replace("'v56'","'v57'").replace('motion-v56.mp4','motion-v57.mp4')
text=text.replace("OLD = OUT.with_name('departure-discovery-motion-v02')","OLD = OUT.with_name('departure-discovery-motion-v03')")
text=text.replace("[(1.08,2.0,.48)] if count==1 else [(1.04,1.75,.62),(1.75,2.8,.24)]",
                  "[(1.08,2.45,.60)] if count==1 else [(1.04,2.15,.74),(2.15,3.4,.34)]")
text=text.replace("(NATIVE/'zoom-stills.mp4').as_posix(),(OUT/'zoom-overlap.mp4').as_posix()",
                  "(OLD/'zoom-overlap.mp4').as_posix(),(OUT/'zoom-overlap.mp4').as_posix()")
text=text.replace("assert 'zoom-stills.mp4' not in concat", "concat=concat.replace((OUT.with_name('departure-discovery-motion-v02')/'departure-reversed-clean.mp4').as_posix(),(OUT/'departure-pullout-twinkle.mp4').as_posix())\n    assert 'departure-reversed-clean.mp4' not in concat")
text=text.replace('V56 departure and all other shot selections retained', 'Blender departure pullout and cyan twinkle added; V57 preserved as fallback')
text=text.replace('Eight brief radial zoom overlaps connect nine static magnification views','Stronger optical zoom overlaps plus Blender departure pullout and cyan twinkle')
text=text.replace('V58: outgoing image expands into a radial blur over each incoming still.', 'V58: stronger outgoing radial blur over each incoming still; longer trails and greater opacity than V57.')
text=text.replace('departure-discovery-motion-v03/', 'departure-discovery-motion-v04/')
text=text.replace("print('V58 assembled; master audio verified; no new credits.')", "print('V58 assembled; master audio verified; no new credits. Run finish.py to register Blender departure metadata.')")
(OUT/'build_zoom_overlap.py').write_text(text,encoding='utf-8')
(OUT/'verify_frames.py').write_text((old/'verify_frames.py').read_text(),encoding='utf-8')
print('Independent stronger V58 builder prepared; V57 untouched.')
