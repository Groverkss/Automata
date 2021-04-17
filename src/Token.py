class Token:
    """Class representing a single token"""

    def __init__(self, token_type, pos, value=None):
        self.token_type = token_type
        self.value = value
        self.pos = pos

    def __str__(self):
        if self.value:
            return str(self.token_type) + ": " + self.value
        else:
            return str(self.token_type)

    def __repr__(self):
        return self.__str__()
