import clustering
import distance
import features

# Arbitrary k at this point.
K = 10

def run():
    businesses = features.getFeatures()

    # Arbitrary K
    kMeans = clustering.KMeans(K, distance.euclidean)
    clusters = kMeans.cluster(businesses)

    for cluster in clusters:
        print(len(cluster))

if __name__ == '__main__':
    run()
