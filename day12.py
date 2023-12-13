import math
from functools import cache


def n_choose_k(n: int, k: int) -> int:
    if k > n:
        return 0
    f = math.factorial
    return f(n) // (f(n - k) * f(k))


def calc_clean_combinations(n: int, defects: tuple[int, ...]) -> int:
    d = len(defects)
    sum_d = sum(defects)
    n = n - sum_d + d
    return n_choose_k(n - d + 1, d)


def is_valid(model: str, defects: tuple[int, ...]) -> bool:
    model_defects = tuple(
        len(s) for s in model.split(".") if s and all(char == "#" for char in s)
    )
    return model_defects == defects


@cache
def solve(model: str, defects: tuple[int, ...]) -> int:
    min_needed = sum(defects) + len(defects) - 1
    if len(model) < min_needed:
        return 0

    known_defects = model.count("#")
    count_defects = sum(defects)
    if count_defects < known_defects:
        return 0

    if model.count("?") == len(model):
        return calc_clean_combinations(len(model), defects)

    if not model:
        if not defects:
            return 1
        else:
            return 0

    if model[0] == ".":
        return solve(model[1:], defects)

    if model[0] == "#":
        if not defects:
            return 0
        defect_len = defects[0]
        if len(model) > defect_len and model[defect_len] == "#":
            return 0
        if model[:defect_len].count("."):
            return 0

        new_model = model[defect_len + 1 :]
        return solve(new_model, defects[1:])

    dot_count = solve(model[1:], defects)
    def_count = solve("#" + model[1:], defects)
    return dot_count + def_count


def main():
    with open("day12_input.txt") as f:
        lines = [line.strip() for line in f.readlines()]

    result = 0
    for line in lines:
        model, defs = line.split()
        defs = [int(d) for d in defs.split(",")]

        model = "?".join([model] * 5)
        defs = defs * 5

        result += solve(model, tuple(defs))

    print(result)


if __name__ == "__main__":
    main()
