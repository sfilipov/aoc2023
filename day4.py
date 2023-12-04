from collections import defaultdict


def parse_cards(lines: list[str]) -> dict[int, int]:
    cards = {}
    for line in lines:
        card_str, nums = line.split(': ')
        card_id = int(card_str.split('Card')[1].strip())
        win_str, have_str = nums.split(' | ')
        win = set(win_str.split())
        have = set(have_str.split())
        matches = win.intersection(have)
        cards[card_id] = len(matches)
    return cards


def main():
    with open('day4_input.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    cards = parse_cards(lines)

    result_part1 = 0
    for matches in cards.values():
        if matches > 0:
            result_part1 += 2 ** (matches - 1)

    dests = {}
    for card_id, matches in cards.items():
        dests[card_id] = [i for i in range(card_id + 1, card_id + matches + 1)]

    sources = defaultdict(list)
    for card_id, ds in dests.items():
        for dest in ds:
            sources[dest].append(card_id)

    calculated = {}
    for card_id in sorted(cards):
        calculated[card_id] = 1 + sum(calculated[source] for source in sources[card_id])

    result_part2 = sum(calculated.values())

    print(result_part1)
    print(result_part2)


if __name__ == '__main__':
    main()
