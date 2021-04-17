from pprint import pprint


class NFA:
    def __init__(
        self, states, letters, transition_matrix, start_states, final_states
    ):
        self.letters = letters
        self.states = states
        self.transition_matrix = transition_matrix
        self.start_states = start_states
        self.final_states = final_states

    def pprint(self):
        """Pretty print NFA"""

        print("States: ", end="")
        pprint(self.states)
        print("Letters: ", end="")
        pprint(self.letters)
        print("Transition Matrix: ", end="")
        pprint(self.transition_matrix)
        print("Start States: ", end="")
        pprint(self.start_states)
        print("Final States: ", end="")
        pprint(self.final_states)
