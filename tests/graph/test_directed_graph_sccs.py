""" Module that contains test for the strongly connected components
functionality of the directed graph
"""

import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
from typing import List, Set
from pythonalgos.graph.vertex import Vertex


class TestDirectedGraphSCCs(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_sccs_nontrivial(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4],
                         4: [5, 2], 5: [6], 6: [7], 7: [5], 8: [8], 9: []}
        self.directed_graph = DirectedGraph(self.vertices)
        sccs_labels = {frozenset(v.get_label() for v in s)
                       for s in self.directed_graph.create_sccs_kosaraju_dfs()}
        sccs_expected = {frozenset([2, 3, 4]), frozenset([5, 6, 7]),
                         frozenset([8])}
        self.assertTrue(sccs_expected == sccs_labels)

    def test_create_sccs_trivial(self):
        self.vertices = {"A": ["B"], "B": ["C", "D"], "C": ["A"], "D": ["E"],
                         "E": ["F"], "F": ["D"], "G": ["F", "H"], "H": ["I"],
                         "I": ["J"], "J": ["G", "K"], "K": []}
        self.directed_graph = DirectedGraph(self.vertices)
        sccs_labels = {frozenset(v.get_label() for v in s)
                       for s in self.directed_graph.create_sccs_kosaraju_dfs(
                            nontrivial=False)}
        sccs_expected = \
            {frozenset(["A", "B", "C"]), frozenset(["D", "E", "F"]),
             frozenset(["G", "H", "I", "J"]), frozenset(["K"])}
        self.assertTrue(sccs_expected == sccs_labels)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
