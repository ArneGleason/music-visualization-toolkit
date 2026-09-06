import pathlib
import sys
import unittest
from unittest.mock import patch, Mock

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'tools'))
import assembly_timebase as tb


class TimebaseTests(unittest.TestCase):
    def test_native_rate_unchanged(self):
        clip={'file':'native.mp4','in_sec':2.86,'speed':1}
        with patch.object(tb,'inspect_video',return_value=(24,192)):
            self.assertEqual(tb.conform_clip('.',clip,24),clip)

    def test_missing_proxy_fails_closed(self):
        with patch.object(tb,'inspect_video',return_value=(30,239)), \
             patch.object(pathlib.Path,'stat',return_value=Mock(st_size=100,st_mtime_ns=1)), \
             patch.object(pathlib.Path,'exists',return_value=False):
            with self.assertRaisesRegex(ValueError,'Missing time-preserving'):
                tb.conform_clip('.',{'file':'source.mp4'},24)

    def test_proxy_preserves_inpoint_and_selection(self):
        clip={'file':'source.mp4','in_sec':2.86,'speed':1,'assembly_decision':'test'}
        with patch.object(tb,'inspect_video',side_effect=[(30,239),(24,191)]), \
             patch.object(pathlib.Path,'stat',return_value=Mock(st_size=100,st_mtime_ns=1)), \
             patch.object(pathlib.Path,'exists',return_value=True):
            result=tb.conform_clip('.',clip,24)
        self.assertEqual(result['in_sec'],2.86)
        self.assertEqual(result['assembly_decision'],'test')
        self.assertEqual(clip['file'],'source.mp4')
        self.assertIn('assembly_cfr',result['file'])

    def test_wrong_proxy_rate_rejected(self):
        with patch.object(tb,'inspect_video',side_effect=[(30,239),(30,239)]), \
             patch.object(pathlib.Path,'stat',return_value=Mock(st_size=100,st_mtime_ns=1)), \
             patch.object(pathlib.Path,'exists',return_value=True):
            with self.assertRaisesRegex(ValueError,'Invalid CFR cache'):
                tb.conform_clip('.',{'file':'source.mp4'},24)

    def test_unhandled_speed_rejected(self):
        with self.assertRaisesRegex(ValueError,'non-unit speed'):
            tb.conform_clip('.',{'file':'source.mp4','speed':.8},24)

    def test_integer_and_float_fps_use_same_cache(self):
        with patch.object(tb,'inspect_video',side_effect=[(30,239),(24,191)]*2), \
             patch.object(pathlib.Path,'stat',return_value=Mock(st_size=100,st_mtime_ns=1)), \
             patch.object(pathlib.Path,'exists',return_value=True):
            integer=tb.conform_clip('.',{'file':'source.mp4'},24)
            decimal=tb.conform_clip('.',{'file':'source.mp4'},24.0)
        self.assertEqual(integer['file'],decimal['file'])


if __name__=='__main__': unittest.main()
