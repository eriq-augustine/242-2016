import math
import unittest

import distance

class TestDistance(unittest.TestCase):
    def test_euclideanBase(self):
        a = [0, 0]
        b = [0, 0]
        self.assertEqual(distance.euclidean(a, b), 0)

        a = [1, 0]
        b = [0, 0]
        self.assertEqual(distance.euclidean(a, b), 1)

        a = [0, 0]
        b = [0, 1]
        self.assertEqual(distance.euclidean(a, b), 1)

        a = [0, 0]
        b = [1, 1]
        self.assertEqual(distance.euclidean(a, b), math.sqrt(2))

    def test_levenshteinBase(self):
        a = 'abc'
        b = 'abc'
        self.assertEqual(distance.levenshtein(a, b), 0)

        a = 'abc'
        b = 'abd'
        self.assertEqual(distance.levenshtein(a, b), 1)

        a = 'abc'
        b = 'abz'
        self.assertEqual(distance.levenshtein(a, b), 1)

        a = 'ab'
        b = 'abc'
        self.assertEqual(distance.levenshtein(a, b), 1)

        a = 'abcd'
        b = 'abc'
        self.assertEqual(distance.levenshtein(a, b), 1)

        a = 'abc'
        b = 'xyz'
        self.assertEqual(distance.levenshtein(a, b), 3)

if __name__ == '__main__':
    unittest.main()
