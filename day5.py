from typing import NamedTuple


class Range(NamedTuple):
    src_start: int
    src_end: int
    diff: int


def parse_map(lines: list[str]) -> list[Range]:
    result = []
    for line in lines:
        if not line:
            continue
        if not line[0].isdigit():
            continue
        dest_start, src_start, r_len = map(int, line.split())
        result.append(Range(src_start, src_start + r_len - 1, dest_start - src_start))

    return sorted(result)


def remap_number(ranges: list[Range], number: int) -> int:
    for r in ranges:
        if r.src_start <= number <= r.src_end:
            return number + r.diff
    return number


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

    locations = []
    for seed in seeds:
        soil = remap_number(seed_to_soil, seed)
        fer = remap_number(soil_to_fer, soil)
        water = remap_number(fer_to_water, fer)
        light = remap_number(water_to_light, water)
        temp = remap_number(light_to_temp, light)
        hum = remap_number(temp_to_hum, temp)
        loc = remap_number(hum_to_loc, hum)
        locations.append(loc)

    print(sorted(locations)[0])


if __name__ == '__main__':
    main()
