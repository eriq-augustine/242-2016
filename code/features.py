import data

# This is mainly for deciding if we are getting real or fake data.
DEBUG = True

# Takes a list of maps and converts it to a single one-hot encoding.
# [{"key1": val1, "key2", val2}, ...]
# All the dictionaries must have the same keys.
def oneHot(values):
    if (len(values) == 0):
        return []

    # A mapping of keys to their respective encodings.
    # {key0: {value0: valueIndex0, value1: valueIndex1, ...}, ...}
    encodings = {}

    # Make a deterministic ordering for the keys.
    keys = sorted(values[0].keys())
    totalValues = 0

    # Build the encodings.
    for key in keys:
        encodings[key] = {}

        for value in values:
            if value[key] not in encodings[key]:
                encodings[key][value[key]] = totalValues
                totalValues += 1

    # Build up the output with all zeros.
    rtn = [[0 for x in range(totalValues)] for value in values]

    for i in range(len(values)):
        for key, value in values[i].items():
            rtn[i][encodings[key][value]] = 1

    return rtn

# TODO(dhawal): Do some feature engineering.
# As of now, we are only returning numeric features.
def getFeatures():
    features = []
    businesses = data.getBusinesses(DEBUG)

    # one-hot encoding of active, city, and state variables + numeric features
    cityStateMatrix = oneHot([{"active": b[1], "city": b[2], "state": b[3]} for b in businesses])
    features = [list(businesses[i][4:]) + cityStateMatrix[i] for i in range(len(businesses))]

    return features

if __name__ == '__main__':
    print(getFeatures())
