import data

# This is mainly for deciding if we are getting real or fake data.
DEBUG = True

# TODO(dhawal): Do some feature engineering.
def getFeatures():
    businesses = data.getBusinesses(DEBUG)

    # For now, just pick out the numeric features.
    return [business[3:] for business in businesses]

if __name__ == '__main__':
    getFeatures()
