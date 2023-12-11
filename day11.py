def expand_image(image: list[str]) -> None:
    i = 0
    while i < len(image):
        if all(char == "." for char in image[i]):
            image.insert(i, image[i])
            i += 2
        else:
            i += 1

    j = 0
    while j < len(image[0]):
        if all(row[j] == "." for row in image):
            for i, row in enumerate(image):
                image[i] = row[:j] + "." + row[j:]
            j += 2
        else:
            j += 1


def find_galaxies(image: list[str]) -> dict[int, tuple[int, int]]:
    galaxies = {}
    next_id = 0
    for i, row in enumerate(image):
        for j, char in enumerate(row):
            if char == "#":
                galaxies[next_id] = (i, j)
                next_id += 1
    return galaxies


def calc_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    a_x, a_y = a
    b_x, b_y = b
    dis_x = abs(a_x - b_x)
    dis_y = abs(a_y - b_y)
    return dis_x + dis_y


def main():
    with open("day11_input.txt") as f:
        image = [line.strip() for line in f.readlines()]

    expand_image(image)
    galaxies = find_galaxies(image)

    result_part1 = 0
    for gal_i, pos_i in galaxies.items():
        for gal_j, pos_j in galaxies.items():
            if gal_i < gal_j:
                result_part1 += calc_distance(pos_i, pos_j)

    print(result_part1)


if __name__ == "__main__":
    main()
