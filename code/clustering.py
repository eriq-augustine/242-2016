import business
import distance

import collections
import random

# All clustering classes have a cluster() method.

K_MEANS_DEFAULT_MAX_STEPS = 10

# TODO(eriq): agglomerative clustering

# KMeans will only support numeric features.
class KMeans:
    def __init__(self, k, pairwiseDistance, maxSteps = K_MEANS_DEFAULT_MAX_STEPS):
        self.k = k
        # Don't refer to this directly, instead use calculatePairwiseDistance().
        self._pairwiseDistanceFunction = pairwiseDistance
        self._maxSteps = maxSteps

    # |points| must have a property called "features" which is the
    # features to compare on.
    def cluster(self, points):
        distances = self.calculatePairwiseDistances(points)
        centroids = self.selectInitialCentroids(points, distances)

        for i in range(self._maxSteps):
            newClusters = [[] for x in centroids]
            for point in points:
                # Assign to the closest centroid
                newClusters[self.closestPointIndex(centroids, point, distances)].append(point)

            # Recompute centroids
            newCentroids = self.recomputeCentroids(newClusters, distances)

            # TODO(eriq): Do an actual check for halting.
            #  Probably cluster membership change (watch for jittering).

            clusters = newClusters
            centroids = newCentroids

        return clusters

    def calculatePairwiseDistance(self, a, b):
        return self._pairwiseDistanceFunction(a.features, b.features)

    # Find the point in |points| closest to |queryPoint|.
    def closestPointIndex(self, points, queryPoint, distances):
        closestIndex = -1
        minDistance = -1
        for i in range(len(points)):
            distance = distances.get(points[i].id, queryPoint.id)
            if (closestIndex == -1 or distance < minDistance):
                closestIndex = i
                minDistance = distance

        return closestIndex

    def recomputeCentroids(self, clusters, distances):
        centroids = []
        for cluster in clusters:
            index = self.getPairwiseCentroidIndex(cluster, distances)
            centroids.append(cluster[index])

        return centroids

    # Given all the points, find the point that has the minimum distance to all the other points.
    def getPairwiseCentroidIndex(self, points, distances):
        index = -1
        minDistance = -1
        for i in range(len(points)):
            totalDistance = 0
            for j in range(len(points)):
                if (i != j):
                    totalDistance += distances.get(points[i].id, points[j].id)

            if (index == -1 or totalDistance < minDistance):
                index = i
                minDistance = totalDistance

        return index

    # Get the summed distance between one point and a group of points.
    def getTotalDistance(self, queryPoint, points, distances):
        totalDistance = 0
        for point in points:
            totalDistance += distances.get(queryPoint.id, point.id)
        return totalDistance

    # Select centroids by:
    #   - Select dataset centroid, DC
    #   - Pick max distance from DC as first centroid.
    #   - Pick all subsequent centroids by maxing distance from all current centroids.
    def selectInitialCentroids(self, points, distances):
        # Start with the dataset centroid
        centroidIndexes = [self.getPairwiseCentroidIndex(points, distances)]
        centroids = [points[centroidIndexes[0]]]

        # For all the other centroids, pick the point that maximizes the distance from all current centroids.
        for i in range(1, self.k):
            # Bail out if no more points are left
            if (len(centroids) >= len(points)):
                break

            index = -1
            maxDistance = -1
            for j in range(len(points)):
                if (j in centroidIndexes):
                    continue

                distance = self.getTotalDistance(points[j], centroids, distances)
                if (index == -1 or distance > maxDistance):
                    index = j
                    maxDistance = distance

            centroidIndexes.append(index)
            centroids.append(points[index])

        return centroids

    # Calculate all the pairwise distances.
    # This assumes that distance is symmetric.
    def calculatePairwiseDistances(self, points):
        distances = SymmetricDistances()

        for i in range(len(points)):
            for j in range(i):
                distances.put(points[i].id, points[j].id, self.calculatePairwiseDistance(points[i], points[j]))

        return distances

# Keep track of pairwise distances that are symmetric (ie. the order of the indexes does not matter.
# This not only assumes symmetry, but also that a point has a zero distance to itself.
class SymmetricDistances:
    def __init__(self):
        self._distances = collections.defaultdict(dict)

    def put(self, i, j, val):
        if (i == j):
            if (val != 0):
                raise Exception("Cannot put a non-zero distance in a SymmetricDistances object")
            return
            
        small = min(i, j)
        big = max(i, j)

        self._distances[small][big] = val

    def get(self, i, j):
        if (i == j):
            return 0

        small = min(i, j)
        big = max(i, j)

        return self._distances[small][big]


if __name__ == '__main__':
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

    kMeans = KMeans(3, distance.euclidean)
    clusters = kMeans.cluster(data)

    for i in range(len(clusters)):
        print("Cluster: %02d, Size: %02d - %s" % (i, len(clusters[i]), [str(x.id) for x in clusters[i]]))
