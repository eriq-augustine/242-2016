import business
import distance

import random

# All clustering classes have a cluster() method.

K_MEANS_DEFAULT_MAX_STEPS = 10

# TODO(eriq): agglomerative clustering

# KMeans will only support numeric features.
class KMeans:
    def __init__(self, k, pairwiseDistance, maxSteps = K_MEANS_DEFAULT_MAX_STEPS):
        self.k = k
        # Don't refer to this directly, instead use calculatePairwiseDistance().
        self._pairwiseDistance = pairwiseDistance
        self.maxSteps = maxSteps
        self.centroids = []

    # |points| must have a property called "features" which is the
    # features to compare on.
    def cluster(self, points):
        centroids = self.selectInitialCentroids(points)

        for i in range(self.maxSteps):
            newClusters = [[] for x in centroids]
            for point in points:
                # Assign to the closest centroid
                newClusters[self.closestPointIndex(centroids, point)].append(point)

            # Recompute centroids
            newCentroids = self.recomputeCentroids(newClusters)

            # TODO(eriq): Do an actual check for halting.
            #  Probably cluster membership change (watch for jittering).

            clusters = newClusters
            centroids = newCentroids

        return clusters

    def calculatePairwiseDistance(self, a, b):
        return self._pairwiseDistance(a.features, b.features)

    # Find the point in |points| closest to |queryPoint|.
    def closestPointIndex(self, points, queryPoint):
        closestIndex = -1
        minDistance = -1
        for i in range(len(points)):
            distance = self.calculatePairwiseDistance(points[i], queryPoint)
            if (closestIndex == -1 or distance < minDistance):
                closestIndex = i
                minDistance = distance

        return closestIndex

    # TODO(eriq): We have to decide if we are going to use theoretical or actual centroids.
    #  With actual, then we only need pairwise distances.
    #  With theoretical, the clusters will probably be better, but we have to make sure everything is numeric.
    def recomputeCentroids(self, clusters):
        centroids = []
        for cluster in clusters:
            index = self.getPairwiseCentroidIndex(cluster)
            centroids.append(cluster[index])

        return centroids

    # Given all the points, find the point that has the minimum distance to all the other points.
    def getPairwiseCentroidIndex(self, points):
        index = -1
        minDistance = -1
        for i in range(len(points)):
            totalDistance = 0
            for j in range(len(points)):
                if (i != j):
                    totalDistance += self.calculatePairwiseDistance(points[i], points[j])

            if (index == -1 or totalDistance < minDistance):
                index = i
                minDistance = totalDistance

        return index

    # Get the summed distance between one point and a group of points.
    def getTotalDistance(self, queryPoint, points):
        totalDistance = 0
        for point in points:
            totalDistance += self.calculatePairwiseDistance(queryPoint, point)
        return totalDistance

    # Select centroids by:
    #   - Select dataset centroid, DC
    #   - Pick max distance from DC as first centroid.
    #   - Pick all subsequent centroids by maxing distance from all current centroids.
    def selectInitialCentroids(self, points):
        # Start with the datasent centroid
        centroidIndexes = [self.getPairwiseCentroidIndex(points)]
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

                distance = self.getTotalDistance(points[j], centroids)
                if (index == -1 or distance > maxDistance):
                    index = j
                    maxDistance = distance

            centroidIndexes.append(index)
            centroids.append(points[index])

        return centroids

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
