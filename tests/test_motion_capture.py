import math
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from motion_capture import Bone, joint_positions  # noqa: E402


class MotionCaptureTests(unittest.TestCase):
    def test_forward_kinematics_preserves_rest_direction(self):
        bones = {"arm": Bone("arm", (1, 0, 0), 2, (0, 0, 0), "XYZ", ())}
        pose = joint_positions({"root": [0, 0, 0, 0, 0, 0]}, bones,
                               {"root": ["arm"]})
        self.assertEqual(pose["arm"], (2.0, 0.0, 0.0))

    def test_joint_rotation_moves_endpoint_without_changing_length(self):
        bones = {"arm": Bone("arm", (1, 0, 0), 2, (0, 0, 0), "XYZ", ("rz",))}
        pose = joint_positions({"root": [0, 0, 0, 0, 0, 0], "arm": [90]},
                               bones, {"root": ["arm"]})
        self.assertAlmostEqual(pose["arm"][0], 0, places=6)
        self.assertAlmostEqual(pose["arm"][1], 2, places=6)
        self.assertAlmostEqual(math.dist(pose["root"], pose["arm"]), 2, places=6)


if __name__ == "__main__":
    unittest.main()
