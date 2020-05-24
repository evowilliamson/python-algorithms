from pythonalgos.util.advisor import Advisor
from pythonalgos.graph.vertex import Vertex
from .. util.logging import Logging
from . directed_graph_core import DirectedGraphCore
from typing import Any, List, MutableMapping, Set

""" Module that contains the logic for kosaraju's SCCs algorithm
"""


def create_sccs_kosaraju_dfs(directed_graph: DirectedGraphCore,
                             nontrivial: bool,
                             advisor: Advisor
                             ) -> List[Set[Vertex]]:
    """ Function that creates a list of strongly connected components
    according to Kosaraju's algorithm
    (https://en.wikipedia.org/wiki/Kosaraju%27s_algorithm) with a
    depth-first-search approach.

    Args:
        directed_graph (DirectedGraph): The directed graph for which the SCCS
            should be calculated nontrivial(bool): If True, only nontrivial
            sccs will be returned, otherwise all sccs
        nontrivial: if true, retrieves the nontrivial sccs, if not, also the
            trivial ones
        advisor(Advisor): Object that contains advice which can be inserted at
            join points

    Returns:
        list(set()) of SCCs: Each SCC is a set of vertices
    """

    dg = directed_graph.copy()

    def filter_nontrivial(sccs_trivial: List[Set[Vertex]]) -> \
            List[Set[Vertex]]:
        """ This function filters out the trivial sccs

        A scc is nontrivial, iff there are at least two vertices in it,
        or there is only one vertex with a self-loop. A self-loop means
        that the indegree and the outdegree are both 1 and the tail is equal
        to the head

        Args:
            sccs(list): The list of trivial sccs

        Returns:
            sccs_nontrivial(list): The list of nontrivial sccs
        """

        sccs_non_trivial = list()
        for scc in sccs_trivial:
            vertex = next(iter(scc))
            if len(scc) >= 2 or \
                (len(scc) == 1 and vertex.get_indegree() == 1 and
                    vertex.get_outdegree() == 1 and
                    vertex.get_edge_heads()[0] == vertex):
                sccs_non_trivial.append(scc)

        return sccs_non_trivial

    def visit_dfs_sccs(vertex: Vertex, visited: MutableMapping[Any, bool], 
                       scc: Set[Vertex]):
        """ Function that performs a recursive depth first search on the
        directed graph to check whether vertices have been visisted

        Args:
            vertex (label): The current vertex
            visited (dict): A dictionary that maintains whether vertices have
                been visited
            scc (set): The current scc being constructed
        """

        visited[vertex] = True
        scc.add(vertex)
        for head in vertex.get_edge_heads():
            if visited.get(head) is None:
                visit_dfs_sccs(head, visited, scc)

    def fill_order_dfd_sccs(vertex: Vertex, 
                            visited: MutableMapping[Vertex, bool],
                            stack: List[Vertex]):
        """ Function that covers the first part of the algorith by determining
        the order of vertices, traversing the graph with a depth first search,
        recursively.

        Args:
            vertex(str): The current vertex
            visited (dict): A dictionary that maintains whether vertices have
                been visited
            stack (list): stack that will be processed, used to inverse the
                order
        """

        visited[vertex] = True
        advisor.advise("visit_vertex", dg, vertex)
        for head in vertex.get_edge_heads():
            if visited.get(head) is None:
                fill_order_dfd_sccs(head, visited, stack)
        advisor.advise("add_vertex_to_stack", dg, vertex)
        stack.append(vertex)

    stack: List[Vertex] = list()
    sccs: List[Set[Vertex]] = list()
    visited: MutableMapping[Vertex, bool] = dict()
    for vertex in dg.get_vertices():
        if visited.get(vertex) is None:
            fill_order_dfd_sccs(vertex, visited, stack)
        else:
            Logging.log("Vertex {0} already visited, skipping", vertex)

    visited = dict()
    dg.reversed()
    advisor.advise("reverse_directed_graph", dg)
    for i in reversed(stack):
        if visited.get(i) is None:
            sccs.append(set())
            visit_dfs_sccs(i, visited, sccs[-1])

    return filter_nontrivial(sccs) if nontrivial else sccs
