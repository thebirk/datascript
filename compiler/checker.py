from typing import List, NamedTuple
from parser import *


# It is the job of the Checker to make sure the following is correct
# All functions tags are valid
# There are no duplicate symbol names(functions, variables, etc.)
# All the datapack options are correct, and the requires options are set
#
# Checker could probably be worked into the Generator


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
