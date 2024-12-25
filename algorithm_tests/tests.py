import unittest

from algorithm_tests.test1 import dijkstra #type: ignore
from algorithm_tests.test2 import merge_sort #type: ignore
from algorithm_tests.test3 import a_star #type: ignore
from algorithm_tests.test4 import depth_first_search #type: ignore
from algorithm_tests.test5 import knapsack #type: ignore

class TestDijkstra(unittest.TestCase):
    def test_dijkstra_basic(self):
        # Basic graph test
        graph = {
            'A': {'B': 4, 'C': 2},
            'B': {'D': 3},
            'C': {'B': 1, 'D': 5},
            'D': {}
        }
        distances, paths = dijkstra(graph, 'A')
        
        # Check specific distances
        self.assertEqual(distances['A'], 0)
        self.assertEqual(distances['B'], 3)
        self.assertEqual(distances['D'], 6)
    
    def test_dijkstra_edge_cases(self):
        # Single node graph
        single_node_graph = {'A': {}}
        distances, paths = dijkstra(single_node_graph, 'A')
        self.assertEqual(distances['A'], 0)
        
        # Disconnected graph
        disconnected_graph = {
            'A': {},
            'B': {},
            'C': {}
        }
        distances, paths = dijkstra(disconnected_graph, 'A')
        for node in disconnected_graph:
            self.assertEqual(distances[node], 0 if node == 'A' else float('infinity'))

class TestMergeSort(unittest.TestCase):
    def test_merge_sort_various_inputs(self):
        # Empty list
        self.assertEqual(merge_sort([]), [])
        
        # Already sorted list
        sorted_list = [1, 2, 3, 4, 5]
        self.assertEqual(merge_sort(sorted_list), sorted_list)
        
        # Reverse sorted list
        reverse_list = [5, 4, 3, 2, 1]
        self.assertEqual(merge_sort(reverse_list), [1, 2, 3, 4, 5])
        
        # List with duplicates
        duplicate_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
        self.assertEqual(merge_sort(duplicate_list), sorted(duplicate_list))
        
        # Large list
        large_list = list(range(1000, 0, -1))
        self.assertEqual(merge_sort(large_list), list(range(1, 1001)))
    

class TestAStar(unittest.TestCase):
    def test_astar_pathfinding(self):
        # Basic grid with clear path
        grid1 = [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
        path1 = a_star(grid1, (0, 0), (4, 4))
        self.assertIsNotNone(path1)
        if path1:
            self.assertEqual(path1[0], (0, 0))
            self.assertEqual(path1[-1], (4, 4))
        
        # Grid with obstacles
        grid2 = [
            [0, 0, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 0, 0]
        ]
        path2 = a_star(grid2, (0, 0), (4, 4))
        self.assertIsNotNone(path2)
        
        # Impossible path (completely blocked)
        grid3 = [
            [0, 1, 0, 0, 0],
            [1, 1, 1, 1, 0],
            [0, 1, 0, 0, 0],
            [0, 1, 1, 1, 0],
            [0, 0, 0, 1, 0]
        ]
        path3 = a_star(grid3, (0, 0), (4, 4))
        self.assertIsNone(path3)
    

class TestDFS(unittest.TestCase):
    def test_depth_first_search(self):
        # Basic graph
        graph1 = {
            'A': ['B', 'C'],
            'B': ['A', 'D', 'E'],
            'C': ['A', 'F'],
            'D': ['B'],
            'E': ['B', 'F'],
            'F': ['C', 'E']
        }
        traversal1 = depth_first_search(graph1, 'A')
        self.assertEqual(len(traversal1), len(set(traversal1)))
        
        # Disconnected graph
        graph2 = {
            'A': ['B'],
            'B': ['A'],
            'C': ['D'],
            'D': ['C']
        }
        traversal2 = depth_first_search(graph2, 'A')
        self.assertEqual(set(traversal2), {'A', 'B'})
        
        # Single node graph
        graph3 = {'A': []}
        traversal3 = depth_first_search(graph3, 'A')
        self.assertEqual(traversal3, ['A'])
    

class TestKnapsack(unittest.TestCase):
    def test_knapsack(self):
        # Basic test case
        weights1 = [10, 20, 30]
        values1 = [60, 100, 120]
        max_value1, selected_items1 = knapsack(weights1, values1, 50)
        self.assertEqual(max_value1, 220)
        
        # No items fit
        weights2 = [60, 70, 80]
        values2 = [100, 120, 140]
        max_value2, selected_items2 = knapsack(weights2, values2, 50)
        self.assertEqual(max_value2, 0)
        self.assertEqual(selected_items2, [])
        
        # All items fit
        weights3 = [10, 20, 30]
        values3 = [60, 100, 120]
        max_value3, selected_items3 = knapsack(weights3, values3, 100)
        self.assertEqual(max_value3, 280)
        
        # Large number of items
        weights4 = list(range(1, 51))
        values4 = list(range(1, 51))
        max_value4, selected_items4 = knapsack(weights4, values4, 100)
        self.assertGreater(max_value4, 0)
        
        # Edge case with zero-weight items
        weights5 = [0, 0, 10, 20, 30]
        values5 = [50, 50, 60, 100, 120]
        max_value5, selected_items5 = knapsack(weights5, values5, 50)
        self.assertEqual(max_value5, 280)

if __name__ == '__main__':
    unittest.main()