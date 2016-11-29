import distance

class FeatureDistanceMap:
    def __init__(self):
        self._distanceMetrics = []

    def distance(self, businessA, businessB):
        return distance.euclidean(businessA.features, businessB.features)
