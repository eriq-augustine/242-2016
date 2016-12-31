import os
import random

# Compute the randIndex for a given clustering
# https://en.wikipedia.org/wiki/Rand_index (for more info on rand index)\

DATA_DIR = os.path.join('..', 'data')
GROUNDTRUTH_DIR = os.path.join(DATA_DIR, 'groundtruth')
HUMANTRUTH_DIR = os.path.join(DATA_DIR, 'humanEval')

HUMAN_PAIRS_FILE = os.path.join(HUMANTRUTH_DIR, 'pairs.txt')

RESTAURANT_FILES = ['burgerking.id', 'chipotle.id', 'dairyqueen.id', 'dominospizza.id', 'dunkindonut.id', 'jackinthebox.id', 'kfc.id', 'mcdonalds.id', 'pandaexpress.id', 'papajohnspizza.id', 'pizzahut.id', 'starbucks.id', 'subway.id', 'subway.id', 'wendys.id']
FINEDINING_FILE = 'finedining.id'

# Flatten x into a single list.
def flatten(x):
    return [item for sublist in x for item in sublist]

# |clusters| is raw output from clustering.
# |truthPairs| is {smallerId: {largerId: similar?}},
# where the end value is true if the businesses are similar, false otherwise.
# The ids in |truthPairs| are yelp ids.
def randIndex(clusters, businesses, truthPairs = None, truthIds = None):
    # Instead of using the undescriptive variable names from Rand Index's forumula,
    # we have translated them to accuracy counterparts where
    # the first set, X, is the truth values, and the second set, Y, is the clustering.
    # a = True Positive
    # b = True Negative
    # c = False Negative
    # d = False Positive
    # We don't actually need c/d, since they are only used when added to (a + b).
    # The entire sum comes out to be nC2 where n is the number of elements (businesses).
    # However, since we are not doing the complete set we just use the number of pairs in |truthPairs|.
    tp = 0
    tn = 0
    totalPairs = 0

    if (truthPairs == None):
        truthPairs, truthIds = getGoldTruthPairs()
    elif (truthIds is None):
        raise 'Need truthIds'
    else:
        truthIds = set(truthIds)

    # Convert the clusters to a structure optimized for searching.
    # However we will not hold negative pairings, those can be inferred by their absence.
    clusters = convertIds(clusters, businesses)
    clusterPairs = buildPairs(clusters, truthIds)
    clusterIds = set(flatten(clusters))

    for id1 in truthPairs:
        if (id1 not in clusterIds):
            continue

        for id2 in truthPairs[id1]:
            if (id2 not in clusterIds):
                continue

            if (truthPairs[id1][id2] and (id1, id2) in clusterPairs):
                tp += 1
            elif ((not truthPairs[id1][id2]) and (id1, id2) not in clusterPairs):
                tn += 1

            totalPairs += 1

    return float(tp + tn) / totalPairs

# Swap from business indexes to business ids.
def convertIds(clusters, businesses):
    return [[businesses[index].otherInfo['yelpId'] for index in cluster] for cluster in clusters]

# Returns {(smallerId, largerId): True}
# We don't hold negative pairs.
# Only include values that are in |truthIds|.
def buildPairs(clusters, truthIds):
    pairs = {}

    for cluster in clusters:
        for id1 in cluster:
            if (id1 not in truthIds):
                continue

            for id2 in cluster:
                if (id2 not in truthIds or id1 >= id2):
                    continue

                pairs[(id1, id2)] = True
    
    return pairs

def getGoldTruthPairs():
    truthIds = []
    pairs = {}

    fineDiningIds = None
    with open(os.path.join(GROUNDTRUTH_DIR, FINEDINING_FILE)) as inFile:
        fineDiningIds = inFile.read().splitlines()
        truthIds.extend(fineDiningIds)

    for retaurantFilename in RESTAURANT_FILES:
        ids = None
        with open(os.path.join(GROUNDTRUTH_DIR, retaurantFilename)) as inFile:
            ids = inFile.read().splitlines()
            truthIds.extend(ids)

        # Add positive pairs
        for id1 in ids:
            for id2 in ids:
                if (id1 >= id2):
                    continue

                if (id1 not in pairs):
                    pairs[id1] = {}

                pairs[id1][id2] = True

        # Add negative pairs
        for fineDiningId in fineDiningIds:
            for id in ids:
                minId = min(fineDiningId, id)
                maxId = max(fineDiningId, id)

                if (minId not in pairs):
                    pairs[minId] = {}

                pairs[minId][maxId] = False

    return pairs, set(truthIds)

