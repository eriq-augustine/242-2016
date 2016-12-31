import distance

STARS = 0
TOTAL_REVIEW_COUNT = 1
AVAILABLE_REVIEW_COUNT = 2
MEAN_REVIEW_LEN = 3
MEAN_WORD_LEN = 4
NUM_WORDS = 5
MEAN_WORD_COUNT = 6
TOTAL_HOURS = 7
ATTRIBUTES = 8
CATEGORIES = 9
TOP_WORDS = 10
KEY_WORDS = 11
OPEN_HOURS = 12
NUM_FEATURES = 13

# DEFAULT_WEIGHTS = [1.0, 0.0, 2.0, 0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 1.0, 1.5, 0.0]
# DEFAULT_WEIGHTS = [2.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.5, 2.0, 1.0, 1.0, 0.5, 1.0, 0.0]
# DEFAULT_WEIGHTS = [0.5, 0.0, 1.0, 0.5, 0.5, 0.0, 0.5, 2.0, 3.5, 0.5, 1.0, 1.0, 0.0]
DEFAULT_WEIGHTS = [2.0, 0.0, 0.0, 3.0, 1.0, 0.0, 1.5, 2.5, 2.5, 1.0, 0.5, 1.0, 3.5]

class FeatureDistanceMap:
    def __init__(self, mapping = None, weights = None):
        self._distanceMetrics = {
            'euclidean': lambda a, b: distance.euclidean([a], [b]),
            'manhattan': distance.manhattanScalar,
            'levenshtein': lambda a, b: distance.levenshtein([a], [b]),
            'needleman_wunsch': lambda a, b: distance.needleman_wunsch([a], [b]),
            'jaccard': distance.jaccard,
            'dice': distance.dice
        }

        self._mapping = mapping
        if (self._mapping == None):
            self._mapping = [None] * NUM_FEATURES
            self._mapping[STARS] = self._distanceMetrics['manhattan']
            self._mapping[TOTAL_REVIEW_COUNT] = self._distanceMetrics['manhattan']
            self._mapping[AVAILABLE_REVIEW_COUNT] = self._distanceMetrics['manhattan']
            self._mapping[MEAN_REVIEW_LEN] = self._distanceMetrics['manhattan']
            self._mapping[MEAN_WORD_LEN] = self._distanceMetrics['manhattan']
            self._mapping[NUM_WORDS] = self._distanceMetrics['manhattan']
            self._mapping[MEAN_WORD_COUNT] = self._distanceMetrics['manhattan']
            self._mapping[TOTAL_HOURS] = self._distanceMetrics['manhattan']
            self._mapping[ATTRIBUTES] = self._distanceMetrics['jaccard']
            self._mapping[CATEGORIES] = self._distanceMetrics['jaccard']
            self._mapping[TOP_WORDS] = self._distanceMetrics['jaccard']
            self._mapping[KEY_WORDS] = self._distanceMetrics['jaccard']
            self._mapping[OPEN_HOURS] = self._distanceMetrics['jaccard']

        self._weights = weights
        if (self._weights == None):
            self._weights = [1] * NUM_FEATURES

    def distance(self, businessA, businessB):
        sum = 0
        for i in range(len(self._mapping)):
            if (self._weights[i] == 0):
                continue
            sum += (1.0 / self._weights[i]) * self._mapping[i](businessA.features[i], businessB.features[i])
        return sum
