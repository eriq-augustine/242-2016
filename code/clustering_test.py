import unittest

import business
import clustering
import distance
import featureDistanceMap

class TestClustering(unittest.TestCase):
    def test_kmeansBase(self):
        data = [
            business.Business(10, [0, 0, 0]),
            business.Business(20, [1, 1, 1]),
            business.Business(30, [2, 2, 2]),

            business.Business(411, [10, 10, 10]),
            business.Business(511, [11, 11, 11]),
            business.Business(611, [12, 12, 12]),

            business.Business(7123, [110, 110, 110]),
            business.Business(8123, [111, 111, 111]),
            business.Business(9123, [112, 112, 112])
        ]

        expected = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8]
        ]

        manhattan = lambda a, b: distance.manhattan([a], [b])
        kMeans = clustering.KMeans(3, featureDistanceMap.FeatureDistanceMap([manhattan, manhattan, manhattan]))
        self.assertEqual(sorted(kMeans.cluster(data)), sorted(expected))

if __name__ == '__main__':
    unittest.main()
