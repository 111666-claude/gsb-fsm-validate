import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fsmcheck import core


class FsmTest(unittest.TestCase):
    def test_start_is_always_reachable(self):
        out = core.analyze([("start", "go", "a")], core.Counter())
        self.assertIn("start", out["reachable"])

    def test_direct_successor_is_reachable(self):
        out = core.analyze([("start", "go", "a")], core.Counter())
        self.assertIn("a", out["reachable"])

    def test_empty_machine(self):
        out = core.analyze([], core.Counter())
        self.assertEqual(out["states"], [])
        self.assertEqual(out["unreachable"], [])

    def test_transitions_count_matches_rows(self):
        out = core.analyze([("start", "go", "a"), ("a", "go", "done")], core.Counter())
        self.assertEqual(out["transitions"], 2)

    def test_table_has_header(self):
        out = core.analyze([("start", "go", "a")], core.Counter())
        self.assertTrue(core.table(out).splitlines()[0].startswith("state"))


if __name__ == "__main__":
    unittest.main()
