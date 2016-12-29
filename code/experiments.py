import clustering
import data
import distance
import featureDistanceMap
import features
import metrics

import argparse
import sys

# N - Numeric Features
# A - "Attribute" features (attributes and categories)
# W - "Word Features"
FEATURES = ['NAW', 'NA', 'NW', 'AW', 'W', 'A', 'N']
# Weights that accomplish the above sets.
FEATURE_WEIGHTS = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
]

# All experimetnal parameters are order of importance.
KS = [10, 16, 14, 12, 18, 8]

SCALAR_NORMALIZATION = [distance.logisticNormalize, distance.logNormalize, distance.noNormalize]
SET_DISTANCE = [distance.jaccard, distance.dice]

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
    mapping[featureDistanceMap.ATTRIBUTES] = setDistance
    mapping[featureDistanceMap.CATEGORIES] = setDistance
    mapping[featureDistanceMap.TOP_WORDS] = setDistance
    mapping[featureDistanceMap.KEY_WORDS] = setDistance

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

def runAll(featureSet):
    weights = FEATURE_WEIGHTS[FEATURES.index(featureSet)]
    print("features\tK\tscalarNorm\tsetDistance\trandIndex")
    print("features\tK\tscalarNorm\tsetDistance\trandIndex", file=sys.stderr)

    for k in KS:
        for scalarNorm in SCALAR_NORMALIZATION:
            for setDistance in SET_DISTANCE:
                id = "%s\t%d\t%s\t%s" % (featureSet, k, scalarNorm.__name__, setDistance.__name__)

                try:
                    print("START: %s" % (id))
                    randIndex = run(weights, k, scalarNorm, setDistance)
                    print("%s\t%f" % (id, randIndex), file=sys.stderr)
                except Exception as ex:
                    print(ex)
                    print("Error running: %s" % (id))
                    print("%s, ERROR" % (id), file=sys.stderr)

                print("END: %s" % (id))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("featureSet", help = ", ".join(FEATURES))
    args = parser.parse_args()
    runAll(args.featureSet)
