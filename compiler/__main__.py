from .parser import Parser
from .checker import Checker
from .generator import Generator

import beeprint
import argparse

input_str = """\
datapack (
    name = "TestPack",
    namespace = "testpack",
    description = "This is a test datapack",
    path = "path/to/your/world/datapacks",
)

func main @load {
    /tp @e[type=zombie] ~ ~1 ~
}

func tick @tick {
    /function other_datapack:do_thing
    
    as @a[name="Some Name With Spaces", name=NoSpaceName, type=!#minecraft:pig, SomeCounter=20] {
        /tell @s "Hello!"
    }

    as @a[RewardTimer=20.., tag=ActivePlayer, level=10.., distance=..5, x=123.32, y=123., z=.123] {
        /give @s minecraft:diamond
        /xp add @s -10
    }
    
    as @a[tag=Player] at @a[tag=HomeTeleport] {
        /tp @s ~ ~ ~
    }
    
    as @e[nbt={id:"minecraft:armor_stand", NoGravity:1b, CustomName:"Fancy Stand", list:[{id:"minecraft:stick", count:23},{id:"minecraft:dirt", count: 4}]}] {
        /say Hello I am stand
    }
    
    align xz positioned as @a as @p {
        /say I am aligned
    }
    
    as @a[gamemode=creative, gamemode=!survival, limit=3, sort=nearest, team=, team=!, team=testteam, team=!testteam] {
        
    }
    
    as @e[x_rotation=0..90, y_rotation=-45..45] {
        /say I have rotation
    }
    
    facing entity @e[tag=CameraLookAt] feet {
        /tp @s ~ ~ ~
    }
    
    rotated 12 12 rotated as @e anchored eyes in overworld in minecraft:the_nether {
        /help
    }
}
"""

# TODO: List
# * Parse ranges
# - Parse the rest of the selectors
#    FIXME: Start parsing '~' and '^' for certain values. Have it be its own function, like 'parse_coord_value()'
#     Actually is this needed?
#  - scores
#  - advancements
# - Parse SNBT, validate?
#  - Missing quote escaping in lexer
#  - Lists/Arrays
# - Parse the rest of the execute block expression
#   - 'if'
#   - 'unless'

# - Start work on  generating the Datapack
#    Use Zipfile.writestr to write strings of text to the archive
#    If we are generating a datapack unzipped, just call unzip on the archive

# Make datapack.path be optional, defaulting to the current dir, and have it be overridable by command lines

# Semicolon insertion a la Go https://medium.com/golangspec/automatic-semicolon-insertion-in-go-1990338f2649


def parse_args():
    parser = argparse.ArgumentParser(prog='datascript')
    parser.add_argument('SOURCE', type=str, help="Source File")
    parser.add_argument('-w', '--watch', action='store_true', help="watch file for changes and recompile datapack")
    parser.add_argument('--nozip', action='store_true', help="generates an unzipped directoru for the datapack, useful for debugging")
    args = parser.parse_args()
    return args


def watch_test():
    import time
    import pathlib
    from watchdog.events import FileModifiedEvent, PatternMatchingEventHandler
    from watchdog.observers import Observer

    class WatchHandler(PatternMatchingEventHandler):
        def on_modified(self, event: FileModifiedEvent):
            print("'{}' was modified".format(event.src_path))

    filepath = pathlib.Path("./Ticker.ds")
    filedir = filepath.parent

    print("File Name:", filepath.name)
    print("Pattern: {}".format(filepath.absolute().as_posix()))
    print("Dir: {}".format(filedir.absolute().as_posix()))

    handler = WatchHandler(patterns=[filepath.absolute().as_posix()], ignore_directories=True)
    observer = Observer()
    observer.schedule(handler, path=filedir.absolute().as_posix(), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.join()
    observer.join()

    exit(0)


def main():
    # args = parse_args()

    parser = Parser(input_str)
    nodes = parser.parse()

    for n in nodes:
        beeprint.pp(n, max_depth=10, indent=4)

    checker = Checker(nodes)
    checker.check()

    gen = Generator(nodes, "./deep/nested/shit", True)
    gen.generate()


if __name__ == "__main__":
    main()
