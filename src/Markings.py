class Marking(object):
    def __init__(self): self.character = " "

    def get_character(self): return self.character

    def __eq__(self, other):
        return self.character == other.character


class X(Marking):
    def __init__(self): self.character = "X"


class O(Marking):
    def __init__(self): self.character = "O"
