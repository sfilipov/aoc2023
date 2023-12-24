import math


class Heap:
    _arr = []

    def push(self, item):
        self._arr.append(item)
        item_index = len(self._arr) - 1
        while (parent_index := self._get_parent_index(item_index)) is not None:
            item = self._arr[item_index]
            parent = self._arr[parent_index]

            if item < parent:
                self._swap(item_index, parent_index)
                item_index = parent_index
            else:
                break

    def pop(self):
        length = len(self._arr)
        if length <= 1:
            return self._arr.pop()
        self._swap(0, length - 1)
        result = self._arr.pop()

        parent_index = 0
        while left_index := self._get_left_index(parent_index):
            parent = self._arr[parent_index]
            smaller_child = self._arr[left_index]
            smaller_index = left_index
            if (right_index := self._get_right_index(parent_index)) and (
                right_child := self._arr[right_index]
            ) < smaller_child:
                smaller_child = right_child
                smaller_index = right_index

            if smaller_child < parent:
                self._swap(parent_index, smaller_index)
                parent_index = smaller_index
            else:
                break

        return result

    def _get_parent_index(self, index):
        if index == 0:
            return None
        return (index - 1) // 2

    def _get_left_index(self, index):
        child_index = index * 2 + 1
        if child_index < len(self._arr):
            return child_index
        return None

    def _get_right_index(self, index):
        child_index = index * 2 + 2
        if child_index < len(self._arr):
            return child_index
        return None

    def _swap(self, index_a, index_b):
        a, b = self._arr[index_a], self._arr[index_b]
        self._arr[index_a] = b
        self._arr[index_b] = a

    def __len__(self):
        return len(self._arr)

    def __iter__(self):
        return self

    def __next__(self):
        if self._arr:
            return self.pop()
        else:
            raise StopIteration


class Solution:
    def __init__(self, path):
        with open(path) as f:
            lines = [line.strip() for line in f.readlines()]

        self.n = len(lines)
        self.m = len(lines[0])

        self.heat = {}
        self.dis_heuristic = {}
        for i in range(self.n):
            for j in range(self.m):
                self.dis_heuristic[(i, j)] = self.n + self.m - i - j - 2
                self.heat[(i, j)] = int(lines[i][j])

    def part1(self):
        start = (0, 0)
        end = (self.n - 1, self.m - 1)

        dis_to_start = {(start, ()): 0}
        best_combined = Heap()
        best_combined.push((0, start, ()))

        while best_combined:
            cost, node, path = best_combined.pop()

            if node == end:
                return cost

            for direction, neighbour in self.valid_neighbours(node, path):
                potential_dis = dis_to_start[(node, path[-3:])] + self.heat[neighbour]
                n_tuple = (neighbour, path[-2:] + (direction,))
                if potential_dis < dis_to_start.get(n_tuple, math.inf):
                    dis_to_start[n_tuple] = potential_dis
                    estimate = potential_dis + self.dis_heuristic[neighbour]
                    best_combined.push((estimate, neighbour, path + (direction,)))

    def valid_neighbours(self, node, path):
        if not path:
            return self.all_neighbours(node)

        neighbours = []
        for direction, neighbour in self.all_neighbours(node):
            if self.are_opposite(direction, path[-1]):
                continue
            if (
                len(path) >= 3
                and direction == path[-1]
                and path[-1] == path[-2]
                and path[-2] == path[-3]
            ):
                continue
            neighbours.append((direction, neighbour))
        return neighbours

    def are_opposite(self, a, b):
        return (
            (a == "l" and b == "r")
            or (a == "r" and b == "l")
            or (a == "u" and b == "d")
            or (a == "d" and b == "u")
        )

    def all_neighbours(self, node):
        i, j = node
        neighbours = []
        if i > 0:
            neighbours.append(("u", (i - 1, j)))
        if i < self.n - 1:
            neighbours.append(("d", (i + 1, j)))
        if j > 0:
            neighbours.append(("l", (i, j - 1)))
        if j < self.m - 1:
            neighbours.append(("r", (i, j + 1)))
        return neighbours


if __name__ == "__main__":
    sol = Solution("day17_input.txt")
    print(sol.part1())
