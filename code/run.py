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
        print("         %s" % (", ".join([str(x) for x in sorted([businesses[index].otherInfo['yelpId'] for index in clusters[i]])])))

    #Metrics
    goldLabel = metrics.readGoldLabel("../data/groundtruth")
    b_cluster = metrics.getClusterBusinessID(businesses, clusters)
    randIndex = metrics.randIndex(b_cluster, goldLabel)
    print("rand index:"  + str(randIndex))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("businessType",
                        help = "%s, %s, %s, %s" % (data.DATA_TYPE_DATABASE, data.DATA_TYPE_FAKE, data.DATA_TYPE_FULL, data.DATA_TYPE_TEST),
                        nargs = '?',
                        default = data.DATA_TYPE_FAKE)
    args = parser.parse_args()
    run(args.businessType)
