"""Unit tests of the branch and bound algorithm."""

import unittest
import networkx as nx
from branch_and_bound_tree import branch_and_bound_algorithm
from ip_formulation import ip_algorithm


class TestGraphs(unittest.TestCase):
    """Unit tests for the branch-and-bound algorithm."""

    def test_graph_1(self):
        """Graph with LP ?, IP 8"""
        graph = nx.Graph()
        graph.add_nodes_from([i for i in range(1, 9)])
        graph.add_edges_from([(5, 6), (6, 7), (7, 8), (8, 5)], capacity=2)
        graph.add_edges_from([(1, 5), (2, 6), (3, 7), (4, 8)], capacity=3)
        terminals = range(1, 5)
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)

    def test_graph_2(self):
        """graph with LP 7.5, IP 8"""
        graph = nx.Graph()
        graph.add_nodes_from([1, 2, 3, 12, 13, 23])
        graph.add_edges_from([(1, 12), (1, 13), (2, 12), (2, 23), (3, 13), (3, 23)], capacity=2)
        graph.add_edges_from([(12, 13), (13, 23), (12, 23)], capacity=1)
        terminals = range(1, 4)
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 8)
        _, cut_value = ip_algorithm(graph, terminals, relaxation=True)
        self.assertEqual(cut_value, 7.5)

    def test_graph_3(self):
        """graph with LP 24, IP 26"""
        graph = nx.Graph()
        terminals = range(1, 5)
        graph.add_nodes_from([1, 2, 3, 4, 12, 13, 14, 23, 24, 34])
        graph.add_edges_from([(1, 12), (1, 13), (1, 14),
                              (2, 12), (2, 23), (2, 24),
                              (3, 13), (3, 23), (3, 34),
                              (4, 14), (4, 24), (4, 34)],
                             capacity=3)
        graph.add_edges_from([(12, 13), (12, 14), (12, 23), (12, 24),
                              (13, 14), (13, 23), (13, 34),
                              (14, 24), (14, 34),
                              (23, 24), (23, 34),
                              (24, 34)], capacity=1)
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 26)
        _, cut_value = ip_algorithm(graph, terminals, relaxation=True)
        self.assertEqual(cut_value, 24)

    def test_graph_4(self):
        """graph with LP 26, IP 27"""
        graph = nx.Graph()
        terminals = range(1, 5)
        graph.add_nodes_from([1, 2, 3, 4, 123, 124, 134, 234])
        graph.add_edges_from([(1, 123), (1, 124), (1, 134),
                              (2, 123), (2, 124), (2, 234),
                              (3, 123), (3, 134), (3, 234),
                              (4, 124), (4, 134), (4, 234)],
                             capacity=3)
        graph.add_edges_from([(123, 124), (123, 134), (123, 234),
                              (124, 134), (124, 234),
                              (134, 234)],
                             capacity=1)
        _, cut_value = branch_and_bound_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = ip_algorithm(graph, terminals)
        self.assertEqual(cut_value, 27)
        _, cut_value = ip_algorithm(graph, terminals, relaxation=True)
        self.assertEqual(cut_value, 26)

    #def test_graph_5(self):
    #    # graph with LP 105, IP 110
    #    graph = nx.Graph()
    #    terminals = range(1, 6)
    #    subset_sizes = 3
    #    agreement = 1
    #    graph.add_nodes_from(terminals)
    #    graph.add_nodes_from(itertools.combinations(terminals, subset_sizes))
    #    graph.add_edges_from([(a, b)
    #                          for a in terminals
    #                          for b in itertools.combinations(terminals, subset_sizes)
    #                          if a in set(b)], capacity=5)
    #    graph.add_edges_from([(a, b)
    #                          for a in itertools.combinations(terminals, subset_sizes)
    #                          for b in itertools.combinations(terminals, subset_sizes)
    #                          if len(set(a) & set(b)) == agreement], capacity=1)
    #    partition, cut_value = branch_and_bound_algorithm(graph, terminals)
    #    self.assertEqual(cut_value, 110)

if __name__ == '__main__':
    unittest.main()