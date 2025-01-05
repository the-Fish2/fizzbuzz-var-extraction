import heapq


class Node:
    def __init__(self, position, g=0, h=0):
        self.position = position
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f


def heuristic(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def get_neighbors(grid, node):
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_position = (node.position[0] + dx, node.position[1] + dy)

        if (
            0 <= new_position[0] < len(grid)
            and 0 <= new_position[1] < len(grid[0])
            and grid[new_position[0]][new_position[1]] != 1
        ):
            neighbors.append(new_position)
    return neighbors


def a_star(grid, start, goal):
    start_node = Node(start, h=heuristic(start, goal))
    open_list = []
    heapq.heappush(open_list, start_node)

    closed_set = set()

    while open_list:
        current_node = heapq.heappop(open_list)

        if current_node.position == goal:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node.position)

        for neighbor_pos in get_neighbors(grid, current_node):
            if neighbor_pos in closed_set:
                continue

            neighbor = Node(
                neighbor_pos, g=current_node.g + 1, h=heuristic(neighbor_pos, goal)
            )
            neighbor.parent = current_node

            existing = [n for n in open_list if n.position == neighbor_pos]
            if existing:
                if neighbor.g < existing[0].g:
                    open_list.remove(existing[0])
                    heapq.heappush(open_list, neighbor)
            else:
                heapq.heappush(open_list, neighbor)

    return None
