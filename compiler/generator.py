from .parser import *

from typing import List
from sys import stderr

import zipfile
import pathlib
import io


class Generator:
    def __init__(self, nodes: List[Node], in_path, zipped):
        self.nodes = nodes
        self.zipped = zipped

        # Look into using io.BytesIO() for generating the ZipFile in memory
        # And then either write it to file or extract to a dir
        # To write the zipfile, .getvalue() on a BytesIO returns bytes

        self.path = pathlib.Path(in_path)
        if self.path.exists() and not self.path.is_dir():
            stderr.write("Target path '{}' already exists and is not a directory\n".format(path))

        # TODO: Use package name instead of Test
        self.filename = self.path.joinpath("{}.zip".format("Test"))

        self.zip_bytes = io.BytesIO()
        self.zip = zipfile.ZipFile(self.zip_bytes, mode='w')

    def write_archive(self):
        if not self.path.exists():
            try:
                self.path.mkdir(parents=True)
            except (FileNotFoundError, OSError):
                stderr.write("Failed to create output directory '{}', missing permissions?".format(self.path.absolute()))
                exit(1)

        if self.zipped:
            self.zip.close()
            with open(self.filename, 'wb') as f:
                f.write(self.zip_bytes.getvalue())
        else:
            # TODO: extractall
            self.zip.close()

    def generate(self):
        pass
