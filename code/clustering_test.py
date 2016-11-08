import unittest

import business
import clustering
import distance

class TestClustering(unittest.TestCase):
    def test_kmeansBase(self):
        data = [
            business.Business(1, [0, 0, 0]),
            business.Business(2, [1, 1, 1]),
            business.Business(3, [2, 2, 2]),

            business.Business(4, [10, 10, 10]),
            business.Business(5, [11, 11, 11]),
            business.Business(6, [12, 12, 12]),

            business.Business(7, [110, 110, 110]),
            business.Business(8, [111, 111, 111]),
            business.Business(9, [112, 112, 112])
        ]

        expected = [
            [
                business.Business(1, [0, 0, 0]),
                business.Business(2, [1, 1, 1]),
                business.Business(3, [2, 2, 2])
            ],
            [
                business.Business(4, [10, 10, 10]),
                business.Business(5, [11, 11, 11]),
                business.Business(6, [12, 12, 12])
            ],
            [
                business.Business(7, [110, 110, 110]),
                business.Business(8, [111, 111, 111]),
                business.Business(9, [112, 112, 112])
            ]
        ]

        kMeans = clustering.KMeans(3, distance.euclidean)
        self.assertEqual(sorted(kMeans.cluster(data)), sorted(expected))

if __name__ == '__main__':
    unittest.main()
