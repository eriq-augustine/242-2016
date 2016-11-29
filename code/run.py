import clustering
import distance
import features
import metrics

# Arbitrary k at this point.
K = 10

def run():
    businesses = features.getBusinesses()

    # Arbitrary K
    kMeans = clustering.KMeans(K, distance.euclidean)
    clusters = kMeans.cluster(businesses)

    #Metrics
    goldLabel = metrics.readGoldLabel("../data/groundtruth")
    b_cluster = metrics.getClusterBusinessID(businesses, clusters)
    randIndex = metrics.randIndex(b_cluster, goldLabel)
    print("rand index:"  + str(randIndex))

    
if __name__ == '__main__':
    run()
