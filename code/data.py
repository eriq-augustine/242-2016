import pickle

# If you use the db, then you will need a file (secrets.py) that defines: DB_HOST, DB_PORT, DB_USER, and DB_PASS

GROUND_TRUTH_200_FILE = 'data/groundTruth_200.pickle'
GROUND_TRUTH_100_FILE = 'data/groundTruth_100.pickle'
RESTAURANTS_FILE = 'data/restaurants.pickle'
GROUND_TRUTH_ALL_FILE = 'data/groundTruth_all.pickle'
HUMAN_EVAL_FILE = 'data/humanEval.pickle'

DATA_SOURCE_DATABASE = 'database'
DATA_SOURCE_GROUNDTRUTH_100 = 'groundtruth100'
DATA_SOURCE_GROUNDTRUTH_200 = 'groundtruth200'
DATA_SOURCE_RESTAURANTS = 'restaurants'
DATA_SOURCE_GROUNDTRUTH_ALL = 'groundtruth'
DATA_SOURCE_HUMAN_EVAL = 'humaneval'

QUERY_BUSINESSES = '''
    SELECT
        B.id,
        B.yelpId,
        B.name,
        B.active,
        B.city,
        B.state,
        B.stars,
        B.reviewCount AS totalReviewCount,
        COALESCE(A.value, '') AS attributes,
        COALESCE(C.value, '') AS categories,
        COALESCE(R.availableReviewCount, 0) AS availableReviewCount,
        COALESCE(R.meanReviewLen, 0) AS meanReviewLen,
        COALESCE(W.meanWordLen, 0) AS meanWordLen,
        COALESCE(W.numWords, 0) AS numWords,
        COALESCE(W.numWords / R.availableReviewCount, 0) AS meanWordCount,
        COALESCE(RSP.topWords, '') AS topWords,
        COALESCE(RSP.keyWords, '') AS keyWords,
        COALESCE(T.totalHours, 0) AS totalHours,
        COALESCE(OH.openHours, '') AS openHours
    FROM
        Businesses B
        -- To limit businesses to only the test set, uncomment this.
        -- JOIN GroundTruth GT ON GT.businessId = B.id
        -- To use a random (but seeded) subset of the ground truth (size: 200ish), uncomment this.
        -- JOIN GroundTruth GT
        --     TABLESAMPLE BERNOULLI(200.0 / (SELECT COUNT(*) FROM GroundTruth) * 100) REPEATABLE(4)
        --     ON GT.businessId = B.id

        -- To limit businesses to only the human eval set, uncomment this.
        -- JOIN HumanEval HE ON HE.businessId = B.id

        JOIN (
            SELECT DISTINCT businessId
            FROM BusinessCategories BC
            WHERE name IN (
                'Restaurants', 'Food', 'Fast Food', 'Pizza', 'Mexican',
                'Sandwiches', 'American (Traditional)', 'Burgers', 'Italian',
                'Chinese', 'American (New)', 'Breakfast & Brunch', 'Cafes'
            )
        ) Restaurants ON Restaurants.businessId = B.id
        LEFT JOIN (
            SELECT
                businessId,
                SUM(LEAST(CASE WHEN close = 0 THEN 1440 ELSE close END - open / 60.0, 24.0)) AS totalHours
            FROM BusinessHours
            WHERE close > open
            GROUP BY businessId
        ) T ON T.businessId = B.id
        LEFT JOIN (
            SELECT
                businessId,
                CONCAT(breakfastCount, ';;', lunchCount, ';;', dinnerCount, ';;', lateCount) AS openHours
            FROM (
                SELECT
                    businessId,
                    CASE WHEN SUM(breakfast) >= 4 THEN 'B' ELSE '' END AS breakfastCount,
                    CASE WHEN SUM(lunch) >= 4 THEN 'L' ELSE '' END AS lunchCount,
                    CASE WHEN SUM(dinner) >= 4 THEN 'D' ELSE '' END AS dinnerCount,
                    CASE WHEN SUM(late) >= 4 THEN 'La' ELSE '' END AS lateCount
                FROM (
                    SELECT
                            businessId,
                            CASE WHEN open <= 720 AND close > 360 THEN 1 ELSE 0 END AS breakfast,
                            CASE WHEN open <= 900 AND close > 720 THEN 1 ELSE 0 END AS lunch,
                            CASE WHEN open <= 1260 AND close > 1020 THEN 1 ELSE 0 END AS dinner,
                            CASE WHEN open >= 1260 OR open <=120 THEN 1 ELSE 0 END AS late
                    FROM (
                            SELECT
                                businessId,
                                open,
                                CASE WHEN close = 0 THEN 1440 ELSE close END AS close
                            FROM BusinessHours
                            WHERE close >= open
                        ) X
                ) Y
            GROUP BY businessId
            ) Z
        ) OH ON OH.businessId = B.id
        LEFT JOIN BusinessAttributesAggregate A ON A.businessId = B.id
        LEFT JOIN BusinessCategoriesAggregate C ON C.businessId = B.id
        LEFT JOIN ReviewStats R ON R.businessId = B.id
        LEFT JOIN (
            SELECT
                businessId,
                SUM(wordCount) AS numWords,
                AVG(CHAR_LENGTH(word)) AS meanWordLen
            FROM ReviewWords
            GROUP BY businessId
        ) W ON W.businessId = B.id
        LEFT JOIN ReviewSpecialWords RSP ON RSP.businessId = B.id
    -- If you want a just a test set quickly, the uncomment the next line.
    -- LIMIT 20
'''

