from typing import List, NamedTuple
from parser import *


class Checker:
    def __init__(self, nodes):
        self.nodes: List[Node] = nodes
        self.symbols: List[NamedTuple] = []

    def declare_symbol(self):
        pass

    def check(self):
        for n in self.nodes:
            if n.type == NodeDatapack:
                self.check_datapack(n)
            elif n.type == NodeFunction:
                pass
            else:
                raise Exception("Internal compiler error: Invalid top level node: {}".format(n.type))

    def check_datapack(self, n):
        pass
