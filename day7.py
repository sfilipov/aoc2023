import enum
from collections import Counter
from functools import total_ordering


@total_ordering
class HandType(enum.Enum):
    High = 1
    TwoKind = 2
    TwoPairs = 3
    ThreeKind = 4
    FullHouse = 5
    FourKind = 6
    FiveKind = 7

    def __lt__(self, other):
        return self.value < other.value


CARD_STRENGTH = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def get_hand_type(hand: str) -> HandType:
    counts = [count for card, count in Counter(hand).most_common()]
    if counts[0] == 5:
        return HandType.FiveKind
    if counts[0] == 4:
        return HandType.FourKind
    if counts[0] == 3:
        return HandType.FullHouse if counts[1] == 2 else HandType.ThreeKind
    if counts[0] == 2:
        return HandType.TwoPairs if counts[1] == 2 else HandType.TwoKind
    return HandType.High


def compare_key(hand: str):
    return (get_hand_type(hand), tuple(CARD_STRENGTH[card] for card in hand))


def main():
    with open("day7_input.txt") as f:
        lines = [line.strip().split() for line in f.readlines()]
        hands = [(hand, int(bid)) for hand, bid in lines]

    hands = sorted(hands, key=lambda k: compare_key(k[0]))
    result = 0
    for i, hand_bid in enumerate(hands):
        rank = i + 1
        hand, bid = hand_bid
        result += rank * bid
    print(result)


if __name__ == "__main__":
    main()