def getConnectionString():
    import secrets
    return "host='%s' port='%s' dbname='%s' user='%s' password='%s'" % (secrets.DB_HOST, secrets.DB_PORT, secrets.DB_NAME, secrets.DB_USER, secrets.DB_PASS)

def getBusinessesDB():
    # We will only need the imports if you actually hit the db.
    # secrets.py should define DB_HOST, DB_PORT, DB_USER, and DB_PASS
    import secrets
    import psycopg2

    conn = psycopg2.connect(getConnectionString())
    cur = conn.cursor()

    cur.execute(QUERY_BUSINESSES)
    businesses = cur.fetchall()

    cur.close()
    conn.close()

    return businesses

def getBusinesses(businessType):
    if (businessType == DATA_SOURCE_DATABASE):
        return getBusinessesDB()
    elif (businessType == DATA_SOURCE_GROUNDTRUTH_100):
        return loadPickle(GROUND_TRUTH_100_FILE)
    elif (businessType == DATA_SOURCE_GROUNDTRUTH_200):
        return loadPickle(GROUND_TRUTH_200_FILE)
    elif (businessType == DATA_SOURCE_GROUNDTRUTH_ALL):
        return loadPickle(GROUND_TRUTH_ALL_FILE,)
    elif (businessType == DATA_SOURCE_RESTAURANTS):
        return loadPickle(RESTAURANTS_FILE)
    elif (businessType == DATA_SOURCE_HUMAN_EVAL):
        return loadPickle(HUMAN_EVAL_FILE)
    else:
        raise Exception("Unknown business type: %s" % (businessType))

# Just a quick way to get some data to work with without hitting the DB.
def loadPickle(pickleFile):
    return pickle.load(open(pickleFile, 'rb'))

if __name__ == '__main__':
    businesses = getBusinessesDB()
    print(len(businesses))
    for business in businesses[:10]:
        print(business)

    # Be very careful about which one you are using.
    # Look at the query, if your are using the GroundTruth table, then you should be using
    # the test pickle.
    # pickle.dump(businesses, open(RESTAURANTS_FILE, 'wb'))
    # pickle.dump(businesses, open(GROUND_TRUTH_ALL_FILE, 'wb'))
    # pickle.dump(businesses[:100], open(GROUND_TRUTH_100_FILE, 'wb'))
    # pickle.dump(businesses[:200], open(GROUND_TRUTH_200_FILE, 'wb'))
    # pickle.dump(businesses, open(HUMAN_EVAL_FILE, 'wb'))
