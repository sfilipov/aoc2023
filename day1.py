def num_for_line(line: str) -> int:
    first, last = None, None
    for char in line:
        if not char.isdigit():
            continue
        digit = int(char)
        if not first:
            first = digit
        last = digit

    return 10 * first + last


def main():
    with open('day1_input.txt', 'r') as f:
        lines = f.readlines()
    result = 0
    for line in lines:
        result += num_for_line(line)
    print(result)

if __name__ == '__main__':
    main()
