import clustering
import data
import distance
import featureDistanceMap
import features
import metrics

import sys
import traceback

# N - Numeric Features
# A - "Attribute" features (attributes and categories)
# W - "Word Features"
FEATURES = ['AWT', 'T', 'NAWT', 'NAT', 'NWT', 'WT', 'AT', 'NT']
# Weights that accomplish the above sets.
FEATURE_WEIGHTS = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1]
]

# All experimetnal parameters are order of importance.
# KS = [10, 8, 12, 14, 16, 18]
KS = [10, 8, 12, 14, 16, 18]

# SCALAR_NORMALIZATION = [distance.logisticNormalize, distance.logNormalize]
SCALAR_NORMALIZATION = [distance.logisticNormalize]
# SET_DISTANCE = [distance.jaccard, distance.dice]
SET_DISTANCE = [distance.jaccard]

def buildFeatureMapping(scalarNormalize, setDistance):
    mapping = [None] * featureDistanceMap.NUM_FEATURES

    scalarDistance = lambda a, b: distance.manhattanScalar(a, b, scalarNormalize)

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

def run(weights, k, scalarNorm, setDistance):
    businesses = features.getBusinesses(data.DATA_SOURCE_GROUNDTRUTH_ALL)

    featureDistMap = featureDistanceMap.FeatureDistanceMap(buildFeatureMapping(scalarNorm, setDistance), weights)
    kMeans = clustering.KMeans(k, featureDistMap)
    clusters = kMeans.cluster(businesses)

    for i in range(len(clusters)):
        print("Cluster: %02d, Size: %02d" % (i, len(clusters[i])))
        print("         %s" % (", ".join([str(x) for x in sorted([businesses[index].otherInfo['yelpId'] for index in clusters[i]])])))

    goldLabel = metrics.readGoldLabel("../data/groundtruth")
    b_cluster = metrics.getClusterBusinessID(businesses, clusters)
    randIndex = metrics.oldRandIndex(b_cluster, goldLabel)

    return randIndex

def runAll():
    print("features\tK\tscalarNorm\tsetDistance\trandIndex")
    print("features\tK\tscalarNorm\tsetDistance\trandIndex", file=sys.stderr)

    for k in KS:
        for featureSet in FEATURES:
            weights = FEATURE_WEIGHTS[FEATURES.index(featureSet)]
            for scalarNorm in SCALAR_NORMALIZATION:
                for setDistance in SET_DISTANCE:
                    id = "%s\t%d\t%s\t%s" % (featureSet, k, scalarNorm.__name__, setDistance.__name__)

                    try:
                        print("START: %s" % (id))
                        randIndex = run(weights, k, scalarNorm, setDistance)
                        print("%s\t%f" % (id, randIndex), file=sys.stderr)
                    except Exception as ex:
                        print(ex)
                        traceback.print_exc()
                        print("Error running: %s" % (id))
                        print("%s, ERROR" % (id), file=sys.stderr)

                    print("END: %s" % (id))

if __name__ == '__main__':
    runAll()
