# tests/test_scorecard.py
import unittest
from src.ossf_scorecard.scorecard import get_scorecard

class TestScorecard(unittest.TestCase):
    def test_get_scorecard(self):
        platform = "github.com"
        org = "nexB"
        repo = "scancode-toolkit"
        data = get_scorecard(platform, org, repo)
        self.assertIn("scorecard", data)

if __name__ == "__main__":
    unittest.main()
