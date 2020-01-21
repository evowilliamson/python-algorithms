""" Module that contains a main function that trails the directe graph.

A directed trail is a walk where edges are not repeated. Edges are traversed in a certain
order, which is dictated by the data structure that holds the edges.

Calls to advice insertions are included at joi -points. These calls belong to a
abstract class Advisor, which must be implemented by interested parties

"""

from .. util.advisor import Advisor
from . directed_graph import DirectedGraph
from . vertex import Vertex
from . edge import Edge


def trail(directed_graph, advisor: Advisor):
    """ Main function that walks the directed graph, restricted by the trail feature
    (no edge repetitions)

    Args:
        directed_graph (DirectedGraph): The directed graph
        advisor (Advisor): Object that contains advice which can be inserted at join points

    """

    _advisor = advisor

    VISITED = "visited"

    def is_edge_visited(edge: Edge):
        if edge.get_attr(VISITED):
            return True
        else:
            return False

    def _trail_dfs(directed_graph: DirectedGraph, vertex: Vertex):
        """ Function that recursively walks the directed graph

        Args:
            directed_graph (DirectedGraph): The directed graph
            vertex (Vertex): The current vertex
        """

        advisor.advise("visit_vertex", directed_graph, vertex)
        for edge in vertex.get_edges():
            if not is_edge_visited(edge):
                edge.set_attr(VISITED, True)
                advisor.advise("edge_not_visited", directed_graph, edge)
                _trail_dfs(directed_graph, edge.get_head())
            else:
                advisor.advise("edge_visited_already", directed_graph, edge)

        return False

    for label, vertex in directed_graph.get_vertices().items():
        _trail_dfs(directed_graph, vertex)
