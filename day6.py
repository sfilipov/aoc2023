import math


def wins_for_race(time: int, distance: int) -> int:
    b = -time
    c = distance
    x1 = (-b - math.sqrt(b ** 2 - 4 * c)) / 2
    x2 = (-b + math.sqrt(b ** 2 - 4 * c)) / 2
    start = x1 + 1 if x1.is_integer() else math.ceil(x1)
    end = x2 - 1 if x2.is_integer() else math.floor(x2)
    return int(end - start + 1)


def main():
    with open('day6_input.txt') as f:
        times = [int(n) for n in f.readline().split()[1:]]
        distances = [int(n) for n in f.readline().split()[1:]]

    result_part1 = 1
    for time, distance in zip(times, distances):
        result_part1 *= wins_for_race(time, distance)
    print(result_part1)

    time = int(''.join(str(t) for t in times))
    distance = int(''.join(str(d) for d in distances))
    print(wins_for_race(time, distance))


if __name__ == '__main__':
    main()
