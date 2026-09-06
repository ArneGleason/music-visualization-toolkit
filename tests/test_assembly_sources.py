import copy
import json
import pathlib
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"tools"))
import assembly_sources as sources


class SourceSelectionTests(unittest.TestCase):
    def setUp(self):
        self.shot = {"id":"s002", "setup":"obs_console_macro", "start_sec":86/24,
                     "end_sec":155/24, "frames":69,
                     "clip":{"file":"flow.mp4", "in_sec":0, "speed":1}}
        self.entries = {"s002":{
            "id":"scope", "setup":"obs_console_macro",
            "decision":"prefer_procedural_still_composite_over_generated_video",
            "approval":"owner_approved_treatment", "delivery_status":"delivery_ready",
            "delivery_file":"clean.mp4", "timing_snapshot":{
                "fps":24, "song_start_frame":86, "song_end_frame_exclusive":155,
                "source_in_frame":0, "source_out_frame_exclusive":69}}}

    def resolve(self):
        with patch.object(pathlib.Path, "is_file", return_value=True), \
                patch.object(sources, "inspect_video", return_value=(24,69)):
            return sources.resolve_clip(ROOT, self.shot, 24, self.entries, 86,155)

    def test_override_without_mutating_assignment(self):
        before = copy.deepcopy(self.shot)
        self.assertEqual(self.resolve()["file"], "clean.mp4")
        self.assertEqual(self.shot, before)

    def test_unprotected_unchanged(self):
        self.shot["id"] = "s003"
        self.assertEqual(self.resolve(), self.shot["clip"])

    def test_motion_fx_policy(self):
        self.entries['s002']['decision'] = 'prefer_music_fx_composite_over_untreated_video'
        self.assertEqual(self.resolve()['file'], 'clean.mp4')

    def test_real_tunnel_migrated_to_outro(self):
        shot = next(s for s in json.loads((ROOT/'shots/shotlist.json').read_text())['shots']
                    if s['id'] == 'o01')
        entries = sources.load_decisions(ROOT)
        self.assertNotIn('s056', entries)
        self.assertEqual(entries['o01']['delivery_status'], 'delivery_ready')
        with patch.object(pathlib.Path,'is_file',return_value=True), \
                patch.object(sources,'inspect_video',return_value=(24,57)):
            self.assertEqual(sources.resolve_clip(ROOT,shot,24,entries,4120,4177)['file'],
                             'out/tunnel_arrival_o01/clean.mp4')

    def test_changed_timing_rejected(self):
        self.shot["start_sec"] += 1/24
        with self.assertRaisesRegex(ValueError, "timing"):
            self.resolve()

    def test_changed_setup_rejected(self):
        self.shot["setup"] = "different"
        with self.assertRaisesRegex(ValueError, "setup changed"):
            self.resolve()

    def test_pending_rejected(self):
        self.entries["s002"]["delivery_status"] = "pending"
        with self.assertRaisesRegex(ValueError, "not ready"):
            self.resolve()

    def test_missing_rejected(self):
        with patch.object(pathlib.Path, "is_file", return_value=False):
            with self.assertRaisesRegex(ValueError, "missing"):
                sources.resolve_clip(ROOT, self.shot,24,self.entries)

    def test_wrong_fps_or_short_file_rejected(self):
        for probe in [(30,69),(24,68)]:
            with self.subTest(probe=probe), patch.object(pathlib.Path,"is_file",return_value=True), \
                    patch.object(sources,"inspect_video",return_value=probe):
                with self.assertRaisesRegex(ValueError,"coverage"):
                    sources.resolve_clip(ROOT,self.shot,24,self.entries)


if __name__ == "__main__":
    unittest.main()
