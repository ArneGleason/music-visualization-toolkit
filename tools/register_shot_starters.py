"""Register a complete starter batch without altering musical edit timing."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
from PIL import Image


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project', type=Path)
    ap.add_argument('--batch', required=True)
    ap.add_argument('--renderer', type=Path, required=True)
    args = ap.parse_args()
    base = args.project.resolve().parent
    score_path = base/'shots/shotlist.json'
    score = json.loads(score_path.read_text())
    authored = base/'shots'/args.batch
    output = base/'generated/storyboard'/args.batch
    manifest, receipts = [], []
    for shot in score['shots']:
        candidate = output/(shot['id']+'.png')
        if candidate.exists():
            receipt_path = authored/(shot['id']+'.review.json')
            prompt_path = authored/(shot['id']+'.prompt.txt')
            receipt = json.loads(receipt_path.read_text())
            prompt = prompt_path.read_text()
            if shot['promptLock'] not in prompt:
                raise ValueError(f"Missing exact prompt lock: {shot['id']}")
            with Image.open(candidate) as im:
                im.verify()
            shot.update(starterImage=candidate.relative_to(base).as_posix(),
                        starterRevision=args.batch.rsplit('-',1)[-1],
                        starterReview=receipt_path.relative_to(base).as_posix(),
                        status='starter_frame_batch_pending_review',
                        generationApproach='Generated clean starter; motion not generated.')
            if shot['id']=='ta-002':
                shot.pop('motionBlocker',None)
            receipts.append(receipt)
        elif not shot.get('starterImage') or not (base/shot['starterImage']).exists():
            raise ValueError(f"No starter image for {shot['id']}")
        source = Path(os.path.relpath(base/shot['starterImage'],output/'review')).as_posix()
        manifest.append({'index':shot['displayId'],'title':f"{shot['sceneName']} / {shot['title']} · {shot['startSeconds']:.3f}–{shot['endSeconds']:.3f}s",'src':source,'href':source})
    # All files validate before the authoritative list changes.
    score_path.write_text(json.dumps(score,indent=2,ensure_ascii=False)+'\n')
    # Include refinement prompts as well as initial requests for provenance.
    prompt_set = [path.name+'\n'+path.read_text() for path in sorted(authored.glob('*.prompt.txt'))]
    (authored/'generation-prompts.txt').write_text('\n\n'.join(prompt_set)+'\n')
    (authored/'references.json').write_text(json.dumps({'batch':args.batch,'status':'review_pending','totalShots':len(manifest),'newOrRevised':len(receipts),'reviews':receipts},indent=2,ensure_ascii=False)+'\n')
    output.mkdir(parents=True,exist_ok=True)
    (output/'review-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    spec = importlib.util.spec_from_file_location('review_renderer',args.renderer)
    renderer = importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
    review = output/'review';review.mkdir(exist_ok=True)
    renderer.build_review_html(review,manifest,{'preset':'image-wall','showCaptions':True,'showPrompts':False,'minTileWidth':600,'output':'starter-board.html','title':'Together Anyways · complete first-run starter frames'})
    print(f'Registered {len(receipts)} new/revised images; {len(manifest)} shots complete.')


if __name__=='__main__':
    main()
