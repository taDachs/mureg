#!/usr/bin/env python3

from mureg.regex_to_sm import concat_sm, build_literal_sm, choose_sm, kleene_star, kleene_plus
from mureg.transforms import reduce_epsilon, reduce_powerset
from mureg.puml import write_puml

test_regex = "aaaba"
test_string_true = "aaaba"
test_string_false = "aaaab"

sm1 = build_literal_sm("a")
sm2 = build_literal_sm("b")

a_star = kleene_plus(sm1)
# sm = a_star
c_sm = choose_sm(sm1, sm2)
sm = concat_sm(a_star, c_sm)
sm = concat_sm(sm, a_star)
# print(sm)
sm = reduce_epsilon(sm)
sm = reduce_powerset(sm)
# print(sm)
# print(sm("aaaaaaaabbbbaaaaaaaaa"))
# print(sm("abaaa"))
# print(sm(""))

with open("./test.puml", "w+") as f:
    write_puml(f, sm)


