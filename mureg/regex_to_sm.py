from mureg.sm import StateMachine, EPS
from mureg.transforms import prepend_states


def concat_sm(sm1, sm2):
    # rename to avoid naming conflicts
    sm1 = prepend_states(sm1, "sm_1_")
    sm2 = prepend_states(sm2, "sm_2_")

    transitions = sm1.transitions + sm2.transitions

    # new epsilon transitions for connecting state machines
    new_connecting_transitions = [(s, EPS, sm2.start_state) for s in sm1.accepting_states]
    transitions += new_connecting_transitions

    # new start state
    new_start = "new_start"
    transitions.append((new_start, EPS, sm1.start_state))

    # new end state
    new_end = "new_end"
    new_accepting_transitions = [(s, EPS, new_end) for s in sm2.accepting_states]

    transitions += new_accepting_transitions

    states = list(set([s for (s, _, _) in transitions] + [s for (_, _, s) in transitions]))

    return StateMachine(states, new_start, [new_end], transitions)


def choose_sm(sm1, sm2):
    # rename to avoid naming conflicts
    sm1 = prepend_states(sm1, "sm_1_")
    sm2 = prepend_states(sm2, "sm_2_")

    transitions = sm1.transitions + sm2.transitions

    new_start = "new_start"
    transitions.append((new_start, EPS, sm1.start_state))
    transitions.append((new_start, EPS, sm2.start_state))

    new_end = "new_end"
    new_accepting_transitions = [(s, EPS, new_end) for s in sm1.accepting_states] + [
        (s, EPS, new_end) for s in sm2.accepting_states
    ]

    transitions += new_accepting_transitions

    states = list(set([s for (s, _, _) in transitions] + [s for (_, _, s) in transitions]))

    return StateMachine(states, new_start, [new_end], transitions)


def build_literal_sm(c):
    states = ["q1", "q2"]
    start_state = "q1"
    accepting_states = ["q2"]

    transitions = [("q1", c, "q2")]

    return StateMachine(states, start_state, accepting_states, transitions)


def build_empty_sm():
    states = ["q1", "q2"]
    start_state = "q1"
    accepting_states = ["q2"]

    transitions = [("q1", EPS, "q2")]

    return StateMachine(states, start_state, accepting_states, transitions)


def kleene_star(sm):
    sm = prepend_states(sm, "kleene_")
    transitions = sm.transitions
    new_start = "new_start"
    new_end = "new_end"

    transitions.append((new_start, EPS, sm.start_state))
    for s in sm.accepting_states:
        transitions.append((s, EPS, sm.start_state))
        transitions.append((s, EPS, new_end))
    transitions.append((new_start, EPS, new_end))

    states = list(set([s for (s, _, _) in transitions] + [s for (_, _, s) in transitions]))

    return StateMachine(states, new_start, [new_end], transitions)


def kleene_plus(sm):
    sm = prepend_states(sm, "kleene_")
    transitions = sm.transitions
    new_start = "new_start"
    new_end = "new_end"

    transitions.append((new_start, EPS, sm.start_state))
    for s in sm.accepting_states:
        transitions.append((s, EPS, sm.start_state))
        transitions.append((s, EPS, new_end))

    states = list(set([s for (s, _, _) in transitions] + [s for (_, _, s) in transitions]))

    return StateMachine(states, new_start, [new_end], transitions)



