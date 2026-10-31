"""Protect edits and paths during cross-machine media restoration."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'tools'))
from project_media import digest, restore, target


class MediaRestoreTests(unittest.TestCase):
    def fixture(self, root, name='projects/demo/generated/frame.png'):
        archive = root / 'media.zip'
        data = b'original media'
        with zipfile.ZipFile(archive, 'w') as bundle:
            bundle.writestr(name, data)
        spec = {'sha256': digest(archive), 'files': [
            {'path': name, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}]}
        return archive, spec

    def test_relocated_restore_is_repeatable_and_preserves_edits(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            archive, spec = self.fixture(base)
            root = base / 'a different checkout'
            root.mkdir()
            restore(root, spec, archive)
            restore(root, spec, archive)
            path = target(root, spec['files'][0]['path'])
            path.write_bytes(b'new local edit')
            with self.assertRaisesRegex(ValueError, 'Local files differ'):
                restore(root, spec, archive)
            self.assertEqual(path.read_bytes(), b'new local edit')

    def test_corrupt_archive_and_member_never_install(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            archive, spec = self.fixture(root)
            spec['files'][0]['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'File checksum failed'):
                restore(root, spec, archive)
            self.assertFalse((root / 'projects').exists())
            spec['sha256'] = '0' * 64
            with self.assertRaisesRegex(ValueError, 'Archive checksum failed'):
                restore(root, spec, archive)

    def test_rejects_escape_and_extra_members(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for name in ['../escape', '/absolute', 'C:/drive', 'folder\\escape']:
                with self.assertRaises(ValueError):
                    target(root, name)
            archive, spec = self.fixture(root)
            with zipfile.ZipFile(archive, 'a') as bundle:
                bundle.writestr('unexpected', b'other')
            spec['sha256'] = digest(archive)
            with self.assertRaisesRegex(ValueError, 'members do not match'):
                restore(root, spec, archive)
            self.assertFalse((root / 'projects').exists())


if __name__ == '__main__':
    unittest.main()
