import math

# A place for distance metric related things.
# Do not feel limited to use only this file, but whoever wants to use distance things
# should just have to import this one file.

# TODO(xiao): Research and implement other distance metrics.

# Pre: |a| and |b| are collections of numeric values.
def euclidean(a, b):
    assert(len(a) == len(b))

    distance = 0
    for i in range(len(a)):
        distance += math.pow(a[i] - b[i], 2)

    return math.sqrt(distance)

# Pre: a and b are two string variables
def levenshtein(a, b):

    # Cornner case
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    
    # Create work vectors
    v0 = [None] * (len(t) + 1)
    v1 = [None] * (len(t) + 1)

    # Initialize v0
    for i in range(len(v0)):
        v0[i] = i
    for i in range(len(s)):

        # Calculate the distance
        v1[i] = i + 1
        for j in range(len(t)):
            cost = 1
            if s[i] == t[j]:
                cost = 0
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
        for j in range(len(v0)):
            v0[j] = v1[j]
    return v1[len(t)]
