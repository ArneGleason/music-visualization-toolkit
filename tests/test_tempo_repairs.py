import pathlib
import contextlib
import io
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/"tools"))
from dawproject import main, parse_tempo
from timeline import MusicalGrid


class TempoRepairTests(unittest.TestCase):
    def test_import_keeps_pickup_after_final_beat_of_bar(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = pathlib.Path(temp)
            source = folder / 'project.xml'
            output = folder / 'beatmap.json'
            source.write_text('<Project><TempoAutomation timeUnit="beats">'
                '<RealPoint time="0" value="120" interpolation="linear"/>'
                '<RealPoint time="16" value="120" interpolation="linear"/>'
                '</TempoAutomation></Project>', encoding='utf-8')
            for zero, first_bar, origin in [(7.5, 2, '2.4.480'), (8, 3, '3.1')]:
                with self.subTest(zero=zero):
                    args = ['dawproject.py', str(source), '--audio', str(folder / 'absent.wav'),
                            '--zero-at', str(zero), '--beatmap-out', str(output), '--no-lyrics']
                    with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()):
                        main()
                    beatmap = json.loads(output.read_text(encoding='utf-8'))
                    self.assertEqual(beatmap['bars'][0]['bar'], first_bar)
                    grid = MusicalGrid(beatmap)
                    self.assertEqual(grid.position(0).text(), origin)
                    self.assertAlmostEqual(grid.sec(origin), 0)

    def test_local_clip_points_do_not_replace_opening_tempo(self):
        root=ET.fromstring('<Project><TempoAutomation timeUnit="beats">'
            '<RealPoint time="0" value="120" interpolation="linear"/>'
            '<RealPoint time="8" value="120" interpolation="linear"/>'
            '<RealPoint time="0" value="60" interpolation="linear"/>'
            '<RealPoint time="4" value="90" interpolation="linear"/>'
            '<RealPoint time="16" value="90" interpolation="linear"/>'
            '</TempoAutomation></Project>')
        repairs={"points":[
            {"index":2,"expected":[0.0,60.0,"linear"],"beat":8,"interpolation":"hold"},
            {"index":3,"expected":[4.0,90.0,"linear"],"beat":12,"interpolation":"hold"}]}
        curve=parse_tempo(root,repairs)
        self.assertEqual(curve.bpm(0),120)
        self.assertEqual(curve.bpm(10),60)
        self.assertAlmostEqual(curve.sec(16),4+4+4*60/90)
        repairs["points"][0]["expected"][1]=61
        with self.assertRaisesRegex(ValueError,"does not match"):
            parse_tempo(root,repairs)


if __name__=="__main__":
    unittest.main()
