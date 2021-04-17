from NFA import NFA


class Expr:
    state_counter = -1

    def __repr__(self):
        return self.__str__()

    @classmethod
    def get_state(cls):
        cls.state_counter += 1
        return cls.state_counter

    def eval(self):
        return None


def get_state():
    return Expr.get_state()


def get_unique(arg_list):
    return list(set(arg_list))


def paranthesize(*args):
    args = list(map(lambda arg: str(arg), args))
    return "(" + " ".join(args) + ")"


class Union(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return paranthesize(self.left, "UNION", self.right)

    def eval(self):
        eval_left = self.left.eval()
        eval_right = self.right.eval()

        start = get_state()
        end = get_state()

        states = get_unique(
            eval_left.states + eval_right.states + [start] + [end]
        )
        letters = get_unique(eval_right.letters + eval_left.letters + ["$"])
        transition_matrix = get_unique(
            eval_left.transition_matrix
            + eval_right.transition_matrix
            + [(start, "$", eval_left.start_states[0])]
            + [(start, "$", eval_right.start_states[0])]
            + [(eval_left.final_states[0], "$", end)]
            + [(eval_right.final_states[0], "$", end)]
        )
        start_states = [start]
        final_states = [end]

        return NFA(
            states, letters, transition_matrix, start_states, final_states
        )


class Concat(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return paranthesize(self.left, "CONCAT", self.right)

    def eval(self):
        eval_left = self.left.eval()
        eval_right = self.right.eval()

        states = get_unique(eval_left.states + eval_right.states)
        letters = get_unique(eval_left.letters + eval_right.letters)
        transition_matrix = get_unique(
            eval_right.transition_matrix
            + eval_left.transition_matrix
            + [(eval_left.final_states[0], "$", eval_right.start_states[0])]
        )
        start_states = eval_left.start_states
        final_states = eval_right.final_states

        return NFA(
            states, letters, transition_matrix, start_states, final_states
        )


class Kleene(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return paranthesize(self.expr, "KLEENE")

    def eval(self):
        eval_expr = self.expr.eval()

        eval_expr.letters = get_unique(eval_expr.letters + ["$"])
        eval_expr.transition_matrix = get_unique(
            eval_expr.transition_matrix
            + [(eval_expr.final_states[0], "$", eval_expr.start_states[0])]
        )

        return eval_expr


class Grouping(Expr):
    def __init__(self, expr):
        self.expr = expr

    def __str__(self):
        return paranthesize("GROUP", self.expr)

    def eval(self):
        return self.expr.eval()


class Literal(Expr):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def eval(self):
        start = get_state()
        end = get_state()

        states = [start, end]
        letters = [self.value]
        transition_matrix = [(start, self.value, end)]
        start_states = [start]
        final_states = [end]

        return NFA(
            states, letters, transition_matrix, start_states, final_states
        )


if __name__ == "__main__":
    hello = Literal("a")
    hello.eval().pprint()
