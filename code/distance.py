import math
import numpy
# A place for distance metric related things.
# Do not feel limited to use only this file, but whoever wants to use distance things
# should just have to import this one file.

def logisticNormalize(val):
    return ((1.0 / (1 + math.exp(-val))) - 0.5) * 2

def logNormalize(val):
    return math.log(max(1, val))

def noNormalize(val):
    return val

'''
The euclidean distance for numeric features.
'''
# Pre: |a| and |b| are collections of numeric values.
def euclidean(a, b, normalization = logisticNormalize):
    assert(len(a) == len(b))

    distance = 0
    for i in range(len(a)):
        distance += math.pow(a[i] - b[i], 2)
    
    result = math.sqrt(distance)
    return normalization(result)

'''
The manhattan distance for numeric features.
'''
# Pre: a and b are two string variables
def manhattan(a, b, normalization = logisticNormalize):
    assert(len(a) == len(b))

    distance = 0
    for i in range(len(a)):
        distance += math.fabs(a[i] - b[i])
    
    return normalization(distance)

def manhattanScalar(a, b, normalization = logisticNormalize):
    return normalization(math.fabs(a - b))

'''
The levenshtein distance for string features.
'''
# Pre: a and b are two string variables
def levenshtein(a, b):

    # Cornner case
    if a == b:
        return 0
    if len(a) == 0 and len(b) == 0:
        return 0
    if len(a) == 0:
        return 1
    if len(b) == 0:
        return 1

    # Create work vectors
    v0 = [None] * (len(b) + 1)
    v1 = [None] * (len(b) + 1)

    # Initialize v0
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(a)):

        # Calculate the distance
        v1[i] = i + 1
        for j in range(len(b)):
            cost = 1
            if a[i] == b[j]:
                cost = 0
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]

    return 1.0 * v1[len(b)] / max(len(a), len(b))

'''
The Needleman Wunsch distance for string features.
Matches are given +1, mismatches are given -1 and indels are given -1
'''
# Pre: a and b are string variales
def needleman_wunsch(a,b):
    #Conner case
    if len(a) == 0 and len(b) == 0:
        return 0

    state = numpy.zeros((len(a) + 1, len(b) + 1))
    # set the initial values for state matrix
    for i in range(1, len(a) + 1):
        state[i][0] = state[i - 1][0] - 1
    for i in range(1, len(b) + 1):
        state[0][i] = state[0][i - 1] - 1

    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            diagonal = state[i - 1][j - 1]
            if a[i - 1] == b[j - 1]:
                diagonal += 1
            else:
                diagonal -= 1
            state[i][j] = max(diagonal, state[i - 1][j] - 1, state[i][j - 1] - 1)

    result = state[len(a)][len(b)]
    maxLen = max(len(a), len(b))
    return 1.0 * (result - maxLen) / (-2 * maxLen)

'''
The Jaccard index (similarity) for set features.
'''
# Pre: a and b are list
def jaccard(a, b):

    #Cornner case
    if len(a) == 0 and len(b) == 0:
        return 0

    a = set(a)
    b = set(b)
    intersection = len(a.intersection(b))
    union = len(a.union(b))
    return 1 - 1.0 * intersection / union

'''
Dice coefficient for set features.
'''
# Pre: a and b are list
def dice(a, b):

    #Conner case
    if len(a) == 0 and len(b) == 0:
        return 0

    a = set(a)
    b = set(b)
    intersection = len(a.intersection(b))
    return 1 - 2.0 * intersection / (len(a) + len(b))

'''
Jacard distance extension
'''
# Pre: a and b are list of boolean 
def jacardExtend(a,b):

    #Cornner case
    if len(a) == 0 and len(b) == 0:
        return 0

    union = max(len(a), len(b))
    minLen = min(len(a), len(b))
    intersection = 0
    for i in range(minLen):
        if a[i] == b[i]:
            intersection += 1
    return 1 - 1.0 * intersection / (union)

'''
Dice distance extension
'''
# Pre: a and b are list of boolean
def diceExtend(a,b):

    #Cornner case
    if len(a) == 0 and len(b) == 0:
        return 0

    minLen = min(len(a), len(b))
    intersection = 0
    for i in range(minLen):
        if a[i] == b[i]:
            intersection += 1
    return 1 - 2.0 * intersection / (len(a) + len(b))

    

