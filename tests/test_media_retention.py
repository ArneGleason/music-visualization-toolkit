"""Retention must never infer that original media or native edits are disposable."""
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
from media_retention import candidates, inventory


class RetentionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)
        self.now = 2000000

    def version(self, number, extra=None):
        folder = self.project / f'generated/wip/previews/full/v{number:03d}'
        folder.mkdir(parents=True)
        (folder / '.disposable').write_text('render from retained source')
        (folder / 'preview.mp4').write_bytes(b'preview')
        if extra:
            (folder / extra).write_bytes(b'keep')
        for path in folder.iterdir():
            os.utime(path, (number * 100, number * 100))
        return folder

    def test_keeps_two_newest_and_pins(self):
        first = self.version(1)
        self.version(2, '.keep')
        self.version(3)
        self.version(4)
        self.assertEqual([x['path'] for x in candidates(self.project, now=self.now)], [str(first)])

    def test_grace_period_and_native_project_are_protected(self):
        native = self.version(1, 'editable.ecproj')
        recent = self.version(2)
        third = self.version(3)
        self.version(4)
        os.utime(recent / 'preview.mp4', (self.now, self.now))
        selected = [x['path'] for x in candidates(self.project, now=self.now)]
        self.assertEqual(selected, [str(third)])
        self.assertNotIn(str(native), selected)
        self.assertNotIn(str(recent), selected)

    def test_legacy_and_unmarked_media_never_selected(self):
        folder = self.project / 'generated/kling-v001'
        folder.mkdir(parents=True)
        (folder / 'original.mp4').write_bytes(b'paid footage')
        old = self.version(1)
        (old / '.disposable').unlink()
        self.version(2)
        self.version(3)
        self.assertEqual(candidates(self.project, now=self.now), [])
        self.assertEqual(inventory(self.project)['.mp4']['files'], 4)

    def test_symlinks_and_nested_directories_are_protected(self):
        first = self.version(1)
        (first / 'link.mp4').symlink_to(first / 'preview.mp4')
        second = self.version(2)
        (second / 'assets').mkdir()
        self.version(3)
        self.version(4)
        self.assertEqual(candidates(self.project, now=self.now), [])

    def test_symlinked_root_refused(self):
        (self.project / 'generated').symlink_to(self.project, target_is_directory=True)
        with self.assertRaises(ValueError):
            candidates(self.project)

    def test_apply_deletes_only_eligible_preview(self):
        old = self.version(1)
        pinned = self.version(2, '.keep')
        newer = self.version(3)
        newest = self.version(4)
        script = Path(__file__).resolve().parent.parent / 'tools/media_retention.py'
        command = [sys.executable, str(script), str(self.project)]
        subprocess.run(command, check=True, capture_output=True)
        self.assertTrue(old.exists())
        subprocess.run(command + ['--apply'], check=True, capture_output=True)
        self.assertFalse(old.exists())
        self.assertTrue(all(p.exists() for p in [pinned, newer, newest]))


if __name__ == '__main__':
    unittest.main()
