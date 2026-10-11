"""Record the accepted job and adapt the existing frame-preserving motion handoff."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
path=PROJECT/'kling-escape-approach-v01.json'
plan=json.loads(path.read_text(encoding='utf-8'))
sid=plan['shots'][0]['id']
job=json.loads((PROJECT/plan['output']/sid/'submission.json').read_text(encoding='utf-8'))['body']
plan.update(status='One requested escape-approach take accepted; awaiting collection and QA',actualSubmittedCredits=job['creditsConsumed'],generationId=job['generationId'])
path.write_text(json.dumps(plan,indent=2)+'\n',encoding='utf-8')
source=(PROJECT/'generated/storyboard/robot-ship-so-bright-v01/register_motion.py').read_text(encoding='utf-8')
source=source.replace('kling-robot-ship-so-bright-v01.json','kling-escape-approach-v01.json')
source=source.replace("default=37","default=25")
source=source.replace("=='robot-ship-so-bright-v01'","=='escape-approach-v01'")
source=source.replace('robot-ship-so-bright-motion-v01','escape-approach-motion-v01')
source=source.replace('storyboard-robot-ship-so-bright-v01.json','storyboard-escape-approach-v01.json')
source=source.replace('selected-motion-v34.mp4','selected-motion-v36.mp4')
source=source.replace('Original robot headquarters ship restored; So bright is now a native no-streak Kling replacement.',
    'So bright now intercuts native Harper movement toward the escape hatch, amid the original robot ship exteriors.')
source=source.replace('Kling / Blender / original robot ship with revised So bright motion',
    'Kling / Blender / native Harper escape approach')
source=source.replace('V35 keeps the restored original robot ship exteriors and five lab takes; only So bright changes from the staged still to its approved 48-credit native replacement. Exact phrase grid, fades, schematic dissolve and original master audio retained.',
    'V37 keeps eight prior native lab/ark takes; only So bright changes to native Harper escape-approach motion. Bright night remains the exterior pause; pod departure is planned at1958after Bright night with design undecided. Exact phrase grid, fades, schematic dissolve and original master audio retained.')
source=source.replace('All nine lab/ark shots animated; redesigned So bright native replacement, user playback pending',
    'All nine lab/ark shots animated; So bright is an escape setup, user playback pending')
source=source.replace('Approved 48-credit replacement completed and collected; agent QA passed; user playback pending',
    'Requested 48-credit escape-approach take completed and collected; agent QA passed; user playback pending')
source=source.replace("project['production']['labVerseReview']=spec['reviewUrl']",
    "project['production']['labVerseReview']=spec['reviewUrl']\nproject['production']['escapeSetup']['status']='Native approach animated; departure planned, pod design undecided'")
(OUT/'register_motion.py').write_text(source,encoding='utf-8')
print('Accepted single job recorded; reusable motion handoff prepared')
