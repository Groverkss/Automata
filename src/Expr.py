class Expr:
    def __repr__(self):
        return self.__str__()


def paranthesize(*args):
    args = list(map(lambda arg: str(arg), args))
    return "(" + " ".join(args) + ")"


class Union(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return paranthesize(self.left, "UNION", self.right)


class Concat(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return paranthesize(self.left, "CONCAT", self.right)


class Kleene(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return paranthesize(self.expr, "KLEENE")


class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return paranthesize("GROUP", self.expr)


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value
