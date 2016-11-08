import pickle

# If you use the db, then you will need a file (secrets.py) that defines: DB_HOST, DB_PORT, DB_USER, and DB_PASS

FAKE_BUSINESSES_FILE = 'fakeBusinesses.pickle'

QUERY_BUSINESSES = '''
    SELECT
        B.id,
        B.yelpId,
        B.active,
        B.city,
        B.state,
        B.stars,
        B.reviewCount AS totalReviewCount,
        COALESCE(R.availableReviewCount, 0) AS availableReviewCount,
        COALESCE(R.meanReviewLen, 0) AS meanReviewLen,
        COALESCE(W.meanWordLen, 0) AS meanWordLen,
        COALESCE(W.numWords, 0) AS numWords,
        COALESCE(W.numWords / R.availableReviewCount, 0) AS meanWordCount
    FROM
        Businesses B
        LEFT JOIN (
            SELECT
                businessId,
                AVG(CHAR_LENGTH(REGEXP_REPLACE(text, E'\\s+', '', 'g'))) as meanReviewLen,
                COUNT(*) AS availableReviewCount
            FROM Reviews
            GROUP BY businessId
        ) R ON R.businessId = B.id
        LEFT JOIN (
            SELECT
                businessId,
                COUNT(*) AS numWords,
                AVG(wordLen) AS meanWordLen
            FROM (
                SELECT
                    businessId,
                    CHAR_LENGTH(REGEXP_SPLIT_TO_TABLE(text, E'\\s+')) AS wordLen
                FROM Reviews
                -- If you want a just a test set quickly, the uncomment the next line.
                -- WHERE businessId <= 20
            ) X
            GROUP BY businessId
        ) W ON W.businessId = B.id
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

def getBusinesses(fake = False):
    if (fake):
        return getFakeBusinesses()
    return getBusinessesDB()

# Just a quick way to get some data to work with without hitting the DB.
def getFakeBusinesses():
    return pickle.load(open(FAKE_BUSINESSES_FILE, 'rb'))

if __name__ == '__main__':
    businesses = getBusinesses()
    print(len(businesses))
    for business in businesses[:10]:
        print(business)
    # pickle.dump(businesses[:50], open(FAKE_BUSINESSES_FILE, 'wb'))
