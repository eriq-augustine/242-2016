import distance

import random

# All clustering classes have a cluster() method.

K_MEANS_DEFAULT_MAX_STEPS = 10

# TODO(eriq): agglomerative clustering

# KMeans will only support numeric features.
class KMeans:
    def __init__(self, k, pairwiseDistance, maxSteps = K_MEANS_DEFAULT_MAX_STEPS):
        self.k = k
        self.pairwiseDistance = pairwiseDistance
        self.maxSteps = maxSteps
        self.centroids = []

    def cluster(self, points):
        centroids = self.selectInitialCentroids(points)

        for i in range(self.maxSteps):
            newClusters = [[] for x in centroids]
            for point in points:
                # Assign to the closest centroid
                newClusters[self.closestCentroidIndex(centroids, point)].append(point)

            # Recompute centroids
            newCentroids = self.recomputeCentroids(newClusters)

            # TODO(eriq): Do an actual check for halting.
            #  Probably cluster membership change (watch for jittering).

            clusters = newClusters
            centroids = newCentroids

        return clusters

    def closestCentroidIndex(self, centroids, point):
        closestIndex = -1
        minDistance = -1
        for i in range(len(centroids)):
            distance = self.pairwiseDistance(centroids[i], point)
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
            centroidIndex = -1
            minDistance = -1
            for i in range(len(cluster)):
                totalDistance = 0
                for j in range(len(cluster)):
                    if (i != j):
                        totalDistance += self.pairwiseDistance(cluster[i], cluster[j])

                if (centroidIndex == -1 or totalDistance < minDistance):
                    centroidIndex = i
                    minDistance = totalDistance

            centroids.append(cluster[i])

        return centroids

    # TODO(eriq): Select centroids by:
    #   - Select dataset centroid, DC
    #   - Pick max distance from DC as first centroid.
    #   - Pick all subsequent centroids by maxing distance from all current centroids.
    def selectInitialCentroids(self, points):
        return random.sample(points, self.k)

if __name__ == '__main__':
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

    kMeans = KMeans(3, distance.euclidean)
    print(kMeans.cluster(data))
