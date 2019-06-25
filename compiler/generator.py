from .parser import *
from typing import List
import zipfile


class Generator:
    def __init__(self, nodes: List[Node], path, zipped):
        self.nodes = nodes
        self.path = path
        self.zipped = zipped

        self.zip = zipfile.ZipFile(path, mode='w')
        self.zip.writestr("data/ticker/functions/tick.mcfunction", "/say Tick\n")
        self.zip.extractall(path='./Test/')
        self.zip.close()

    def generate(self):
        pass
