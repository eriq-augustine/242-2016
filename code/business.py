class Business:
    def __init__(self, id, features, otherInfo = {}):
        self.id = id
        self.features = features
        self.otherInfo = otherInfo

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __hash__(self):
        return self.id
