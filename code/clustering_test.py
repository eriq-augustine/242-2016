import unittest

import clustering
import distance

class TestClustering(unittest.TestCase):
    def test_kmeansBase(self):
        data = [
            [0, 0, 0],
            [1, 1, 1],
            [2, 2, 2],

            [10, 10, 10],
            [11, 11, 11],
            [12, 12, 12],

            [110, 110, 110],
            [111, 111, 111],
            [112, 112, 112]
        ]

        expected = [
            [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            [[10, 10, 10], [11, 11, 11], [12, 12, 12]],
            [[110, 110, 110], [111, 111, 111], [112, 112, 112]]
        ]

        kMeans = clustering.KMeans(3, distance.euclidean)
        self.assertEqual(sorted(kMeans.cluster(data)), sorted(expected))

if __name__ == '__main__':
    unittest.main()
