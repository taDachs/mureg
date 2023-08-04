EPS = -1
WILD = -2


class StateMachine:
    def __init__(self, states, start_state, accepting_states, transitions):
        self.states = states
        self.start_state = start_state
        self.accepting_states = accepting_states
        self.transitions = transitions

        self.current_state = self.start_state

    def __call__(self, w):
        return self.read_word(w)

    def read_word(self, w):
        current_state = self.start_state
        for c in w:
            valid_transitions = self.get_transitions(q=current_state, c=c)
            if len(valid_transitions) > 1:
                raise Exception(f"Nondeterministic transition: {valid_transitions}")
            elif len(valid_transitions) == 1:
                current_state = valid_transitions[0][2]
            else:
                return False
        return current_state in self.accepting_states

    def get_transitions(self, q=None, c=None, q_dot=None):
        trans = self.transitions
        if q is not None:
            trans = [t for t in trans if t[0] == q]

        if c is not None:
            trans = [t for t in trans if t[1] == c]

        if q_dot is not None:
            trans = [t for t in trans if t[2] == q_dot]

        return trans

    def __str__(self):
        return f"""
States: {self.states}
Start State: {self.start_state}
Accepting States: {self.accepting_states}
Transitions: {self.transitions}
        """
