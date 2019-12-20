""" Module that contains test for the strongly connected components
functionality of the directed graph
"""

import unittest
from pythonalgos.graph.directed_graph import DirectedGraph
import os
import time
from pythonalgos.util.logging import Logging
import util.path_tools as pt
from os import path


class TestDirectedGraphSCCs(unittest.TestCase):

    def setUp(self):
        pass

    def test_create_sccs_nontrivial(self):
        self.vertices = {0: [1], 1: [2, 3], 2: [3], 3: [4],
                         4: [5, 2], 5: [6], 6: [7], 7: [5], 8: [8], 9: []}
        self.directed_graph = DirectedGraph(self.vertices)
        sccs = self.directed_graph.create_sccs_kosaraju_dfs()
        sccs_expected = [[2, 3, 4], [5, 6, 7], [8]]
        for vertices in sccs:
            sorted_vertices = sorted(list(vertices))
            if sorted_vertices not in sccs_expected:
                self.assertFalse(True, msg=str(
                    sorted_vertices) + " not in expected sccs")

    def test_create_sccs_extra(self):
        self.vertices = {"A": ["B"], "B": ["C", "D"], "C": ["A"], "D": ["E"], "E": ["F"],
                         "F": ["D"], "G": ["F", "H"], "H": ["I"], "I": ["J"], "J": ["G", "K"], "K": []}
        self.directed_graph = DirectedGraph(self.vertices)
        sccs = self.directed_graph.create_sccs_kosaraju_dfs(nontrivial=False)
        sccs_expected = [["A", "B", "C"], [
            "D", "E", "F"], ["G", "H", "I", "J"], ["K"]]
        for vertices in sccs:
            sorted_vertices = sorted(list(vertices))
            if sorted_vertices not in sccs_expected:
                self.assertFalse(True, msg=str(
                    sorted_vertices) + " not in expected sccs")
    
    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
