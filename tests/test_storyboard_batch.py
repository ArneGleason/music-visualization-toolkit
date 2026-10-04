import contextlib
import io
import json
import pathlib
import sys
import tempfile
import unittest

ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'tools'))
from plan_storyboard_batch import plan


class StoryboardBatchTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=pathlib.Path(self.temp.name)
        spec=json.loads((ROOT/'projects/a-right-little-something/storyboard-opening.json').read_text())
        fixtures={
            'project.json':{'render':{'fps':24},'timing':{'beatmap':'generated/beatmap.json'}},
            'storyboard-opening.json':spec,
            'generated/beatmap.json':{'duration_sec':40,'bars':[
                {'bar':i+1,'num':4,'beats':[i*2+j*.5 for j in range(4)]} for i in range(22)]},
            'generated/review/listening-notes.json':{'revision':1,'notes':[
                {'id':s['noteId'],'start':t,'text':'Human scene idea'}
                for s,t in zip(spec['shots'],[0,9.46,15.11,18.52,22.59])]},
            'generated/animatic/animatic-data.json':{'phrases':[{'id':spec['endPhrase'],'start':26.344}]}}
        for name,doc in fixtures.items():
            target=self.base/name;target.parent.mkdir(parents=True,exist_ok=True)
            target.write_text(json.dumps(doc))
        self.path=self.base/'shots/shotlist.json';self.path.parent.mkdir()
        self.existing={'id':'unrelated','description':'Hand-authored concept','startFrame':2831}
        self.path.write_text(json.dumps({'shots':[self.existing]}))

    def run_plan(self,merge=True):
        with contextlib.redirect_stdout(io.StringIO()):
            plan(self.base/'project.json',self.base/'storyboard-opening.json',merge)
        return json.loads(self.path.read_text())

    def test_merge_preserves_creative_work_and_contiguous_frame_handles(self):
        doc=self.run_plan();shots=doc['shots'][:5]
        self.assertEqual(doc['shots'][-1],self.existing)
        self.assertEqual(len(shots),5)
        for shot in shots:
            self.assertEqual(shot['frames'],shot['endFrameExclusive']-shot['startFrame'])
            self.assertEqual(shot['handles']['generatedFrames'],shot['frames']+24)
            self.assertEqual(shot['handles']['editInLocalFrame'],13)
        self.assertEqual(shots[0]['handles']['sourceStartFrame'],-11)
        for a,b in zip(shots,shots[1:]):
            self.assertEqual(a['endFrameExclusive'],b['startFrame'])
        shots[0]['description']='Custom opening description'
        self.path.write_text(json.dumps(doc))
        rerun=self.run_plan()
        self.assertEqual(rerun['shots'][0]['description'],'Custom opening description')
        self.assertEqual(len(rerun['shots']),6)

    def test_existing_register_requires_merge(self):
        original=self.path.read_bytes()
        with self.assertRaisesRegex(ValueError,'--merge'):
            self.run_plan(False)
        self.assertEqual(self.path.read_bytes(),original)


if __name__=='__main__':unittest.main()
