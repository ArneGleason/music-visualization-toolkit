import pathlib
import sys
import unittest
import xml.etree.ElementTree as ET

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent.parent/"tools"))
from dawproject import parse_tempo


class TempoRepairTests(unittest.TestCase):
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
