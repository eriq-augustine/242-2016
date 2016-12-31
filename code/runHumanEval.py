import clustering
import data
import featureDistanceMap
import features
import learnWeights
import metrics

K = 10

# Learned from weight learning.
# WEIGHTS = [2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.5, 2.0, 1.0, 1.0, 0.5, 1.0, 0.0]
# WEIGHTS = [0.5, 0.0, 1.0, 0.5, 0.5, 0.0, 0.5, 2.0, 3.5, 0.5, 1.0, 1.0, 0.0]
WEIGHTS = [2.0, 0.0, 0.0, 3.0, 1.0, 0.0, 1.5, 2.5, 2.5, 1.0, 0.5, 1.0, 3.5]

def run():
    businesses = features.getBusinesses(data.DATA_SOURCE_HUMAN_EVAL)

    featureDistMap = featureDistanceMap.FeatureDistanceMap(learnWeights.getFeatureMapping(), WEIGHTS)
    kMeans = clustering.KMeans(K, featureDistMap)

    # kMeans = clustering.KMeans(K, featureDistanceMap.FeatureDistanceMap())

    clusters = kMeans.cluster(businesses)

    for i in range(len(clusters)):
        print("Cluster: %02d, Size: %02d" % (i, len(clusters[i])))
        print("         %s" % (", ".join([str(x) for x in sorted([businesses[index].otherInfo['name'] for index in clusters[i]])])))

    # Metrics
    truthPairs, truthIds = metrics.getHumanTruthPairs()
    print("Rand Index: %f" % (metrics.randIndex(clusters, businesses, truthPairs, truthIds)))

if __name__ == '__main__':
    run()
