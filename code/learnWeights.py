import clustering
import data
import distance
import featureDistanceMap
import features
import metrics

import random
import sys

# We will hold weights constant and modify one at a time.
# Then we will make up to MAX_ITERATIONS passes or until the weights remain unchanged.
# The order we probe the weights will be random every iteration to prevent bias.

MAX_ITERATIONS = 30

START_WEIGHT = 1.0
MIN_WEIGHT = 0.0
WEIGHT_INCREMENT = 0.50
MAX_WEIGHT = 2.0

DATA = data.DATA_SOURCE_GROUNDTRUTH_200

K = 10
SCALAR_DISTANCE = distance.manhattanScalar
SCALAR_NORMALIZATION = distance.logisticNormalize
SET_DISTANCE = distance.jaccard

def getFeatureMapping():
    mapping = [None] * featureDistanceMap.NUM_FEATURES

    scalarDistance = lambda a, b: SCALAR_DISTANCE(a, b, SCALAR_NORMALIZATION)
    setDistance = SET_DISTANCE

    mapping[featureDistanceMap.STARS] = scalarDistance
    mapping[featureDistanceMap.TOTAL_REVIEW_COUNT] = scalarDistance
    mapping[featureDistanceMap.AVAILABLE_REVIEW_COUNT] = scalarDistance
    mapping[featureDistanceMap.MEAN_REVIEW_LEN] = scalarDistance
    mapping[featureDistanceMap.MEAN_WORD_LEN] = scalarDistance
    mapping[featureDistanceMap.NUM_WORDS] = scalarDistance
    mapping[featureDistanceMap.MEAN_WORD_COUNT] = scalarDistance
    mapping[featureDistanceMap.TOTAL_HOURS] = scalarDistance
    mapping[featureDistanceMap.ATTRIBUTES] = setDistance
    mapping[featureDistanceMap.CATEGORIES] = setDistance
    mapping[featureDistanceMap.TOP_WORDS] = setDistance
    mapping[featureDistanceMap.KEY_WORDS] = setDistance
    mapping[featureDistanceMap.OPEN_HOURS] = setDistance

    return mapping

def paramId(weights, k):
    return str((k, weights))

def runClustering(weights, k, featureFunctionMapping, businesses, truthPairs, truthIds, cache):
    cacheId = paramId(weights, k)
    if (cacheId in cache):
        return cache[cacheId]

    featureDistMap = featureDistanceMap.FeatureDistanceMap(featureFunctionMapping, weights)
    kMeans = clustering.KMeans(k, featureDistMap)

    id = "\t".join([str(weight) for weight in weights])
    randIndex = -1

    try:
        clusters = kMeans.cluster(businesses)
        randIndex = metrics.randIndex(clusters, businesses, truthPairs, truthIds)
        print("%s\t%f" % (id, randIndex), file=sys.stderr)

        '''
        for i in range(len(clusters)):
            print("Cluster: %02d, Size: %02d" % (i, len(clusters[i])))
            print("         %s" % (", ".join([str(x) for x in sorted([businesses[index].otherInfo['yelpId'] for index in clusters[i]])])))
        '''
    except Exception as ex:
        print(ex)
        print("%s\tERROR" % (id), file=sys.stderr)

    cache[cacheId] = randIndex

    return randIndex


# Recrsvley modify weights.
# Each call is responsible for a single weight.
# |weightsOrder| is a list of indexes representing the order that we will probe the weights in.
# |orderIndex| is the index into that list.
# So, the weight that each call will probe is: weights[weightsOrder[orderIndex]].
# The best randIndex of this probe will be returned.
def probeWeight(weights, weightsOrder, orderIndex, k, featureFunctionMapping, businesses, truthPairs, truthIds, cache):
    # First allow the next weight to probe.
    if (orderIndex < len(weightsOrder) - 1):
        probeWeight(weights, weightsOrder, orderIndex + 1, k, featureFunctionMapping, businesses, truthPairs, truthIds, cache)

    weight = MIN_WEIGHT
    weightIndex = weightsOrder[orderIndex]

    maxWeight = -1
    maxRandIndex = -1

    while (weight <= MAX_WEIGHT):
        weights[weightIndex] = weight
        randIndex = runClustering(weights, k, featureFunctionMapping, businesses, truthPairs, truthIds, cache)

        if (maxWeight == -1 or randIndex > maxRandIndex):
            maxWeight = weight
            maxRandIndex = randIndex

        weight += WEIGHT_INCREMENT

    weights[weightIndex] = maxWeight
    return maxRandIndex

def main():
    businesses = features.getBusinesses(DATA)
    truthPairs, truthIds = metrics.getGoldTruthPairs()

    weights = [START_WEIGHT] * featureDistanceMap.NUM_FEATURES
    # weights = featureDistanceMap.DEFAULT_WEIGHTS
    featureFunctionMapping = getFeatureMapping()

    cache = {}

    oldWeights = list(weights)
    for iteration in range(MAX_ITERATIONS):
        weightsOrder = list(range(len(weights)))
        random.shuffle(weightsOrder)

        randIndex = probeWeight(weights, weightsOrder, 0, K, featureFunctionMapping, businesses, truthPairs, truthIds, cache)

        if (oldWeights == weights):
            break

        oldWeights = list(weights)

    id = "\t".join([str(weight) for weight in weights])
    print("Converged in %d / %d iterations" % (iteration + 1, MAX_ITERATIONS))
    print("Final Weights: %s\t%f" % (id, randIndex), file=sys.stderr)

if __name__ == '__main__':
    main()
