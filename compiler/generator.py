from .parser import *
from typing import List
import zipfile
import pathlib


class Generator:
    def __init__(self, nodes: List[Node], in_path, zipped):
        self.nodes = nodes
        self.zipped = zipped

        # Look into using io.BytesIO() for generating the ZipFile in memory
        # And then either write it to file or extract to a dir
        # To write the zipfile, .getvalue() on a BytesIO returns bytes

        path = pathlib.Path(in_path)
        if path.exists() and not path.is_dir():
            stderr.write("Target path '{}' already exists and is not a directory\n".format(path))
        self.filename = path.joinpath("{}.zip".format("Test"))

        if not path.exists():
            path.mkdir(parents=True)

        self.zip = zipfile.ZipFile(self.filename, mode='w')
        self.zip.writestr("test.txt", "Hello world!")
        self.zip.close()

    def generate(self):
        pass
