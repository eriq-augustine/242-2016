import business
import data

# This is mainly for deciding if we are getting real or fake data.
DEBUG = True

# Query constants
COLUMN_ID = 0
COLUMN_YELP_ID = 1
COLUMN_ACTIVE = 2
COLUMN_CITY = 3
COLUMN_STATE = 4
COLUMN_NUMERIC_START = 5

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
def getBusinesses():
    features = []
    rawBusinesses = data.getBusinesses(DEBUG)

    # one-hot encoding of active, city, and state variables + numeric features
    cityStateMatrix = oneHot([{"active": b[COLUMN_ACTIVE], "city": b[COLUMN_CITY], "state": b[COLUMN_STATE]} for b in rawBusinesses])
    features = [list(rawBusinesses[i][COLUMN_NUMERIC_START:]) + cityStateMatrix[i] for i in range(len(rawBusinesses))]

    return [business.Business(rawBusinesses[i][COLUMN_ID], features[i], {"yelpId": rawBusinesses[i][COLUMN_YELP_ID]}) for i in range(len(rawBusinesses))]

if __name__ == '__main__':
    businesses = getBusinesses()
    print(businesses)
    print("0:")
    print("   " + str(businesses[0].id))
    print("   " + str(businesses[0].features))
    print("   " + str(businesses[0].otherInfo))
