import clustering
import data
import distance
import featureDistanceMap
import features
import metrics

import sys

START_WEIGHT = 0.0
WEIGHT_INCREMENT = 1.0
END_WEIGHT = 2.0

DATA = data.DATA_TYPE_FAKE

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

def run(weights, k, featureFunctionMapping, businesses, goldLabel):
    featureDistMap = featureDistanceMap.FeatureDistanceMap(featureFunctionMapping, weights)
    kMeans = clustering.KMeans(k, featureDistMap)

    id = "\t".join([str(weight) for weight in weights])

    try:
        print("START: %s" % (id))
        clusters = kMeans.cluster(businesses)
        b_cluster = metrics.getClusterBusinessID(businesses, clusters)
        randIndex = metrics.randIndex(b_cluster, goldLabel)
        print("%s\t%f" % (id, randIndex), file=sys.stderr)

        '''
        for i in range(len(clusters)):
            print("Cluster: %02d, Size: %02d" % (i, len(clusters[i])))
            print("         %s" % (", ".join([str(x) for x in sorted([businesses[index].otherInfo['yelpId'] for index in clusters[i]])])))
        '''
    except Exception as ex:
        print(ex)
        print("Error running: %s" % (id))
        print("%s\tERROR" % (id), file=sys.stderr)

    print("END: %s" % (id))


# Recrsvley modify weights for all combinations.
# Each call is responsible for a single weight.
def runWeight(weights, weightIndex, k, featureFunctionMapping, businesses, goldLabel):
    if (weightIndex == len(weights)):
        # We collected all the weights.
        run(weights, k, featureFunctionMapping, businesses, goldLabel)
        return

    assert(weights[weightIndex] == START_WEIGHT)

    weight = START_WEIGHT
    while (weight <= END_WEIGHT):
        weights[weightIndex] = weight
        runWeight(weights, weightIndex + 1, k, featureFunctionMapping, businesses, goldLabel)
        weight += WEIGHT_INCREMENT

    # Cleanup
    # This is not actually necessary, but will provide a good spot check.
    weights[weightIndex] = START_WEIGHT

def main():
    businesses = features.getBusinesses(DATA)
    goldLabel = metrics.readGoldLabel("../data/groundtruth")

    initialWeights = [START_WEIGHT] * featureDistanceMap.NUM_FEATURES
    featureFunctionMapping = getFeatureMapping()

    print("features\tK\tscalarNorm\tsetDistance\trandIndex")
    print("features\tK\tscalarNorm\tsetDistance\trandIndex", file=sys.stderr)

    runWeight(initialWeights, 0, K, featureFunctionMapping, businesses, goldLabel)


if __name__ == '__main__':
    main()
