from pathlib import Path

out=Path(__file__).resolve().parent
script=(out.with_name('departure-discovery-v03')/'revise.py').read_text(encoding='utf-8')
# Advance existing revision plumbing in one pass, preserving the original V01 source.
for before,after in [('V53','V54'),('v53','v54'),('V52','V53'),('v52','v53'),('departure-v03-undocking','departure-v04-undocking'),('departure-discovery-v03/board','departure-discovery-v04/board')]:
    script=script.replace(before,after)
script=script.replace('exec-64cc12e5-3fc3-431f-bc1c-9a5d444eb127.png','exec-e84f2fc8-8059-422f-9490-aa9b313e0916.png').replace('attempts=2','attempts=1')
script=script.replace('Extra internal ring removed. Harper floats with bent knees; both complete shoes visible above the band. Ship and station framing retained. First attempt hid one shoe; second corrected it.','Larger head and torso scale restored from the user-preferred first floating draft; both knees tucked and shoes visible. Ship geometry retained.')
script=script.replace('with Harper visibly floating weightless inside','with Harper at the user-preferred larger scale, visibly floating weightless inside')
script=script.replace('V54 removes the invented interior ring and floats Harper with both feet fully visible; original ship reference preserved.','V54 restores larger floating Harper and marks this ship design as the continuity reference for future intro matching.')
script=script.replace('One equatorial band — Harper floating, both feet visible','SHIP CONTINUITY REFERENCE — larger floating Harper')
script=script.replace("shot['imagePrompt']=prompt", "shot['imagePrompt']=prompt\nshot['referenceRole']='Ship continuity reference for matching the intro; user-selected ship design, larger Harper adjustment pending review'\nregister.setdefault('continuityReferences',{})['personalSphereShip']={'id':'sphere-ship-continuity-v01','image':image,'geometrySource':'generated/storyboard/departure-discovery-v01/undocking.png','scaleSource':'generated/storyboard/departure-discovery-v04/larger-harper-scale-source.png','boardItemId':'departure-v04-undocking','userSelectedDesign':True,'useFor':'Match selected intro shots to the middle-sequence ship design when that revision is undertaken.','invariants':['Single outer equatorial band; no internal cockpit ring','One aft engine ring and entry port','Original upper/lower technical plates and transparent cyan-grid sphere','Larger adult Harper scale, floating rather than standing'],'scope':'Reference saved now; intro footage not revised in this turn.'}\nregister['departureDiscoverySequence']['shipContinuityReference']='sphere-ship-continuity-v01'")
script=script.replace("'\\nFrames 2665–2805; V54 still preview, review pending.'", "'\\nSHIP CONTINUITY REFERENCE: sphere-ship-continuity-v01. Use this design to match future intro revisions. Larger Harper scale restored.\\nFrames 2665–2805; V54 still preview, review pending.'")
(out/'revise.py').write_text(script,encoding='utf-8')
print('Prepared larger Harper and continuity reference registration')
