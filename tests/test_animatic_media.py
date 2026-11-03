import sys
import tempfile
import unittest
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from animatic_media import Artwork


class TransitionTests(unittest.TestCase):
    def test_full_frame_fills_canvas_without_stretching(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            Image.new('RGB', (200,100), 'red').save(base/'still.png')
            shot = {'id':'a','starterImage':'still.png'}
            art = Artwork(base, [shot], 24, full_frame=True)
            frame = art.frame(shot, 0)
            self.assertEqual(frame.size, (1920,1080))
            self.assertEqual(frame.getextrema(), ((255,255),(0,0),(0,0)))

    def test_full_frame_blackout_dimensions(self):
        a = {'id':'a','startFrame':0,'frames':30}
        b = {'id':'b','startFrame':30,'frames':40,
             'transitionIn':{'type':'impact_blackout'}}
        art = Artwork(Path('.'), [a,b], 24, full_frame=True)
        self.assertEqual(art.at(b,30).size, (1920,1080))
        self.assertEqual(art.at(b,35).size, (1920,1080))

    def test_upward_wipe_reveals_bottom_first(self):
        art = Artwork.__new__(Artwork)
        a = {'id':'a', 'startFrame':0, 'frames':20}
        b = {'id':'b', 'startFrame':20, 'frames':20,
             'transitionIn':{'type':'soft_wipe','frames':5,'alignment':'start',
                             'direction':'bottom_to_top','featherFraction':.2}}
        art.shots = [a,b]
        art.frame = lambda s,i: Image.new('RGB',(100,100),'black' if s['id']=='a' else 'white')
        self.assertEqual(art.at(b,20).getextrema(), ((0,0),)*3)
        middle = art.at(b,22)
        self.assertEqual(middle.getpixel((50,0)), (0,0,0))
        self.assertEqual(middle.getpixel((50,99)), (255,255,255))
        self.assertTrue(0 < middle.getpixel((50,50))[0] < 255)
        self.assertEqual(art.at(b,24).getextrema(), ((255,255),)*3)

    def test_impact_blackout_preserves_source_time_and_reveals_live_frame(self):
        art = Artwork.__new__(Artwork)
        a = {'id': 'a', 'startFrame': 0, 'frames': 30}
        b = {'id': 'b', 'startFrame': 30, 'frames': 40,
             'transitionIn': {'type': 'impact_blackout'}}
        art.shots = [a, b]
        calls = []
        def frame(shot, index):
            self.assertTrue(shot['startFrame'] <= index < shot['startFrame']+shot['frames'])
            calls.append((shot['id'], index))
            return Image.new('RGB', (1920,1008), (index,20,30))
        art.frame = frame
        self.assertEqual(art.at(a,29).getextrema(), ((255,255),)*3)
        calls.clear()
        for index in range(30,38):
            result = art.at(b,index)
        self.assertEqual(result.getextrema(), ((0,0),)*3)
        self.assertEqual(calls, [])
        self.assertEqual(art.at(b,51).getpixel((0,0)), (51,20,30))
        self.assertEqual(calls, [('b',51)])
        self.assertEqual(art.at(b,52).getpixel((0,0)), (52,20,30))

    def test_soft_wipe_reveals_left_first_and_has_clean_endpoints(self):
        art = Artwork.__new__(Artwork)
        a = {'id': 'a', 'startFrame': 0, 'frames': 10}
        b = {'id': 'b', 'startFrame': 10, 'frames': 10,
             'transitionIn': {'type': 'soft_wipe', 'frames': 5,
                              'alignment': 'start', 'direction': 'left_to_right',
                              'featherFraction': .2}}
        art.shots = [a, b]
        art.frame = lambda s, i: Image.new('RGB', (100, 2),
                                         'black' if s['id'] == 'a' else 'white')
        self.assertEqual(art.at(b, 10).getextrema(), ((0, 0),) * 3)
        middle = art.at(b, 12)
        self.assertEqual(middle.getpixel((0, 0)), (255, 255, 255))
        self.assertEqual(middle.getpixel((99, 0)), (0, 0, 0))
        self.assertTrue(0 < middle.getpixel((50, 0))[0] < 255)
        self.assertEqual(art.at(b, 14).getextrema(), ((255, 255),) * 3)
        b['transitionIn']['direction'] = 'right_to_left'
        self.assertEqual(art.at(b, 12).getpixel((99, 0)), (255, 255, 255))

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

    def test_start_aligned_transition_needs_no_incoming_head_handle(self):
        art = Artwork.__new__(Artwork)
        a = {'id': 'a', 'startFrame': 0, 'frames': 34}
        b = {'id': 'b', 'startFrame': 34, 'frames': 56,
             'transitionIn': {'type': 'crossfade', 'frames': 6, 'alignment': 'start'}}
        art.shots = [a, b]
        calls = []
        def frame(shot, index):
            if shot['id'] == 'b' and index < 34:
                raise ValueError('No incoming head handle')
            calls.append((shot['id'], index))
            return Image.new('RGB', (1, 1), 'black' if shot['id'] == 'a' else 'white')
        art.frame = frame
        self.assertEqual(art.at(a, 33).getpixel((0, 0)), (0, 0, 0))
        self.assertEqual(art.at(b, 34).getpixel((0, 0)), (0, 0, 0))
        self.assertEqual(art.at(b, 39).getpixel((0, 0)), (255, 255, 255))
        self.assertIn(('a', 39), calls)
        calls.clear()
        art.at(b, 40)
        self.assertEqual(calls, [('b', 40)])

if __name__=='__main__':unittest.main()
