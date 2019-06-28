from typing import List, NamedTuple
from .parser import *

import re

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
        self.found_datapack = False
        self.name = ''
        self.namespace = ''
        self.description = ''
        self.valid_namespace_regex = re.compile(r'[a-z0-9_]+')

    def declare_symbol(self):
        pass

    def check(self):
        for n in self.nodes:
            if isinstance(n, NodeDatapack):
                self.check_datapack(n)
            elif n.type == NodeFunction:
                self.check_function(n)
            else:
                raise Exception("Internal compiler error: Invalid top level node: {}".format(n.type))

    def check_function(self, n: NodeFunction):
        pass

    @staticmethod
    def checker_error(msg: str, token: Token):
        stderr.write("{}({}:{}): Checker Error: {}".format(token.filepath, token.line, token.column, msg))
        exit(1)

    def check_datapack(self, n: NodeDatapack):
        if self.found_datapack:
            self.checker_error("Found duplicate 'datapack' statement", n.tok)

        self.found_datapack = True

        for name, (opt, tok) in n.options.items():
            if name == 'name':
                self.name = opt
            elif name == 'namespace':
                if self.valid_namespace_regex.fullmatch(opt):
                    self.namespace = opt
                else:
                    self.checker_error("Namespaces can only contain lowercase letters, numbers and underscores(_), got '{}'".format(opt), tok)
            elif name == 'description':
                self.description = opt
            elif name == 'path':
                pass
            else:
                stderr.write("Unknown datapack option '{}'".format(opt))
                exit(1)

        if 'name' not in n.options:
            self.checker_error("'datapack' option 'name' is missing", n.tok)

        if 'namespace' not in n.options:
            self.checker_error("'datapack' option 'namepsace' is missing", n.tok)
