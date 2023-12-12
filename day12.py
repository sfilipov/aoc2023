"""
- use dots to split into subproblems
    - recursively check possible counts on subproblems
- when left only with ?s - use combinatorics directly to calculate
- when left with mix of ?s and #? - brute force
    - figure out number of .s and #s based on defects. Assign smaller number
"""

import math
from itertools import combinations


def n_choose_k(n: int, k: int) -> int:
    if k > n:
        return 0
    f = math.factorial
    return f(n) // (f(n - k) * f(k))


def calc_clean_combinations(n: int, defects: list[int]) -> int:
    d = len(defects)
    sum_d = sum(defects)
    n = n - sum_d + d
    return n_choose_k(n - d + 1, d)


def is_valid(model: str, defects: list[int]) -> bool:
    defects_array = [
        len(s) for s in model.split(".") if s and all(char == "#" for char in s)
    ]
    return tuple(defects_array) == tuple(defects)


# TODO inference is wrong on invalid inputs (i.e. speculative solves on dot split)
# def infer(model: str, defects: list[int]) -> tuple[str, list[int]]:
#     known_defect_index = model.find("#")
#     if known_defect_index == -1:
#         return (model, defects)
#     if not defects:
#         return (model, defects)
#     defect_len = defects[0]
#     if known_defect_index == 0:
#         return infer(model[defect_len + 1 :], defects[1:])
#     if known_defect_index == defect_len:
#         return infer(model[1:], defects)
#     if known_defect_index < defect_len:
#         next_var = model.find("?", known_defect_index)
#         known_defect_range = next_var - known_defect_index
#         if known_defect_range == defect_len:
#             return infer(model[next_var + 1 :], defects[1:])
#         unknown = defect_len - known_defect_range
#         keep_start = known_defect_index - unknown
#         if keep_start > 0:
#             return infer(model[keep_start:], defects)

#     return (model, defects)


def solve(model: str, defects: list[int]) -> int:
    min_needed = sum(defects) + len(defects) - 1
    if len(model) < min_needed:
        return 0

    known_defects = sum(1 for char in model if char == "#")
    count_defects = sum(defects)
    if count_defects < known_defects:
        return 0

    dot_indexes = [i for i, char in enumerate(model) if char == "."]
    if dot_indexes:
        pivot_index = dot_indexes[len(dot_indexes) // 2]
        return solve_dot_split(model, defects, pivot_index)

    # model, defects = infer(model, defects)

    if all(char == "?" for char in model):
        return calc_clean_combinations(len(model), defects)

    var_indexes = [i for i, char in enumerate(model) if char == "?"]
    if var_indexes:
        pivot_index = var_indexes[len(var_indexes) // 2]
        dot_count = solve_dot_split(model, defects, pivot_index)
        def_model = "".join([model[:pivot_index], "#", model[pivot_index + 1 :]])
        def_count = solve(def_model, defects)
        return dot_count + def_count

    return 1
    # return solve_brute(model, defects)


def solve_dot_split(model: str, defects: list[int], dot_index: int) -> int:
    model_a, model_b = model[:dot_index], model[dot_index + 1 :]
    result = 0
    for i in range(len(defects) + 1):
        defects_a, defects_b = defects[:i], defects[i:]
        result += solve(model_a, defects_a) * solve(model_b, defects_b)
    return result


# def solve_brute(model: str, defects: list[int]) -> int:
#     var_indexes = [i for i, char in enumerate(model) if char == "?"]
#     total_defects = sum(defects)
#     known_defects = len(model) - len(var_indexes)
#     to_assign = total_defects - known_defects
#     if to_assign < 0:
#         return 0
#     count = 0
#     for assigned_defects in combinations(var_indexes, to_assign):
#         assigned_defects = set(assigned_defects)
#         model_array: list[str] = []
#         for i, char in enumerate(model):
#             if char == "#":
#                 c = "#"
#             else:
#                 c = "#" if i in assigned_defects else "."
#             model_array.append(c)
#         test_model = "".join(model_array)
#         if is_valid(test_model, defects):
#             count += 1

#     return count


def main():
    with open("day12_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    result = 0
    for line in lines:
        model, defs = line.split()
        defs = [int(d) for d in defs.split(",")]

        model = "?".join([model] * 5)
        defs = defs * 5

        result += solve(model, defs)

    print(result)


if __name__ == "__main__":
    main()
