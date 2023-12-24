import math


# NOTE deliberately implementing heap instead of using heapq just for the coding practice
class Heap:
    def __init__(self):
        self._arr = []

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
                # NOTE using A* instead of Djikstra but it makes little difference in our case
                self.dis_heuristic[(i, j)] = self.n + self.m - i - j - 2
                self.heat[(i, j)] = int(lines[i][j])

    def part1(self):
        return self.solve(1, 3)

    def part2(self):
        return self.solve(4, 10)

    def solve(self, min_moves, max_moves):
        # NOTE idea for pushing all going forward is from reddit
        # https://old.reddit.com/r/adventofcode/comments/18k9ne5/2023_day_17_solutions/kdq86mr/

        start = (0, 0)
        end = max(self.heat)

        best_candidate = Heap()
        best_candidate.push((0, start, (0, 0)))
        cost_to_start = {(start, (0, 0)): 0}
        seen = set()

        while best_candidate:
            _, (x, y), (dir_x, dir_y) = best_candidate.pop()
            key = ((x, y), (dir_x, dir_y))
            if (x, y) == end:
                return cost_to_start[key]

            if key in seen:
                continue
            seen.add(key)

            valid_dirs = {(0, -1), (0, 1), (-1, 0), (1, 0)} - {
                (dir_x, dir_y),
                (-dir_x, -dir_y),
            }
            for dx, dy in valid_dirs:
                new_x, new_y = x, y
                new_cost = cost_to_start[key]
                for i in range(1, max_moves + 1):
                    new_x, new_y = new_x + dx, new_y + dy
                    pos, dir = (new_x, new_y), (dx, dy)
                    if pos not in self.heat:
                        continue
                    new_cost += self.heat[pos]
                    if i >= min_moves:
                        if new_cost < cost_to_start.get((pos, dir), math.inf):
                            cost_to_start[pos, dir] = new_cost
                        f_cost = new_cost + self.dis_heuristic[pos]
                        best_candidate.push((f_cost, pos, dir))


if __name__ == "__main__":
    sol = Solution("day17_input.txt")
    print(sol.part1())
    print(sol.part2())
