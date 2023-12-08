from typing import NamedTuple


class Node(NamedTuple):
    name: str
    left: str
    right: str


def travel(nodes_map, node, direction):
    next_node_name = node.left if direction == "L" else node.right
    return nodes_map[next_node_name]


def gcd(a: int, b: int) -> int:
    a, b = max(a, b), min(a, b)
    while a % b != 0:
        r = a % b
        a, b = b, r
    return b


def lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def main():
    with open("day8_input.txt") as f:
        command, nodes_str = f.read().split("\n\n")

    nodes_map: dict[str, Node] = {}
    for node_str in nodes_str.strip().split("\n"):
        name, left_right_str = node_str.split(" = ")
        left, right = left_right_str[1:-1].split(", ")
        nodes_map[name] = Node(name, left, right)

    current = nodes_map["AAA"]
    result = 0
    while current.name != "ZZZ":
        for direction in command:
            next_node_name = current.left if direction == "L" else current.right
            current = nodes_map[next_node_name]
            result += 1
    print(result)

    currents = [node for node in nodes_map.values() if node.name.endswith("A")]
    cycles = []
    for current in currents:
        count = 0
        while not current.name.endswith("Z"):
            for direction in command:
                current = travel(nodes_map, current, direction)
                count += 1
        cycles.append(count)

    result = 1
    for cycle in cycles:
        result = lcm(result, cycle)
    print(result)


if __name__ == "__main__":
    main()
