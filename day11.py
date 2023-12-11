def expand_image(image: list[str]) -> tuple[set[int], set[int]]:
    expanded_rows = set()
    for i, row in enumerate(image):
        if all(char == "." for char in row):
            expanded_rows.add(i)

    expanded_cols = set()
    for j in range(len(image[0])):
        if all(row[j] == "." for row in image):
            expanded_cols.add(j)

    return (expanded_rows, expanded_cols)


def find_galaxies(
    image: list[str],
    expanded_rows: set[int],
    expanded_cols: set[int],
    expansion_factor: int,
) -> dict[int, tuple[int, int]]:
    galaxies = {}
    next_id = 0
    num_row_expansions = 0
    for i, row in enumerate(image):
        if i in expanded_rows:
            num_row_expansions += 1
            continue
        num_col_expansions = 0
        for j, char in enumerate(row):
            if j in expanded_cols:
                num_col_expansions += 1
                continue
            if char == "#":
                row_index = i + num_row_expansions * expansion_factor
                col_index = j + num_col_expansions * expansion_factor
                galaxies[next_id] = (row_index, col_index)
                next_id += 1
    return galaxies


def calc_distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    a_x, a_y = a
    b_x, b_y = b
    dis_x = abs(a_x - b_x)
    dis_y = abs(a_y - b_y)
    return dis_x + dis_y


def calc_distances_sum(
    image: list[str],
    expanded_rows: set[int],
    expanded_cols: set[int],
    expansion_factor: int,
) -> int:
    galaxies = find_galaxies(image, expanded_rows, expanded_cols, expansion_factor)
    result = 0
    for gal_i, pos_i in galaxies.items():
        for gal_j, pos_j in galaxies.items():
            if gal_i < gal_j:
                result += calc_distance(pos_i, pos_j)
    return result


def main():
    with open("day11_input.txt") as f:
        image = [line.strip() for line in f.readlines()]

    expanded_rows, expanded_cols = expand_image(image)
    print(calc_distances_sum(image, expanded_rows, expanded_cols, 1))
    print(calc_distances_sum(image, expanded_rows, expanded_cols, 999_999))


if __name__ == "__main__":
    main()
