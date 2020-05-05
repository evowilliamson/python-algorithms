from __future__ import annotations
from . vertex import Vertex
from copy import deepcopy
from typing import Set
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

        self._vertices = dict()
        if vertices is not None:
            for label in vertices.keys():
                self.add_vertex(label)
            for label, heads in vertices.items():
                for head in heads:
                    self.add_edge(label, head)

    def copy(self) -> DirectedGraphCore:
        """ Copies the directed graph and returns it

        Returns:
            the copied directed graph """

        return deepcopy(self)

    def add_vertex(self, label: Any):
        """ Adds a vertex to the dictionary of vertices

        Args:
            label: a vertex represented by its label """

        if label in self._vertices:
            raise RuntimeError("vertex = '{}'".format(label) +
                               " is already a vertex in this directed graph")
        self._vertices[label] = Vertex(label)

    def get_vertex(self, label: Any) -> Vertex:
        """ Returns the vertex that coincides with the label

        Args:
            label: a vertex represented by its label

        Returns:
            Vertex: the requested vertex """

        return self._vertices[label]

    def get_vertices(self) -> Mapping[Any, Vertex]:
        """ Returns the vertices dictionary

        Returns
            self._vertices (dict) """

        return self._vertices

    def add_edge(self, tail: Any, head: Any):
        """ Adds an edge to the graph, the edge is identified by a tail and
        a head vertex.

        Args:
            tail: the edge that represents the start vertex
            head: the edge that represents the destination vertex """

        if tail not in self._vertices or head not in self._vertices:
            raise RuntimeError("Destination or source of edge ('{}'"
                               .format(tail) + ",'{}'".format(head) +
                               ") cannot be found as a vertex")
        else:
            self._vertices[tail].add_edge(self._vertices[head])
            self._vertices[head].increase_indegree()

    def get_all_edges(self) -> Set[Edge]:
        """ Method that retrieves all edges of all vertices

        Returns:
            set(): A set of all edges in the directed graph """

        return {e for v in self._vertices.values() for e in v.get_edges()}

    def get_vertices_count(self) -> int:
        return len(self._vertices)

    def __str__(self):
        res = ""
        for label in self._vertices:
            res += "\n" + str(label) + ": " + str(self._vertices[label])

        return res
