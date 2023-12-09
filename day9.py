def next_for_seq(seq: list[int]) -> tuple[int, int]:
    stack: list[list[int]] = []
    while not all(num == 0 for num in seq):
        sub_seq = [b - a for a, b in zip(seq[:-1], seq[1:])]
        stack.append(seq)
        seq = sub_seq

    while stack:
        next_seq = stack.pop()
        next_seq.append(next_seq[-1] + seq[-1])
        next_seq.insert(0, next_seq[0] - seq[0])
        seq = next_seq

    return (seq[0], seq[-1])


def main():
    with open("day9_input.txt") as f:
        seqs = [[int(num) for num in seq.strip().split()] for seq in f.readlines()]

    result_part1 = 0
    result_part2 = 0
    for seq in seqs:
        first, last = next_for_seq(seq)
        result_part1 += last
        result_part2 += first
    print(result_part1, result_part2)


if __name__ == "__main__":
    main()
