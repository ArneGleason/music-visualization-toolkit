from __future__ import annotations

import json
import pathlib
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

from dawproject import parse_notes  # noqa: E402
from timeline import (MusicalGrid, Position, TimelineRegister,  # noqa: E402
                      compile_timeline, validate_timeline)
from waveforms import _origin_beat  # noqa: E402


def beatmap():
    return {
        "ppq": 960,
        "duration_sec": 8.0,
        "zero_beat": 0.0,
        "tempo_map": [],
        "bars": [
            {"bar": 1, "beat": 0, "sec": 0, "num": 4, "den": 4,
             "beats": [0.0, 0.5, 1.0, 1.5]},
            {"bar": 2, "beat": 4, "sec": 2, "num": 4, "den": 4,
             "beats": [2.0, 2.6, 3.2, 3.8]},
            {"bar": 3, "beat": 8, "sec": 4.4, "num": 4, "den": 4,
             "beats": [4.4, 5.1, 5.8, 6.5]},
            {"bar": 4, "beat": 12, "sec": 7.2, "num": 4, "den": 4,
             "beats": [7.2, 7.9, 8.6, 9.3]},
        ],
    }


class GridTests(unittest.TestCase):
    def test_tick_interpolation_and_inverse(self):
        grid = MusicalGrid(beatmap())
        self.assertAlmostEqual(grid.sec("2.1.480"), 2.3)
        self.assertEqual(grid.position(2.3), Position(2, 1, 480))
        self.assertEqual(grid.position(2.31, snap_ticks=240), Position(2, 1, 480))

    def test_position_parser_is_explicit(self):
        self.assertEqual(Position.parse("12.3.480"), Position(12, 3, 480))
        self.assertEqual(Position.parse({"bar": 7, "beat": 2}), Position(7, 2, 0))


class RegisterTests(unittest.TestCase):
    def test_validation_allows_unplaced_and_rejects_backwards_range(self):
        grid = MusicalGrid(beatmap())
        timeline = {"schemaVersion": 1, "tracks": [
            {"id": "lyrics", "type": "lyrics", "items": [
                {"id": "pending", "text": "later", "timingStatus": "unplaced"},
                {"id": "bad", "start": "2.2", "end": "2.1"},
            ]}
        ]}
        errors = validate_timeline(timeline, grid)
        self.assertEqual(len(errors), 1)
        self.assertIn("ends at or before", errors[0])

    def test_improv_origin_is_allowed_only_on_lyrics(self):
        grid = MusicalGrid(beatmap())
        timeline = {"schemaVersion": 1, "tracks": [
            {"id": "lyrics", "type": "lyrics", "items": [
                {"id": "vocal-extra", "text": "Ooh", "lyricOrigin": "improv",
                 "start": "1.1", "end": "1.2"},
            ]},
            {"id": "notes", "type": "notes", "items": [
                {"id": "wrong-track", "text": "No", "lyricOrigin": "improv",
                 "start": "1.1", "end": "1.2"},
            ]},
        ]}
        errors = validate_timeline(timeline, grid)
        self.assertEqual(len(errors), 1)
        self.assertIn("outside a lyrics track", errors[0])

    def test_compile_rounds_edges_to_frames_and_query_returns_overlap(self):
        with tempfile.TemporaryDirectory() as tmp:
            d = pathlib.Path(tmp)
            (d / "generated").mkdir()
            (d / "beatmap.json").write_text(json.dumps(beatmap()))
            timeline = {"schemaVersion": 1, "project": "test", "tracks": [
                {"id": "scenes", "type": "scene", "label": "Scenes", "items": [
                    {"id": "a", "start": "1.1", "end": "2.2", "prompt": "A"},
                    {"id": "b", "start": "2.1", "end": "3.1", "prompt": "B"},
                ]},
                {"id": "choreo", "type": "choreography", "label": "Choreo", "items": [
                    {"id": "c", "start": "2.1", "end": "2.3",
                     "prompt": "react", "drivers": ["bass.amp"]},
                ]},
            ]}
            (d / "timeline.json").write_text(json.dumps(timeline))
            project = {"title": "Test", "slug": "test", "render": {"fps": 24},
                       "timeline": "timeline.json",
                       "timing": {"beatmap": "beatmap.json",
                                  "compiledTimeline": "generated/compiled.json"}}
            compiled = compile_timeline(project, d)
            scene_b = compiled["tracks"][0]["items"][1]
            self.assertEqual(scene_b["startFrame"], 48)
            self.assertEqual(scene_b["startSec"], 2.0)
            state = TimelineRegister(compiled).at(frame=50)
            self.assertEqual([x["id"] for x in state["scenes"]], ["a", "b"])
            self.assertEqual(state["scene"]["id"], "b")
            self.assertEqual(state["drivers"], ["bass.amp"])


class DawprojectNoteTests(unittest.TestCase):
    def test_lane_track_mapping_and_disabled_clip_filter(self):
        root = ET.fromstring("""
        <Project><Structure><Track id="t1" name="Synth"/></Structure>
        <Arrangement><Lanes track="t1"><Clips>
          <Clip time="8" playStart="2"><Notes><Note time="3"/></Notes></Clip>
          <Clip time="20" enable="false"><Notes><Note time="1"/></Notes></Clip>
        </Clips></Lanes></Arrangement></Project>
        """)
        self.assertEqual(parse_notes(root), [(9.0, "Synth")])


class WaveformAlignmentTests(unittest.TestCase):
    def test_file_origin_uses_clip_time_minus_play_start(self):
        root = ET.fromstring("""
        <Project><Structure><Track id="vox" name="Lead Vocal restored"/></Structure>
        <Arrangement><Lanes track="vox"><Clips>
          <Clip time="12" playStart="4.75" duration="20"/>
          <Clip time="40" playStart="32.75" duration="8"/>
          <Clip time="0" contentTimeUnit="seconds" duration="200"/>
        </Clips></Lanes></Arrangement></Project>
        """)
        self.assertEqual(_origin_beat(root, "Lead Vocal"), 7.25)


if __name__ == "__main__":
    unittest.main()
