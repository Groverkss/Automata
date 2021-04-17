from collections import deque
import itertools

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

    def convert_to_dfa(self):
        left_states = deque()

        start_state = [0] * len(self.states)
        start_state[self.start_states[0]] = 1
        for val in self._get_epsilon_vals(self.start_states[0]):
            start_state[val] = 1
        start_state = tuple(start_state)

        left_states.append(start_state)

        new_transition_matrix = []
        states = {}
        final_states = []

        states[start_state] = 0

        while len(left_states) > 0:
            curr_state = left_states.popleft()

            for final_state in self.final_states:
                if curr_state[final_state]:
                    final_states.append(states[curr_state])
                    break

            if curr_state not in states:
                states[curr_state] = len(states)

            req_states = [
                index for index, value in enumerate(curr_state) if value == 1
            ]

            transitions = list(
                filter(
                    lambda state: state[0] in req_states, self.transition_matrix
                )
            )

            # Group transitions by alphabet
            for groups in itertools.groupby(transitions, lambda x: x[1]):
                alpha, actions = groups
                if alpha == "$":
                    continue

                new_transition = [0] * len(self.states)

                for start, _, end in actions:
                    new_transition[end] = 1
                    for vals in self._get_epsilon_vals(end):
                        new_transition[vals] = 1

                new_transition = tuple(new_transition)
                if new_transition not in states:
                    left_states.append(new_transition)
                    states[new_transition] = len(states)

                new_transition_matrix.append(
                    (states[curr_state], alpha, states[new_transition])
                )

        if "$" in self.letters:
            self.letters.remove("$")

        self.states = list(states.values())
        self.transition_matrix = new_transition_matrix
        self.start_states = [0]
        self.final_states = final_states

    def _get_epsilon_vals(self, state, first=True):
        if first:
            self._epsilon_done = set()
        self._epsilon_done.add(state)

        transitions = [
            self._get_epsilon_vals(end, False)
            for start, alpha, end in self.transition_matrix
            if alpha == "$" and start == state and end not in self._epsilon_done
        ]
        transitions.append([state])

        flat_list = [item for sublist in transitions for item in sublist]
        flat_list = list(set(flat_list))

        return flat_list
