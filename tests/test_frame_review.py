import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from frame_review import load_shots


class ShotNavigationTest(unittest.TestCase):
    def test_partial_preview_and_exclusive_edges(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "shots.json"
            path.write_text(json.dumps({"frameIndexBase": 0, "shots": [
                {"id": "before", "startFrame": 0, "endFrameExclusive": 10},
                {"id": "partial", "startFrame": 10, "endFrameExclusive": 20},
                {"id": "inside", "startFrame": 20, "endFrameExclusive": 30},
                {"id": "after", "startFrame": 30, "endFrameExclusive": 40},
            ]}))
            result = load_shots(path, master_start=15, count=15, frame_base=0)
            self.assertEqual([s["id"] for s in result], ["partial", "inside"])
            self.assertEqual(result[0]["startFrame"], 10)
            self.assertEqual(result[-1]["endFrameExclusive"], 30)

    def test_one_based_player_converts_zero_based_shots(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "shots.json"
            path.write_text(json.dumps({"frameIndexBase": 0, "shots": [
                {"id": "second", "startFrame": 10, "endFrameExclusive": 20},
                {"id": "first", "startFrame": 0, "endFrameExclusive": 10},
            ]}))
            result = load_shots(path, master_start=1, count=20, frame_base=1)
            self.assertEqual([s["startFrame"] for s in result], [1, 11])
            self.assertEqual(result[-1]["endFrameExclusive"], 21)

    def test_without_shotlist(self):
        self.assertEqual(load_shots(None, 0, 100, 0), [])

    def test_source_offset_is_not_shifted_with_master_numbering(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'shots.json'
            path.write_text(json.dumps({'fps': 24, 'frameIndexBase': 0, 'shots': [
                {'id': 'motion', 'startFrame': 559, 'endFrameExclusive': 637,
                 'videoSource': 'clip.mp4', 'videoEdit': {'sourceInFrame': 12}},
                {'id': 'still', 'startFrame': 637, 'endFrameExclusive': 690,
                 'videoHandles': {'editInSourceFrame': 24}},
            ]}))
            motion, still = load_shots(path, 560, 131, 1)
            self.assertEqual(motion['endFrameExclusive'] - motion['startFrame'], 78)
            self.assertEqual(motion['sourceInFrame'] / motion['sourceFps'], 0.5)
            self.assertEqual(motion['mediaType'], 'video')
            self.assertIsNone(still['sourceInFrame'])
            self.assertEqual(still['mediaType'], 'still')


if __name__ == "__main__":
    unittest.main()
