from typing import NamedTuple


class Range(NamedTuple):
    start: int
    end: int


def parse_map(lines: list[str]) -> list[tuple[Range, int]]:
    result = []
    for line in lines:
        if not line:
            continue
        if not line[0].isdigit():
            continue
        dest_start, src_start, r_len = map(int, line.split())
        result.append((Range(src_start, src_start + r_len - 1), dest_start - src_start))

    return sorted(result)


def intersect(src: Range, dest: Range):
    if src.end < dest.start:
        return (src, None, None)
    if src.start > dest.end:
        return (None, None, src)

    before = Range(src.start, dest.start - 1) if src.start < dest.start else None
    inter = Range(max(src.start, dest.start), min(src.end, dest.end))
    after = Range(dest.end + 1, src.end) if src.end > dest.end else None
    return (before, inter, after)


def remap_range(src_ranges: list[Range], dest_ranges: list[tuple[Range, int]]) -> list[Range]:
    if not src_ranges:
        return []

    result: list[Range] = []
    i = 0
    j = 0
    current_src = None
    while i < len(src_ranges) or current_src:
        if not current_src:
            current_src = src_ranges[i]

        if j < len(dest_ranges):
            current_dest, diff = dest_ranges[j]
            before, inter, after = intersect(current_src, current_dest)
            if inter:
                if before:
                    result.append(before)

                result.append(Range(inter.start + diff, inter.end + diff))

                if after:
                    current_src = after
                    j += 1
                else:
                    current_src = None
                    i += 1

            else:
                if before:
                    result.append(before)
                    current_src = None
                    i += 1

                if after:
                    current_src = after
                    j += 1

        else:
            result.append(current_src)
            current_src = None
            i += 1

    return sorted(result)


def main():
    with open('day5_input.txt') as f:
        blocks = (block.split('\n') for block in f.read().split('\n\n'))

    seeds = [int(seed_str) for seed_str in next(blocks)[0].split(': ')[1].split()]
    seed_to_soil = parse_map(next(blocks))
    soil_to_fer = parse_map(next(blocks))
    fer_to_water = parse_map(next(blocks))
    water_to_light = parse_map(next(blocks))
    light_to_temp = parse_map(next(blocks))
    temp_to_hum = parse_map(next(blocks))
    hum_to_loc = parse_map(next(blocks))

    def transform_seeds(seeds: list[Range]) -> int:
        soil = remap_range(seeds, seed_to_soil)
        fer = remap_range(soil, soil_to_fer)
        water = remap_range(fer, fer_to_water)
        light = remap_range(water, water_to_light)
        temp = remap_range(light, light_to_temp)
        hum = remap_range(temp, temp_to_hum)
        loc = remap_range(hum, hum_to_loc)
        return loc[0].start

    seeds_part1 = sorted(Range(seed, seed) for seed in seeds)
    print(transform_seeds(seeds_part1))

    seeds_part2: list[Range] = []
    for i in range(0, len(seeds), 2):
        start, r_len = seeds[i], seeds[i + 1]
        end = start + r_len - 1
        seeds_part2.append(Range(start, end))
    seeds_part2.sort()
    print(transform_seeds(seeds_part2))


if __name__ == '__main__':
    main()
