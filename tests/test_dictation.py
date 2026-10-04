import pathlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "tools"))
from listening_review import prepare_dictation, recordings, validate_notes


class RecoveryTests(unittest.TestCase):
    def test_retries_share_identity_and_recover_text_and_anchor(self):
        with tempfile.TemporaryDirectory() as folder:
            base = pathlib.Path(folder)
            a = base / 'dictation-a.webm'
            b = base / 'dictation-b.webm'
            a.write_bytes(b'same audio'); b.write_bytes(b'same audio')
            b.with_suffix('.json').write_text(json.dumps({'text':'Scene idea'}))
            a.with_suffix('.anchor.json').write_text(json.dumps({'start':'12.5','end':'13','kind':'scene'}))
            items = recordings(base)
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0]['text'], 'Scene idea')
            self.assertEqual(items[0]['anchor']['start'], '12.5')
            ident = items[0]['id']
            (base/'dictation-0.webm').write_bytes(b'same audio')
            self.assertEqual(recordings(base)[0]['id'], ident)

    def test_legacy_recording_has_no_invented_anchor(self):
        with tempfile.TemporaryDirectory() as folder:
            base = pathlib.Path(folder)
            (base/'dictation-old.webm').write_bytes(b'audio')
            self.assertIsNone(recordings(base)[0]['anchor'])

    def test_recording_trash_keeps_audio_and_identity(self):
        with tempfile.TemporaryDirectory() as folder:
            base = pathlib.Path(folder)
            audio = base/'dictation-a.webm'
            audio.write_bytes(b'audio')
            ident = recordings(base)[0]['id']
            (base/'recording-state.json').write_text(json.dumps({ident:{'deleted':True}}))
            self.assertTrue(recordings(base)[0]['deleted'])
            self.assertEqual(audio.read_bytes(), b'audio')
            (base/'recording-state.json').write_text(json.dumps({ident:{'deleted':False}}))
            self.assertFalse(recordings(base)[0]['deleted'])


class NoteValidationTests(unittest.TestCase):
    def note(self, start, end, status='open'):
        return {'id':'note-a','start':start,'end':end,'text':'Idea','status':status}

    def test_unplaced_and_deleted_notes_are_valid(self):
        for note in (self.note(None,None), self.note(12,14,'deleted')):
            validate_notes({'notes':[note]}, 100)

    def test_partial_or_invalid_anchors_are_rejected(self):
        for start,end in ((None,12),(12,None),(-1,12),(12,11),(12,101)):
            with self.assertRaises(ValueError):
                validate_notes({'notes':[self.note(start,end)]}, 100)

    def test_duplicate_ids_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_notes({'notes':[self.note(0,0),self.note(None,None)]}, 100)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "Requires FFmpeg")
class DictationTests(unittest.TestCase):
    def recording(self, path, duration):
        # A streamed WebM mimics MediaRecorder: no seekable duration header.
        result = subprocess.run(
            ["ffmpeg", "-v", "error", "-f", "lavfi", "-i",
             "sine=frequency=440:sample_rate=16000", "-t", str(duration),
             "-c:a", "libopus", "-f", "webm", "-live", "1", "pipe:1"],
            capture_output=True, check=True)
        path.write_bytes(result.stdout)

    def test_streamed_webm_without_duration_is_decoded(self):
        with tempfile.TemporaryDirectory() as folder:
            audio = pathlib.Path(folder) / "browser.webm"
            self.recording(audio, 1.25)
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "csv=p=0", str(audio)], capture_output=True, text=True, check=True)
            self.assertEqual(probe.stdout.strip(), "N/A")
            self.assertAlmostEqual(prepare_dictation(audio, audio.with_suffix('.wav')), 1.25, places=2)
            self.assertTrue(audio.exists())

    def test_long_streamed_recording_is_rejected_and_retained(self):
        with tempfile.TemporaryDirectory() as folder:
            audio = pathlib.Path(folder) / "long.webm"
            self.recording(audio, 187)
            with self.assertRaisesRegex(ValueError, "at most three minutes"):
                prepare_dictation(audio, audio.with_suffix('.wav'))
            self.assertTrue(audio.exists())

    def test_invalid_recording_is_rejected_and_retained(self):
        with tempfile.TemporaryDirectory() as folder:
            audio = pathlib.Path(folder) / "invalid.webm"
            audio.write_bytes(b"invalid audio")
            with self.assertRaisesRegex(ValueError, "Could not decode"):
                prepare_dictation(audio, audio.with_suffix('.wav'))
            self.assertEqual(audio.read_bytes(), b"invalid audio")


if __name__ == "__main__":
    unittest.main()
