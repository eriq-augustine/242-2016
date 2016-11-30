import pickle

# If you use the db, then you will need a file (secrets.py) that defines: DB_HOST, DB_PORT, DB_USER, and DB_PASS

FAKE_BUSINESSES_FILE = 'fakeBusinesses.pickle'
REAL_BUSINESSES_FILE = 'fullBusinesses.pickle'
TEST_BUSINESSES_FILE = 'testBusinesses.pickle'

DATA_TYPE_DATABASE = 'database'
DATA_TYPE_FAKE = 'fake'
DATA_TYPE_FULL = 'full'
DATA_TYPE_TEST = 'test'

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
        COALESCE(RSP.keyWords, '') AS keyWords
    FROM
        Businesses B
        -- To limit businesses to only the test set, uncomment this.
        -- JOIN GroundTruth GT ON GT.businessId = B.id
        JOIN (
            SELECT DISTINCT businessId
            FROM BusinessCategories BC
            WHERE name IN (
                'Restaurants', 'Food', 'Fast Food', 'Pizza', 'Mexican',
                'Sandwiches', 'American (Traditional)', 'Burgers', 'Italian',
                'Chinese', 'American (New)', 'Breakfast & Brunch', 'Cafes'
            )
        ) Restaurants ON Restaurants.businessId = B.id
        LEFT JOIN BusinessAttributesAggregate A ON A.businessId = B.id
        LEFT JOIN BusinessCategoriesAggregate C on C.businessId = B.id
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
    if (businessType == DATA_TYPE_DATABASE):
        return getBusinessesDB()
    elif (businessType == DATA_TYPE_FAKE):
        return getFakeBusinesses()
    elif (businessType == DATA_TYPE_FULL):
        return getFullBusinesses()
    elif (businessType == DATA_TYPE_TEST):
        return getTestBusinesses()
    else:
        raise Exception("Unknown business type: %s" % (businessType))

# Just a quick way to get some data to work with without hitting the DB.
def getFakeBusinesses():
    return pickle.load(open(FAKE_BUSINESSES_FILE, 'rb'))

# Get the  businesses in our golden set from the pickle.
def getTestBusinesses():
    return pickle.load(open(TEST_BUSINESSES_FILE, 'rb'))

# Get the real businesses from the pickle.
def getFullBusinesses():
    return pickle.load(open(REAL_BUSINESSES_FILE, 'rb'))

if __name__ == '__main__':
    businesses = getBusinessesDB()
    print(len(businesses))
    for business in businesses[:10]:
        print(business)
    # pickle.dump(businesses[:100], open(FAKE_BUSINESSES_FILE, 'wb'))

    # Be very careful about which one you are using.
    # Look at the query, if your are using the GroundTruth table, then you should be using
    # the test pickle.
    # pickle.dump(businesses, open(REAL_BUSINESSES_FILE, 'wb'))
    # pickle.dump(businesses, open(TEST_BUSINESSES_FILE, 'wb'))
