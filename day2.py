MAX_COLOR = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


def parse_game(game: str) -> tuple[int, dict[str, int]]:
    seen = {
        'red': 0,
        'green': 0,
        'blue': 0,
    }
    game_str, draws = game.split(': ')
    game_id = int(game_str.split('Game ')[1])
    draws = draws.split('; ')
    for draw in draws:
        num_colors = draw.split(', ')
        for num_color in num_colors:
            num = int(num_color.split(' ')[0])
            color = num_color.split(' ')[1].strip()
            if num > seen[color]:
                seen[color] = num

    for color, value in seen.items():
        if value > MAX_COLOR[color]:
            game_id = 0

    return game_id, seen


def main():
    with open('day2_input.txt', 'r') as f:
        games = f.readlines()

    part1_sum = 0
    part2_sum = 0
    for game in games:
        game_id, seen = parse_game(game)
        part1_sum += game_id
        part2_sum += seen['red'] * seen['green'] * seen['blue']

    print(f'Valid games sum: {part1_sum}')
    print(f'Power sum: {part2_sum}')


if __name__ == '__main__':
    main()
