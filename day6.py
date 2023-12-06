import math

def main():
    with open('day6_input.txt') as f:
        times = [int(n) for n in f.readline().split()[1:]]
        distances = [int(n) for n in f.readline().split()[1:]]
        races = list(zip(times, distances))

    result = 1
    for time, dis in races:
        b = -time
        c = dis
        x1 = (-b - math.sqrt(b ** 2 - 4 * c)) / 2
        x2 = (-b + math.sqrt(b ** 2 - 4 * c)) / 2
        start = x1 + 1 if x1.is_integer() else math.ceil(x1)
        end = x2 - 1 if x2.is_integer() else math.floor(x2)
        winning_ways = int(end - start + 1)
        result *= winning_ways

    print(result)


if __name__ == '__main__':
    main()
