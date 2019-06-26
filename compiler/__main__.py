from .parser import Parser, Node
#from .checker import Checker
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
#  - scores
#  - advancements
#  - nbt
# - Parse SNBT, validate?
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
    parser.add_argument('--unzip', action='store_true', help="generates an unzipped directoru for the datapack, useful for debugging")
    args = parser.parse_args()
    return args


def main():
    # args = parse_args()

    parser = Parser(input_str)
    nodes = parser.parse()

    for n in nodes:
        beeprint.pp(n, max_depth=10, indent=4)

#    checker = Checker(nodes)
#    checker.check()

    gen = Generator(nodes, "../datascript/test_dir", True)
    gen.generate()

#    lexer = Lexer(input_str)
#    t = lexer.next_token()
#
#    while t is not None and t.kind != "eof":
#        print(t)
#        t = lexer.next_token()


if __name__ == "__main__":
    main()
