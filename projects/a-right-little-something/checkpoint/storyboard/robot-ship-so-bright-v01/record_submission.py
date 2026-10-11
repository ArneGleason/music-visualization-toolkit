"""Record the single approved paid job and the staged edit."""
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
PROJECT=OUT.parents[2]
def load(p): return json.loads(p.read_text(encoding='utf-8'))
def save(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=PROJECT/'kling-robot-ship-so-bright-v01.json'
plan=load(p)
job=load(PROJECT/plan['output']/plan['shots'][0]['id']/'submission.json')['body']
plan.update(status='One approved 48-credit replacement accepted by Kling; awaiting collection and QA',
    actualSubmittedCredits=job['creditsConsumed'],generationId=job['generationId'])
save(p,plan)
g=load(OUT/'generation-input.json')
g.update(status='Built-in ImageGen first attempt succeeded; native motion approved and submitted',
    originalGeneratedFile='C:/Users/arneg/.codex/generated_images/01a125f7-d729-7f60-8997-758a2cbdca4d/exec-4fb6e0b3-e7a3-44de-8edd-2697aaea8361.png',
    reviewNotes='Original graphite ship and galleries retained. Large textured curved sun dominates; no luminous lines between vessel and star. Short cyan engine light remains aft. Ship fills about half the frame, slightly larger than the requested 40–45%. Quiet dark lyric strip verified in timed proof.',
    boardRevision=69)
save(OUT/'generation-input.json',g)
print('Paid job recorded exactly once: '+job['generationId'])
