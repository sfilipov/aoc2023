def hash(string):
    h = 0
    for char in string:
        ascii = ord(char)
        h += ascii
        h *= 17
        h %= 256
    return h


def main():
    with open("day15_input.txt") as f:
        line = f.read().replace("\n", "")

    codes = line.split(",")
    result = 0
    for code in codes:
        result += hash(code)
    print(result)

    boxes = {}
    order = 0
    for code in codes:
        if "=" in code:
            label, lens = code.split("=")
        else:
            label = code.split("-")[0]
            lens = None

        box_id = hash(label)
        existing = boxes.setdefault(box_id, {})
        if lens:
            new_order = order if label not in existing else existing[label][0]
            existing[label] = (new_order, int(lens))
        elif label in existing:
            del existing[label]

        order += 1

    result = 0
    for box_id, lenses in boxes.items():
        lenses = [lens for order, lens in sorted(lenses.values())]
        for i, lens in enumerate(lenses):
            result += (box_id + 1) * (i + 1) * lens
    print(result)


if __name__ == "__main__":
    main()
