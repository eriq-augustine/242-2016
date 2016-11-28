import business
import distance

import array
import random

# All clustering classes have a cluster() method.

K_MEANS_DEFAULT_MAX_STEPS = 10

# TODO(eriq): agglomerative clustering

# Optimizations:
#  - Only hold the full points until the distances are calculated.
#  - Precomputes and caches all pairwise distances.
#  - Holds all pairwise distances as a single array representing a skew-symmetric matrix.
#  - Only passes around indexes on the original input.
class KMeans:
    def __init__(self, k, pairwiseDistance, maxSteps = K_MEANS_DEFAULT_MAX_STEPS):
        self._k = k
        # Don't refer to this directly, instead use calculatePairwiseDistance().
        self._pairwiseDistanceFunction = pairwiseDistance
        self._maxSteps = maxSteps
        self._clusters = None

        # These will be cleared each run.
        self._numPoints = 0
        self._distances = None

    # |points| must have a property called "features" which is the
    # features to compare on.
    # Will return a list of list of indexes into the original list representing the clusters.
    def cluster(self, points):
        if (self._clusters != None):
            return clusters

        self._numPoints = len(points)
        self._distances = self.calculatePairwiseDistances(points)

        self._clusters = self.kmeans()

        self._numPoints = 0
        self._distances = None

        return self._clusters

    def kmeans(self):
        centroids = self.selectInitialCentroids()

        clusters = None
        # These are clusters from the run before the previous run
        # (2 runs old after the new clusters are computed.)
        # This will be checked against to ensure we have no jittering
        # (a point moving between two different clusters which can prevent us from halting early).
        oldClusters = None

        stop = False
        for i in range(self._maxSteps):
            newClusters = [[] for x in centroids]
            for pointIndex in range(self._numPoints):
                # Assign to the closest centroid
                newClusters[self.closestPointIndex(centroids, pointIndex)].append(pointIndex)

            # Recompute centroids
            newCentroids = self.recomputeCentroids(newClusters)

            # Check to see if we should end early (but wait for at least two cycles).
            if (oldClusters != None and self.checkForStop(oldClusters, clusters, newClusters)):
                stop = True

            oldClusters = clusters
            clusters = newClusters
            centroids = newCentroids

            if (stop):
                break

        return clusters

    def checkForStop(self, oldClusters, clusters, newClusters):
        if (oldClusters == None or clusters == None):
            return False

        # Check set membership.

        # Convert the clusters from [[int, ...], ...] to set["id, id, ...", ...]
        oldClustersSet = set([" ".join([str(x) for x in sorted(cluster)]) for cluster in oldClusters])
        clustersSet =    set([" ".join([str(x) for x in sorted(cluster)]) for cluster in clusters])
        newClustersSet = set([" ".join([str(x) for x in sorted(cluster)]) for cluster in newClusters])

        return newClustersSet == clustersSet or newClustersSet == oldClustersSet

    # Find the index of the pointIndex in |pointIndices| closest to |queryPointIndex|.
    def closestPointIndex(self, pointIndices, queryPointIndex):
        closestIndex = -1
        minDistance = -1
        for i in range(len(pointIndices)):
            distance = self._distances.get(pointIndices[i], queryPointIndex)
            if (closestIndex == -1 or distance < minDistance):
                closestIndex = i
                minDistance = distance

        return closestIndex

    def recomputeCentroids(self, clusters):
        centroids = []
        for cluster in clusters:
            centroids.append(self.getPairwiseCentroid(cluster))

        return centroids

    # Given all the points, find the point that has the minimum distance to all the other points.
    def getPairwiseCentroid(self, pointIndices):
        index = -1
        minDistance = -1
        for i in range(len(pointIndices)):
            totalDistance = 0
            for j in range(len(pointIndices)):
                if (i != j):
                    totalDistance += self._distances.get(pointIndices[i], pointIndices[j])

            if (index == -1 or totalDistance < minDistance):
                index = i
                minDistance = totalDistance

        return pointIndices[index]

    # Get the summed distance between one point and a group of points.
    def getTotalDistance(self, queryPointIndex, pointIndices):
        totalDistance = 0
        for pointIndex in pointIndices:
            totalDistance += self._distances.get(queryPointIndex, pointIndex)
        return totalDistance

    # Select centroids by:
    #   - Select dataset centroid, DC
    #   - Pick max distance from DC as first centroid.
    #   - Pick all subsequent centroids by maxing distance from all current centroids.
    def selectInitialCentroids(self):
        # Start with the dataset centroid
        centroids = [self.getPairwiseCentroid(range(self._numPoints))]

        # For all the other centroids, pick the point that maximizes the distance from all current centroids.
        for i in range(1, self._k):
            # Bail out if no more points are left
            if (len(centroids) >= self._numPoints):
                break

            index = -1
            maxDistance = -1
            for j in range(self._numPoints):
                if (j in centroids):
                    continue

                distance = self.getTotalDistance(j, centroids)
                if (index == -1 or distance > maxDistance):
                    index = j
                    maxDistance = distance

            centroids.append(index)

        return centroids

    # Calculate all the pairwise distances.
    # This assumes that distance is symmetric.
    def calculatePairwiseDistances(self, points):
        distances = SymmetricDistances(len(points))

        for i in range(self._numPoints):
            for j in range(i):
                distances.put(i, j, self.calculatePairwiseDistance(points[i], points[j]))

        return distances

    def calculatePairwiseDistance(self, a, b):
        return self._pairwiseDistanceFunction(a.features, b.features)

# Keep track of pairwise distances that are symmetric (ie. the order of the indexes does not matter.
# This not only assumes symmetry, but also that a point has a zero distance to itself.
class SymmetricDistances:
    # Size should be the total number of objects, not the squared size or anything.
    def __init__(self, size):
        self._size = size
        # We are minimizing memory usage here.
        # If we want to use something smaller than a standard float, we will need to go with numpy.
        # We will use one array of size (n * (n - 1) / 2).
        # Note that the int cast is safe since we are multiplying an odd by even.
        self._distances = array.array('f', int(size * (size - 1) / 2) * [0])

    # We have a skew-symmetric matrix held as a single array.
    # The index is given by: (row * size) + col - rowModifier(row)
    # Where rowModifier(row) is the number of total cells skipped by the current row and all before it
    # (since we are not storing the diagnol and everything below).
    # rowModifier(row) = rowModifier(row - 1) + (row + 1)
    # rowModifier(row) = 1/2 * (row + 1) * (row + 2) // Closed form.
    def _calcIndex(self, row, col):
        return row * self._size + col - int((row + 1) * (row + 2) / 2)

    def put(self, i, j, val):
        if (i == j):
            if (val != 0):
                raise Exception("Cannot put a non-zero distance in a SymmetricDistances object")
            return

        small = min(i, j)
        big = max(i, j)

        self._distances[self._calcIndex(small, big)] = val

    def get(self, i, j):
        if (i == j):
            return 0

        small = min(i, j)
        big = max(i, j)

        return self._distances[self._calcIndex(small, big)]


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
        print("Cluster: %02d, Size: %02d - %s" % (i, len(clusters[i]), [str(x) for x in sorted(clusters[i])]))
