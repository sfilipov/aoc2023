def find_rows_symmetry(rows: list[str], known_sym: int | None = None) -> int:
    for axis in range(1, len(rows)):
        to_check = min(axis, len(rows) - axis)
        is_symmetric = True
        for i in range(to_check):
            if is_symmetric and rows[axis - i - 1] != rows[axis + i]:
                is_symmetric = False
        if is_symmetric and axis != known_sym:
            return axis
    return -1


def find_symmetry(
    rows: list[str], columns: list[str], known_sym: tuple[str, int] | None = None
) -> tuple[str, int] | None:
    row_sym = find_rows_symmetry(
        rows, known_sym[1] if known_sym and known_sym[0] == "row" else None
    )
    if row_sym != -1:
        return ("row", row_sym)

    col_sym = find_rows_symmetry(
        columns, known_sym[1] if known_sym and known_sym[0] == "col" else None
    )
    if col_sym != -1:
        return ("col", col_sym)


def columns_for_rows(rows: list[str]) -> list[str]:
    columns = []
    for j in range(len(rows[0])):
        column = []
        for i in range(len(rows)):
            column.append(rows[i][j])
        columns.append("".join(column))
    return columns


def flip_smudge(row: str, index: int) -> str:
    return "".join([row[:index], "." if row[index] == "#" else "#", row[index + 1 :]])


def calc_for_sym(sym: tuple[str, int] | None) -> int:
    if not sym:
        return 0
    axis, pos = sym
    if axis == "row":
        return 100 * pos
    else:
        return pos


def calc_block(rows: list[str], test_smudge: bool) -> int:
    columns = columns_for_rows(rows)

    if not test_smudge:
        return calc_for_sym(find_symmetry(rows, columns))
    else:
        old_symmetry = find_symmetry(rows, columns)
        for i in range(len(rows)):
            for j in range(len(rows[0])):
                rows[i] = flip_smudge(rows[i], j)
                columns[j] = flip_smudge(columns[j], i)

                symmetry = find_symmetry(rows, columns, old_symmetry)
                if symmetry:
                    return calc_for_sym(symmetry)

                rows[i] = flip_smudge(rows[i], j)
                columns[j] = flip_smudge(columns[j], i)

    raise Exception("Invalid block: blocks need axis of symmetry")


def main():
    with open("day13_input.txt") as f:
        blocks: list[list[str]] = []
        for block in f.read().split("\n\n"):
            blocks.append([line for line in block.split("\n") if line])

    result = 0
    for block in blocks:
        result += calc_block(block, test_smudge=False)
    print(result)

    result = 0
    for block in blocks:
        result += calc_block(block, test_smudge=True)
    print(result)


if __name__ == "__main__":
    main()
