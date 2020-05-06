from __future__ import annotations
from . vertex import Vertex
from copy import deepcopy
from typing import Set, Mapping, Any, List
from . edge import Edge

""" Module that contains the definition of a directed graph as a class """


class DirectedGraphCore(object):
    """ Directed graph core class, it just contains the pure defintion of the
    concept, not the extra functionalities, like calculating sccs, etc.. """

    def __init__(self, vertices: Mapping[Any, List[Any]] = None):
        """ Initialises a directed graph (with the provided vertices)

        Args:
            vertices(dict): a dict with the vertices and their tails in it
        """

        self._vertices: Set[Vertex] = set()
        if vertices is not None:
            for label in vertices.keys():
                self.add_vertex(label)
            for label, heads in vertices.items():
                for head in heads:
                    self.add_edge(self.get_vertex(label),
                                  self.get_vertex(head))

    def get_vertex(self, label: Any):
        """ Returns the vertex that coincides with the label

        Args:
            label: the label of the vertex

        Returns:
            The vertex object
        """
        for vertex in self._vertices:
            if vertex.get_label() == label:
                return vertex

        raise RuntimeError(f"label {label} couldn't be found in vertices")

    def copy(self) -> DirectedGraphCore:
        """ Copies the directed graph and returns it

        Returns:
            the copied directed graph """

        return deepcopy(self)

    def add_vertex(self, label: Any):
        """ Adds a vertex to the dictionary of vertices

        Args:
            label: a vertex represented by its label """

        for vertex in self._vertices:
            if vertex.get_label() == label:
                raise RuntimeError(
                    f"Vertex = {label} is already a vertex in this directed " +
                    " graph")

        self._vertices.add(Vertex(label))

    def get_vertices(self) -> Set[Vertex]:
        """ Returns the vertices set

        Returns
            self._vertices """

        return self._vertices

    def add_edge(self, tail: Vertex, head: Vertex):
        """ Adds an edge to the graph, the edge is identified by a tail and
        a head vertex.

        Args:
            tail: the edge that represents the start vertex
            head: the edge that represents the destination vertex """

        tail.add_edge(head)
        head.increase_indegree()

    def get_all_edges(self) -> Set[Edge]:
        """ Method that retrieves all edges of all vertices

        Returns:
            set(): A set of all edges in the directed graph """

        return {e for v in self._vertices for e in v.get_edges()}

    def get_reversed_graph(self) -> DirectedGraphCore:
        """ Function that returns the reverse of this graph

        Args:
            directed_graph (DirectedGraph): The directed graph

        Returns:
            DirectedGraph: The reversed graph """

        reversed = DirectedGraphCore()
        for i in self.get_vertices():
            reversed.add_vertex(i.get_label())

        for tail in self.get_vertices():
            for head in tail.get_heads():
                reversed.add_edge(tail, head)

        return reversed

    def get_vertices_count(self) -> int:
        return len(self._vertices)

    def __str__(self):
        res = ""
        for vertex in self._vertices:
            res += "\n" + str(vertex)

        return res
