import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from animatic_media import Artwork


class TransitionTests(unittest.TestCase):
    def test_centered_transition_uses_both_source_handles(self):
        art=Artwork.__new__(Artwork)
        a={'id':'a','startFrame':0,'frames':109}
        b={'id':'b','startFrame':109,'frames':100,'transitionIn':{'type':'crossfade','frames':12}}
        art.shots=[a,b]
        calls=[]
        def frame(shot,index):
            calls.append((shot['id'],index))
            return Image.new('RGB',(1,1),'black' if shot['id']=='a' else 'white')
        art.frame=frame
        self.assertEqual(art.at(a,103).getpixel((0,0)),(0,0,0))
        self.assertEqual(art.at(b,114).getpixel((0,0)),(255,255,255))
        self.assertIn(('b',103),calls)
        self.assertIn(('a',114),calls)
        calls.clear();art.at(b,115)
        self.assertEqual(calls,[('b',115)])

    def test_missing_handle_fails_instead_of_freezing(self):
        with tempfile.TemporaryDirectory() as tmp:
            art=Artwork.__new__(Artwork);art.fps=24;art.cache={'a':Path(tmp)}
            shot={'id':'a','videoSource':'a.mp4','startFrame':0,'frames':10}
            with self.assertRaisesRegex(ValueError,'Insufficient video handle'):
                art.frame(shot,-25)

if __name__=='__main__':unittest.main()
