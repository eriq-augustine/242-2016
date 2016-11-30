import math
import unittest

import distance

class TestDistance(unittest.TestCase):
    def test_euclideanBase(self):
        a = [0, 0]
        b = [0, 0]
        self.assertAlmostEqual(distance.euclidean(a, b), 0, places = 3)
        self.assertAlmostEqual(distance.euclidean(a, b, distance.logNormalize), 0, places = 3)

        a = [1, 0]
        b = [0, 0]
        self.assertAlmostEqual(distance.euclidean(a, b), 0.46199999, places = 3)

        a = [0, 0]
        b = [0, 1]
        self.assertAlmostEqual(distance.euclidean(a, b), 0.46199999, places = 3)

        a = [0, 0]
        b = [1, 1]
        self.assertAlmostEqual(distance.euclidean(a, b), 0.60884, places = 3)

    def test_manhattanScalarBase(self):
        testCases = [
            (0, 0, 0, 0, 0),
            (-1, 0, 1, 0, 0.462),
            (0, 1, 1, 0, 0.462),
            (1, 1, 0, 0, 0),
            (1, -1, 2, 0.693, 0.7616)
        ]

        for testCase in testCases:
            self.assertAlmostEqual(distance.manhattanScalar(testCase[0], testCase[1], distance.noNormalize), testCase[2], places = 3)
            self.assertAlmostEqual(distance.manhattanScalar(testCase[0], testCase[1], distance.logNormalize), testCase[3], places = 3)
            self.assertAlmostEqual(distance.manhattanScalar(testCase[0], testCase[1], distance.logisticNormalize), testCase[4], places = 3)

    def test_manhattanBase(self):
        a = [0, 0]
        b = [0, 0]
        self.assertAlmostEqual(distance.manhattan(a, b), 0, places = 3)

        a = [1, 0]
        b = [0, 0]
        self.assertAlmostEqual(distance.manhattan(a, b), 0.462, places = 3)

        a = [0, 0]
        b = [0, 1]
        self.assertAlmostEqual(distance.manhattan(a, b), 0.462, places = 3)

        a = [0, 0]
        b = [1, 1]
        self.assertAlmostEqual(distance.manhattan(a, b), 0.761594, places = 3)

    def test_levenshteinBase(self):

        a = ''
        b = ''
        self.assertAlmostEqual(distance.levenshtein(a, b), 0, places = 3)

        a = 'abc'
        b = 'abc'
        self.assertAlmostEqual(distance.levenshtein(a, b), 0, places = 3)

        a = 'abcd'
        b = 'abc'
        self.assertAlmostEqual(distance.levenshtein(a, b), 0.25, places = 3)

        a = 'abc'
        b = 'abd'
        self.assertAlmostEqual(distance.levenshtein(a, b), 0.33333, places = 3)

        a = 'ab'
        b = 'abc'
        self.assertAlmostEqual(distance.levenshtein(a, b), 0.33333, places = 3)

        a = ''
        b = 'abc'
        self.assertAlmostEqual(distance.levenshtein(a, b), 1, places = 3)

        a = 'abc'
        b = ''
        self.assertAlmostEqual(distance.levenshtein(a, b), 1, places = 3)

        a = 'abc'
        b = 'xyz'
        self.assertAlmostEqual(distance.levenshtein(a, b), 1, places = 3)

    def test_needleman_wunschBase(self):
        a = ''
        b = ''
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 0, places = 3)

        a = 'ab'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 0, places = 3)

        a = 'b'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 0.5, places = 3)

        a = 'a'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 0.5, places = 3)

        a = 'ac'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 0.5, places = 3)

        a = 'ca'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 0.75, places = 3)   

        a = 'c'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 1, places = 3) 

        a = ''
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 1, places = 3)  

        a = 'ab'
        b = ''
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 1, places = 3)  

        a = 'cd'
        b = 'ab'
        self.assertAlmostEqual(distance.needleman_wunsch(a, b), 1, places = 3)               

    def test_jaccard(self):
        a = ['a','b']
        b = ['a','b']
        self.assertAlmostEqual(distance.jaccard(a, b), 0, places = 3)  

        a = []
        b = []
        self.assertAlmostEqual(distance.jaccard(a, b), 0, places = 3)  
       
        a = ['a']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.jaccard(a, b), 0.5, places = 3)  

        a = ['b']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.jaccard(a, b), 0.5, places = 3)  

        a = ['a', 'c']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.jaccard(a, b), 0.666666, places = 3) 

        a = ['c']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.jaccard(a, b), 1, places = 3)  

        a = []
        b = ['a', 'b']
        self.assertAlmostEqual(distance.jaccard(a, b), 1, places = 3)  

        a = ['a', 'b']
        b = []
        self.assertAlmostEqual(distance.jaccard(a, b), 1, places = 3)  

        a = ['c', 'd']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.jaccard(a, b), 1, places = 3) 


    def test_dice(self):
        a = []
        b = []
        self.assertAlmostEqual(distance.dice(a, b), 0, places = 3)  

        a = ['a', 'b']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 0, places = 3)  

        a = ['a']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 0.333333, places = 3)  

        a = ['b']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 0.333333, places = 3)  

        a = ['a', 'c']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 0.5, places = 3)  

        a = []
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 1, places = 3)  

        a = ['a', 'b']
        b = []
        self.assertAlmostEqual(distance.dice(a, b), 1, places = 3)  

        a = ['c']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 1, places = 3)  

        a = ['c', 'd']
        b = ['a', 'b']
        self.assertAlmostEqual(distance.dice(a, b), 1, places = 3)  


    def test_jacardExtend(self):
        a = []
        b = []
        self.assertAlmostEqual(distance.jacardExtend(a, b), 0, places = 3)  

        a = [True, False]
        b = [True, False]
        self.assertAlmostEqual(distance.jacardExtend(a, b), 0, places = 3)  

        a = [False]
        b = [False, True]
        self.assertAlmostEqual(distance.jacardExtend(a, b), 0.5, places = 3)  

        a = [True, False]
        b = [False, True]
        self.assertAlmostEqual(distance.jacardExtend(a, b), 1, places = 3)  

    def test_diceExtend(self):
        a = []
        b = []
        self.assertAlmostEqual(distance.diceExtend(a, b), 0, places = 3)  

        a = [True, False]
        b = [True, False]
        self.assertAlmostEqual(distance.diceExtend(a, b), 0, places = 3)  

        a = [False]
        b = [False, True]
        self.assertAlmostEqual(distance.diceExtend(a, b), 0.333333, places = 3)  

        a = [True, False]
        b = [False, True]
        self.assertAlmostEqual(distance.diceExtend(a, b), 1, places = 3) 


if __name__ == '__main__':
    unittest.main()
