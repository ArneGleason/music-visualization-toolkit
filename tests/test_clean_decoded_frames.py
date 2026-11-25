"""Check deletion against real decoded video, including sources with audio."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
from clean_decoded_frames import inspect


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg required')
class CacheCleanupTests(unittest.TestCase):
    def test_regeneration_and_deletion_preserve_unique_assets(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            parent = root / 'generated/test'
            parent.mkdir(parents=True)
            source = parent / 'clip.mp4'
            cache = parent / 'clip-frames'
            cache.mkdir()
            subprocess.run(['ffmpeg', '-v', 'error', '-f', 'lavfi', '-i',
                            'testsrc2=size=64x48:rate=24', '-f', 'lavfi', '-i',
                            'sine=frequency=440', '-t', '0.25', '-pix_fmt', 'yuv420p',
                            str(source)], check=True)
            decode = ['ffmpeg', '-v', 'error', '-y', '-i', str(source), '-vf', 'fps=24',
                      '-compression_level', '1', '-start_number', '0', str(cache / '%05d.png')]
            subprocess.run(decode, check=True)
            stamp = cache / 'source-stamp.txt'
            stamp.write_text(str((source.stat().st_size, source.stat().st_mtime_ns, 24)))
            record, frames, _ = inspect(cache)
            self.assertEqual(record['frameCount'], 6)
            with Image.open(frames[0]) as image:
                image = image.convert('RGB')
                image.putpixel((0, 0), (1, 2, 3))
                image.save(frames[0])
            with self.assertRaisesRegex(ValueError, 'differs from source'):
                inspect(cache)
            subprocess.run(decode, check=True)
            sample = cache / '001.jpg'
            sample.write_bytes(b'preserve review sample')
            tool = Path(__file__).resolve().parent.parent / 'tools/clean_decoded_frames.py'
            subprocess.run([sys.executable, str(tool), str(root), '--report',
                            str(root / 'receipt.json'), '--apply'], check=True, capture_output=True)
            self.assertTrue(source.exists())
            self.assertTrue(sample.exists())
            self.assertFalse(list(cache.glob('*.png')))
            self.assertFalse(stamp.exists())


if __name__ == '__main__':
    unittest.main()
