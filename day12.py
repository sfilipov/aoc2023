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
        model_a, model_b = model[:pivot_index], model[pivot_index + 1 :]
        result = 0
        for i in range(len(defects) + 1):
            defects_a, defects_b = defects[:i], defects[i:]
            result += solve(model_a, defects_a) * solve(model_b, defects_b)
        return result

    if all(char == "?" for char in model):
        return calc_clean_combinations(len(model), defects)

    var_indexes = [i for i, char in enumerate(model) if char == "?"]
    total_defects = sum(defects)
    known_defects = len(model) - len(var_indexes)
    to_assign = total_defects - known_defects
    count = 0
    for assigned_defects in combinations(var_indexes, to_assign):
        assigned_defects = set(assigned_defects)
        model_array: list[str] = []
        for i, char in enumerate(model):
            if char == "#":
                c = "#"
            else:
                c = "#" if i in assigned_defects else "."
            model_array.append(c)
        test_model = "".join(model_array)
        if is_valid(test_model, defects):
            count += 1

    return count


def main():
    with open("day12_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    result = 0
    for line in lines:
        model, defs = line.split()
        defs = [int(d) for d in defs.split(",")]
        result += solve(model, defs)

    print(result)


if __name__ == "__main__":
    main()
