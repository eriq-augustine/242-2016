import distance

STARS = 0
TOTAL_REVIEW_COUNT = 1
AVAILABLE_REVIEW_COUNT = 2
MEAN_REVIEW_LEN = 3
MEAN_WORD_LEN = 4
NUM_WORDS = 5
MEAN_WORD_COUNT = 6
ATTRIBUTES = 7
CATEGORIES = 8
TOP_WORDS = 9
KEY_WORDS = 10
NUM_FEATURES = 11

class FeatureDistanceMap:
    def __init__(self, mappings = None):
        self._distanceMetrics = {
            'euclidean': lambda a, b: distance.euclidean([a], [b]),
            'manhattan': distance.manhattanScalar,
            'levenshtein': lambda a, b: distance.levenshtein([a], [b]),
            'needleman_wunsch': lambda a, b: distance.needleman_wunsch([a], [b]),
            'jaccard': distance.jaccard
        }

        self._mapping = mappings
        if mappings == None:
            self._mapping = [None] * NUM_FEATURES
            self._mapping[STARS] = self._distanceMetrics['manhattan']
            self._mapping[TOTAL_REVIEW_COUNT] = self._distanceMetrics['manhattan']
            self._mapping[AVAILABLE_REVIEW_COUNT] = self._distanceMetrics['manhattan']
            self._mapping[MEAN_REVIEW_LEN] = self._distanceMetrics['manhattan']
            self._mapping[MEAN_WORD_LEN] = self._distanceMetrics['manhattan']
            self._mapping[NUM_WORDS] = self._distanceMetrics['manhattan']
            self._mapping[MEAN_WORD_COUNT] = self._distanceMetrics['manhattan']
            self._mapping[ATTRIBUTES] = self._distanceMetrics['jaccard']
            self._mapping[CATEGORIES] = self._distanceMetrics['jaccard']
            self._mapping[TOP_WORDS] = self._distanceMetrics['jaccard']
            self._mapping[KEY_WORDS] = self._distanceMetrics['jaccard']

    def distance(self, businessA, businessB):
        sum = 0
        for i in range(len(self._mapping)):
            sum += self._mapping[i](businessA.features[i], businessB.features[i])
        return sum
