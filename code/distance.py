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
