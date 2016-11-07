import os
import random

class Metrics:
    
    #Computing the randIndex for a given clustering
    #assignment = dict(businessid) = clusterlabel
    #goldLabel = list of lists of same cluster buisnesses
    #https://en.wikipedia.org/wiki/Rand_index (for more info on rand index)

    def randIndex(self, assign, goldLabel):
        a = 0
        b = 0
        c = 0
        d = 0

        for cluster in goldLabel:
            num_business = len(cluster)
            for i in range(num_business):
                for j in range(i,num_business):
                    if assign[cluster[i]] == assign[cluster[j]]:
                        a += 1
                    else:
                        d += 1

        return (a + 0.0)/(a + d)

    def readBusinessIds(self, filename):
        b_ids = []
        with open(filename, "r") as fp:
            for ids in fp:
                b_ids.append(ids.rstrip("\r\n"))
        return b_ids

    def readGoldLabel(self, directory):
        goldLabel = []
        files = os.listdir(directory)
        for f in files:
            goldLabel.append(self.readBusinessIds(os.path.join(directory, f)))
        
        return goldLabel

if __name__ == "__main__":
    metrics = Metrics()
    assign = {}
    goldLabel = metrics.readGoldLabel("../data/groundtruth")
    clusters = len(goldLabel)
    for c in goldLabel:
        for i in c:
            assign[i] = random.randint(1,clusters)
    print(metrics.randIndex(assign, goldLabel))

