import data
from sklearn.feature_extraction import DictVectorizer
import numpy as np
import sys

# This is mainly for deciding if we are getting real or fake data.
DEBUG = True

# TODO(dhawal): Do some feature engineering.
# As of now, we are only returning numeric features.
def getFeatures():
    features = []
    businesses = data.getBusinesses(DEBUG)

    # one-hot encoding of active, city, and state variables + numeric features
    vec = DictVectorizer()
    cityStateMatrix = vec.fit_transform([{"active": b[1], "city":b[2], "state":b[3]} for b in businesses]).toarray()
    businesses = np.array([business[4:] for business in businesses])
    features = np.hstack((cityStateMatrix, businesses)).tolist()
    return features

if __name__ == '__main__':
    print(getFeatures())
