import business
import data

# Query constants
COLUMN_ID = 0
COLUMN_YELP_ID = 1
COLUMN_NAME = 2
COLUMN_ACTIVE = 3
COLUMN_CITY = 4
COLUMN_STATE = 5
COLUMN_STARS = 6
COLUMN_TOTAL_REVIEW_COUNT = 7
COLUMN_ATTRIBUTES = 8
COLUMN_CATEGORIES = 9
COLUMN_AVAILABLE_REVIEW_COUNT = 10
COLUMN_MEAN_REVIEW_LEN = 11
COLUMN_MEAN_WORD_LEN = 12
COLUMN_NUM_WORDS = 13
COLUMN_MEAN_WORD_COUNT = 14
COLUMN_TOP_WORDS = 15
COLUMN_KEY_WORDS = 16
COLUMN_TOTAL_HOURS = 17
COLUMN_OPEN_HOURS = 18

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

def buildMap(businesses, column):
    attributeMap = {}
    count = 0

    for business in businesses:
        for attribute in splitWithEmpty(business[column]):
            if attribute not in attributeMap:
                attributeMap[attribute] = count
                count += 1

    return attributeMap

def splitWithEmpty(val):
    return [x for x in val.split(';;') if x != '']

def extractFeatures(rawBusiness, attributeMap, categoryMap, topWordMap, keyWordMap, openHoursMap):
    featureVector = []
    numericColumns = [
        COLUMN_STARS,
        COLUMN_TOTAL_REVIEW_COUNT,
        COLUMN_AVAILABLE_REVIEW_COUNT,
        COLUMN_MEAN_REVIEW_LEN,
        COLUMN_MEAN_WORD_LEN,
        COLUMN_NUM_WORDS,
        COLUMN_MEAN_WORD_COUNT,
        COLUMN_TOTAL_HOURS
    ]

    for column in numericColumns:
        featureVector.append(rawBusiness[column])

    attributes = [attributeMap[ele] for ele in splitWithEmpty(rawBusiness[COLUMN_ATTRIBUTES])]
    featureVector.append(attributes)

    categories = [categoryMap[ele] for ele in splitWithEmpty(rawBusiness[COLUMN_CATEGORIES])]
    featureVector.append(categories)

    topWords = [topWordMap[ele] for ele in splitWithEmpty(rawBusiness[COLUMN_TOP_WORDS])]
    featureVector.append(topWords)

    keyWords = [keyWordMap[ele] for ele in splitWithEmpty(rawBusiness[COLUMN_KEY_WORDS])]
    featureVector.append(keyWords)

    openHours = [openHoursMap[ele] for ele in splitWithEmpty(rawBusiness[COLUMN_OPEN_HOURS])]
    featureVector.append(openHours)

    otherInfo = {
        "yelpId": rawBusiness[COLUMN_YELP_ID],
        "name": rawBusiness[COLUMN_NAME]
    }

    return business.Business(rawBusiness[COLUMN_ID], featureVector, otherInfo)

def getBusinesses(businessType=data.DATA_SOURCE_GROUNDTRUTH_200):
    features = []
    rawBusinesses = data.getBusinesses(businessType)

    attributeMap = buildMap(rawBusinesses, COLUMN_ATTRIBUTES)
    categoryMap = buildMap(rawBusinesses, COLUMN_CATEGORIES)
    topWordMap = buildMap(rawBusinesses, COLUMN_TOP_WORDS)
    keyWordMap = buildMap(rawBusinesses, COLUMN_KEY_WORDS)
    openHoursMap = buildMap(rawBusinesses, COLUMN_OPEN_HOURS)

    businesses = [extractFeatures(business, attributeMap, categoryMap, topWordMap, keyWordMap, openHoursMap) for business in rawBusinesses]
    return businesses

if __name__ == '__main__':
    businesses = getBusinesses()
    print(businesses)
    print("0:")
    print("   " + str(businesses[0].id))
    print("   " + str(businesses[0].features))
    print("   " + str(businesses[0].otherInfo))
