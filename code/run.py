import clustering
import data
import featureDistanceMap
import features
import metrics

import argparse

# Arbitrary k at this point.
K = 10

def run(businessType):
    businesses = features.getBusinesses(businessType)

    # Arbitrary K
    kMeans = clustering.KMeans(K, featureDistanceMap.FeatureDistanceMap())
    clusters = kMeans.cluster(businesses)

    for i in range(len(clusters)):
        print("Cluster: %02d, Size: %02d" % (i, len(clusters[i])))
        print("         %s" % (", ".join([str(x) for x in sorted([businesses[index].otherInfo['name'] for index in clusters[i]])])))

    # Metrics
    goldLabel = metrics.readGoldLabel("../data/groundtruth")
    b_cluster = metrics.getClusterBusinessID(businesses, clusters)
    randIndex = metrics.oldRandIndex(b_cluster, goldLabel)
    print("Old Rand Index: "  + str(randIndex))

    print("New Rand Index: %f" % (metrics.randIndex(clusters, businesses)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("businessType",
                        help = "%s, %s, %s, %s, %s, %s" % (
                            data.DATA_SOURCE_DATABASE,
                            data.DATA_SOURCE_GROUNDTRUTH_ALL,
                            data.DATA_SOURCE_GROUNDTRUTH_100,
                            data.DATA_SOURCE_GROUNDTRUTH_200,
                            data.DATA_SOURCE_RESTAURANTS,
                            data.DATA_SOURCE_HUMAN_EVAL
                        ),
                        nargs = '?',
                        default = data.DATA_SOURCE_GROUNDTRUTH_200)
    args = parser.parse_args()
    run(args.businessType)
