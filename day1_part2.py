def clean_line(line: str) -> str:
    return (
        line
        .replace('one', 'oonee')
        .replace('two', 'ttwoo')
        .replace('three', 'tthreee')
        .replace('four', 'ffourr')
        .replace('five', 'ffivee')
        .replace('six', 'ssixx')
        .replace('seven', 'ssevenn')
        .replace('eight', 'eeightt')
        .replace('nine', 'nninee')
        .replace('one', '1')
        .replace('two', '2')
        .replace('three', '3')
        .replace('four', '4')
        .replace('five', '5')
        .replace('six', '6')
        .replace('seven', '7')
        .replace('eight', '8')
        .replace('nine', '9')
    )

def num_for_line(line: str) -> int:
    line = clean_line(line)
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
