from mureg.sm import StateMachine, EPS


def write_puml(fp, sm):
    fp.write("@startuml\n")
    fp.write("scale 600 width\n")

    fp.write(f"[*] -> {sm.start_state}\n")

    for (q, c, q_dot) in sm.transitions:
        fp.write(f"{q} --> {q_dot} : {'eps' if c == EPS else c}\n")

    for q in sm.accepting_states:
        fp.write(f"{q} --> [*]\n")

    fp.write("@enduml")


