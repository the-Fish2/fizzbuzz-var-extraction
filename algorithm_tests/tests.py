import unittest

from algorithm_tests.test1 import dijkstra
from algorithm_tests.test2 import merge_sort
from algorithm_tests.test3 import a_star
from algorithm_tests.test4 import depth_first_search
from algorithm_tests.test5 import knapsack


class TestDijkstra(unittest.TestCase):
    def test_dijkstra_basic_distances(self):
        graph = {"A": {"B": 4, "C": 2}, "B": {"D": 3}, "C": {"B": 1, "D": 5}, "D": {}}
        distances, paths = dijkstra(graph, "A")
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 3)
        self.assertEqual(distances["D"], 6)

    def test_dijkstra_single_node(self):
        single_node_graph = {"A": {}}
        distances, paths = dijkstra(single_node_graph, "A")
        self.assertEqual(distances["A"], 0)

    def test_dijkstra_disconnected_graph(self):
        disconnected_graph = {"A": {}, "B": {}, "C": {}}
        distances, paths = dijkstra(disconnected_graph, "A")
        for node in disconnected_graph:
            self.assertEqual(distances[node], 0 if node == "A" else float("infinity"))


class TestMergeSort(unittest.TestCase):
    def test_merge_sort_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_merge_sort_already_sorted(self):
        sorted_list = [1, 2, 3, 4, 5]
        self.assertEqual(merge_sort(sorted_list), sorted_list)

    def test_merge_sort_reverse_sorted(self):
        reverse_list = [5, 4, 3, 2, 1]
        self.assertEqual(merge_sort(reverse_list), [1, 2, 3, 4, 5])

    def test_merge_sort_duplicates(self):
        duplicate_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        self.assertEqual(merge_sort(duplicate_list), sorted(duplicate_list))

    def test_merge_sort_large_list(self):
        large_list = list(range(1000, 0, -1))
        self.assertEqual(merge_sort(large_list), list(range(1, 1001)))


class TestAStar(unittest.TestCase):
    def test_astar_clear_path(self):
        grid = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        path = a_star(grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)
        if path:
            self.assertEqual(path[0], (0, 0))
            self.assertEqual(path[-1], (4, 4))

    def test_astar_path_with_obstacles(self):
        grid = [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
        ]
        path = a_star(grid, (0, 0), (4, 4))
        self.assertIsNotNone(path)

    def test_astar_impossible_path(self):
        grid = [
            [0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0],
        ]
        path = a_star(grid, (0, 0), (4, 4))
        self.assertIsNone(path)


class TestDFS(unittest.TestCase):
    def test_dfs_basic_graph(self):
        graph = {
            "A": ["B", "C"],
            "B": ["A", "D", "E"],
            "C": ["A", "F"],
            "D": ["B"],
            "E": ["B", "F"],
            "F": ["C", "E"],
        }
        traversal = depth_first_search(graph, "A")
        self.assertEqual(len(traversal), len(set(traversal)))

    def test_dfs_disconnected_graph(self):
        graph = {"A": ["B"], "B": ["A"], "C": ["D"], "D": ["C"]}
        traversal = depth_first_search(graph, "A")
        self.assertEqual(set(traversal), {"A", "B"})

    def test_dfs_single_node(self):
        graph = {"A": []}
        traversal = depth_first_search(graph, "A")
        self.assertEqual(traversal, ["A"])


class TestKnapsack(unittest.TestCase):
    def test_knapsack_basic(self):
        weights = [10, 20, 30]
        values = [60, 100, 120]
        max_value, selected_items = knapsack(weights, values, 50)
        self.assertEqual(max_value, 220)

    def test_knapsack_no_items_fit(self):
        weights = [60, 70, 80]
        values = [100, 120, 140]
        max_value, selected_items = knapsack(weights, values, 50)
        self.assertEqual(max_value, 0)
        self.assertEqual(selected_items, [])

    def test_knapsack_all_items_fit(self):
        weights = [10, 20, 30]
        values = [60, 100, 120]
        max_value, selected_items = knapsack(weights, values, 100)
        self.assertEqual(max_value, 280)

    def test_knapsack_large_item_set(self):
        weights = list(range(1, 51))
        values = list(range(1, 51))
        max_value, selected_items = knapsack(weights, values, 100)
        self.assertGreater(max_value, 0)

    def test_knapsack_zero_weight_items(self):
        weights = [0, 0, 10, 20, 30]
        values = [50, 50, 60, 100, 120]
        max_value, selected_items = knapsack(weights, values, 50)
        self.assertEqual(max_value, 280)


if __name__ == "__main__":
    unittest.main()
