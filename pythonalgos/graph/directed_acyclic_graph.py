""" Module that contains the definition of a directed acyclic graph
"""

from . import DirectedGraph


class DirectedAcyclicGraph(DirectedGraph):
    """ Class to represent a directed acyclic graph. It inherits from
    DirectedGraph and when calling the __init__ constructor, it will check
    whether the graph adheres to the fact that the graph doesn't contain a
    cycle """

    def __init__(self, vertices):
        """ Initializer that calls the super() initializer and then performs
        the cyclic test to check whether it is a directed acyclic graph """

        super().__init__(vertices)
        if super().is_cyclic():
            raise RuntimeError("Directed graph has a cycle")
