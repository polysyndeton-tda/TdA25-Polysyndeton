import unittest
from src.search import levenshtein_distance


class TestLevenshtein(unittest.TestCase):
    def test_identical_strings(self):
        a = "hroch"
        b = "hroch"
        dist = levenshtein_distance(a, b)
        self.assertEqual(dist, 0)

    def test_twp_strings(self):
        a = "hroch"
        b = "hrosi"
        dist = levenshtein_distance(a, b)
        self.assertEqual(dist, 2)


if __name__ == "__main__":
    unittest.main()