def getHumanTruthPairs():
    truthIds = []
    pairs = {}

    with open(HUMAN_PAIRS_FILE) as inFile:
        inPairs = inFile.read().splitlines()
        for inPair in inPairs:
            parts = inPair.split(',')
            minId = min(parts[0], parts[1])
            maxId = max(parts[0], parts[1])

            # Truth values come in the range of [1, 5].
            # Leave out 3, <3 = false, >3 = true.
            similarityValue = int(parts[2])
            similar = None

            if (similarityValue < 3):
                similar = False
            elif (similarityValue > 3):
                similar = True
            else:
                continue

            truthIds.append(minId)
            truthIds.append(maxId)

            if (minId not in pairs):
                pairs[minId] = {}

            pairs[minId][maxId] = similar

    return pairs, set(truthIds)

# Past here is our old rand index code.
# It has a bug, but is currently left in for analysis and consistency.

# assignment = dict(businessid) = clusterlabel
# goldLabel = list of lists of same cluster buisnesses

def getRestaurantFiles():
    return ['burgerking.id', 'chipotle.id', 'dairyqueen.id', 'dominospizza.id', 'dunkindonut.id', 'jackinthebox.id', 'kfc.id', 'mcdonalds.id', 'pandaexpress.id', 'papajohnspizza.id', 'pizzahut.id', 'starbucks.id', 'subway.id', 'subway.id', 'wendys.id', 'finedining.id']

def oldRandIndex(assign, goldLabel):
    a = 0.0
    b = 0
    c = 0
    d = 0

    for cluster in goldLabel:
        if cluster == 'finedining.id':
            continue
        num_business = len(goldLabel[cluster])
        for i in range(num_business):
            # BUG(varun): This is a bug.
            # It should be range(i + 1, num_businesses).
            # a gets artifically inflated by the number of non-finedining businesses.
            # This can be computed out of all the current results.
            for j in range(i,num_business):
                try:
                    if assign[goldLabel[cluster][i]] == assign[goldLabel[cluster][j]]:
                        a += 1
                    else:
                        d += 1
                except KeyError:
                   #print("One of both keys not found in clusters:" + str( goldLabel[cluster][i]) + "," + str(goldLabel[cluster][j]))
                   pass

    for finedining in goldLabel['finedining.id']:
        for cluster in goldLabel:
            if cluster == 'finedining.id':
                continue
            for j in goldLabel[cluster]:
                try:
                    if assign[finedining] == assign[j]:
                        c += 1
                    else:
                        b += 1
                except KeyError:
                    #print("One of both keys not found in clusters:" + str( goldLabel[cluster][i]) + "," + str(goldLabel[cluster][j]))
                    pass
    randIndex = -1
    if a+b+c+d != 0:
        randIndex = (a + b )/(a + b + c + d)

    return randIndex

def readBusinessIds(filename):
    b_ids = []
    with open(filename, "r") as fp:
        for ids in fp:
            b_ids.append(ids.rstrip("\r\n"))
    return b_ids

def readGoldLabel(directory):
    goldLabel = {}
    restaurant_files = getRestaurantFiles()

    for f in restaurant_files:
        goldLabel[f] = readBusinessIds(os.path.join(directory, f))
    return goldLabel

def getClusterBusinessID(businesses, clusters):
    b_cluster = {}
    for i in range(len(clusters)):
        for index in clusters[i]:
            b_cluster[businesses[index].otherInfo['yelpId']] = i
    return b_cluster

if __name__ == "__main__":
    assign = {}
    goldLabel = readGoldLabel("../data/groundtruth")

    clusters = len(goldLabel)
    for c in goldLabel:
        for i in c:
            assign[i] = random.randint(1,clusters)

    print(oldRandIndex(assign, goldLabel))
