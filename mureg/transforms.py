from mureg.sm import EPS, StateMachine


def reduce_epsilon(sm, rename=True):
    def compute_eps_closure(s, visited=None):
        if visited is None:
            visited = []

        visited.append(s)

        trans = sm.get_transitions(q=s, c=EPS)
        states = [q for (_, _, q) in trans]
        states = list(set(states))
        closure = [s]
        for q in states:
            if q in visited:
                continue
            closure += compute_eps_closure(q, visited)

        return list(set(closure))

    # compute epsilon closures
    eps_closures = []
    for s in sm.states:
        eps_closures.append(compute_eps_closure(s))

    # compute final states
    final_states = []
    for closure in eps_closures:
        if any([s in sm.accepting_states for s in closure]):
            final_states.append(closure)

    # compute new transitions
    new_transitions = []
    for closure_1 in eps_closures:
        for closure_2 in eps_closures:
            for q_1 in closure_1:
                for q_2 in closure_2:
                    transitions = sm.get_transitions(q=q_1, q_dot=q_2)
                    for _, c, _ in transitions:
                        if c is EPS:
                            continue
                        new_transitions.append((closure_1, c, closure_2))

    # convert state names
    new_transitions = [("_".join(q1), c, "_".join(q2)) for (q1, c, q2) in new_transitions]
    final_states = ["_".join(s) for s in final_states]
    new_states = list(
        set([s for (s, _, _) in new_transitions] + [s for (_, _, s) in new_transitions])
    )

    new_start_state = "_".join(compute_eps_closure(sm.start_state))

    epsilon_free_sm = StateMachine(new_states, new_start_state, final_states, new_transitions)
    return reduce_unreachable_states(epsilon_free_sm, rename=rename)
    # return epsilon_free_sm


def reduce_unreachable_states(sm, rename=True):
    reachable_transitions = []

    open = []
    closed = set()

    open.append(sm.start_state)

    while len(open) != 0:
        s = open.pop(0)
        closed.add(s)
        transitions = sm.get_transitions(q=s)
        for t in transitions:
            reachable_transitions.append(t)
            s_dot = t[2]
            if s_dot in closed:
                continue
            open.append(s_dot)

    reachable_states = list(closed)
    reachable_transitions = list(set(reachable_transitions))
    start_state = sm.start_state

    reachable_final_states = [s for s in sm.accepting_states if s in reachable_states]

    if rename:
        mapping = {s: f"q_{i}" for i, s in enumerate(reachable_states)}
        reachable_states = list(mapping.values())
        reachable_transitions = {
            (mapping[q], c, mapping[q_dot]) for (q, c, q_dot) in reachable_transitions
        }
        reachable_final_states = [mapping[s] for s in reachable_final_states]
        start_state = mapping[start_state]

    return StateMachine(
        reachable_states, start_state, reachable_final_states, reachable_transitions
    )


def reduce_powerset(sm):
    alphabet = {c for (_, c, _) in sm.transitions}
    S = set()
    T = set()
    new_states = {(sm.start_state,)}
    new_transitions = set()

    while (len(S) != len(new_states)) or (len(T) != len(new_transitions)):
        # TODO: this is incredibly stupid but I am just to tired right now
        S = new_states
        T = new_transitions
        new_states = set()
        new_transitions = set()

        for s_dot in S:
            new_states.add(s_dot)
            for x in alphabet:
                u_dot = set()
                for s in s_dot:
                    transitions = sm.get_transitions(q=s, c=x)
                    u_dot |= {q for (_, _, q) in transitions}
                if len(u_dot) == 0:
                    continue
                u_dot = tuple(u_dot)
                new_states.add(u_dot)
                new_transitions.add((s_dot, x, u_dot))

    new_accepting_states = ["_".join(s) for s in S if any([q in sm.accepting_states for q in s])]
    S = ["_".join(s) for s in S]
    T = [("_".join(q), c, "_".join(q_dot)) for (q, c, q_dot) in T]

    deterministic_sm = StateMachine(
        S,
        sm.start_state,
        new_accepting_states,
        T,
    )

    return reduce_unreachable_states(deterministic_sm)


def prepend_states(sm, s):
    states = [s + str(q) for q in sm.states]
    start_state = s + str(sm.start_state)
    final_states = [s + str(q) for q in sm.accepting_states]
    transitions = [(s + str(t[0]), t[1], s + str(t[2])) for t in sm.transitions]

    return StateMachine(states, start_state, final_states, transitions)

