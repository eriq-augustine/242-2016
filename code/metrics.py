import os
import random

#Computing the randIndex for a given clustering
#assignment = dict(businessid) = clusterlabel
#goldLabel = list of lists of same cluster buisnesses
#https://en.wikipedia.org/wiki/Rand_index (for more info on rand index)

def getRestaurantFiles():
    restaurant_files = ['burgerking.id', 'chipotle.id', 'dairyqueen.id', 'dominospizza.id', 'dunkindonut.id', 'jackinthebox.id', 'kfc.id', 'mcdonalds.id', 'pandaexpress.id', 'papajohnspizza.id', 'pizzahut.id', 'starbucks.id', 'subway.id', 'subway.id', 'wendys.id', 'finedining.id']
    return restaurant_files

def randIndex(assign, goldLabel):
    a = 0.0
    b = 0
    c = 0
    d = 0

    for cluster in goldLabel:
        if cluster == 'finedining.id':
            continue
        num_business = len(goldLabel[cluster])
        for i in range(num_business):
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
    print(randIndex(assign, goldLabel))
