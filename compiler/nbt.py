from .lexer import Token, Lexer

import typing


class NBTNode:
    pass


class NBTTag(typing.NamedTuple):
    name: str
    value: NBTNode


class NBTCompound(NBTNode):
    def __init__(self, tags: typing.List[NBTTag]):
        self.tags: typing.List[NBTTag] = tags


class NBTByte(NBTNode):
    def __init__(self, value: int):
        assert value >= -128 and value <= 127
        self.value = value


class NBTShort(NBTNode):
    def __init__(self, value: int):
        assert value >= -32768 and value <= 32767
        self.value = value


class NBTInt(NBTNode):
    def __init__(self, value: int):
        assert value >= -2147483648 and value <= 2147483647
        self.value = value


class NBTLong(NBTNode):
    def __init__(self, value: int):
        assert value >= -9223372036854775808 and value <= 9223372036854775807
        self.value = value


class NBTFloat(NBTNode):
    def __init__(self, value: float):
        self.value = value


class NBTDouble(NBTNode):
    def __init__(self, value: float):
        self.value = value


class NBTString(NBTNode):
    def __init__(self, value: str):
        self.value = value


class NBTList(NBTNode):
    def __init__(self, tag_list: typing.List[NBTNode], tag_type: typing.Type):
        self.list = tag_list
        self.type = tag_type


class NBTByteArray(NBTNode):
    def __init__(self, array: typing.List[int]):
        self.array = array


class NBTIntArray(NBTNode):
    def __init__(self, array: typing.List[int]):
        self.array = array


class NBTLongArray(NBTNode):
    def __init__(self, array: typing.List[int]):
        self.array = array


class NBTParseError(Exception):
    def __init__(self, file: str, line: int, column: int, msg: str):
        self.file = file
        self.line = line
        self.column = column
        self.msg = msg


class NBTValidateError(Exception):
    pass


class NBTParser:
    suffix_table = {
        'b': NBTByte, 'B': NBTByte,
        's': NBTShort, 'S': NBTShort,
        'l': NBTLong, 'L': NBTLong,
        'f': NBTFloat, 'F': NBTFloat,
        'd': NBTDouble, 'D': NBTDouble,
    }

    def __init__(self, parser):
        self.parser = parser
        self.lexer: Lexer = parser.lexer

    def parse_error(self, msg, tok: Token = None):
        if tok is None:
            tok = self.parser.current_token
        raise NBTParseError(tok.filepath, tok.line, tok.column, msg)

    def parse_value(self):
        tok = self.parser.current_token

        if self.parser.current_token.kind == 'number':
            self.parser.next_token()

            suffix = NBTParser.suffix_table.get(self.parser.current_token.lexeme, None)
            if suffix is not None:
                self.parser.next_token()
                return suffix(int(tok.lexeme))

            return NBTInt(int(tok.lexeme))
        if self.parser.current_token.kind == 'float':
            self.parser.next_token()

            if self.parser.is_ident('f') or self.parser.is_ident('F'):
                return NBTFloat(float(tok.lexeme))
            else:
                return NBTDouble(float(tok.lexeme))
        elif self.parser.current_token.kind == '{':
            return self.parse_compound()
        elif self.parser.current_token.kind == 'string':
            self.parser.next_token()
            return NBTString(tok.lexeme)
        elif self.parser.current_token.kind == '[':
            return self.parse_list()
        else:
            self.parse_error("Unexpected '{}', expected NBT value".format(self.parser.current_token.lexeme))

    def parse_list(self):
        # Check if Byte, Int or Double Array
        if self.parser.current_token.kind != '[':
            self.parse_error("Expected list, got '{}'".format(self.parser.current_token.lexeme))
        self.parser.next_token()

        values = []

        # if self.parser.is_ident('B')

        raise Exception("incomplete: list")

    def parse_compound(self):
        if self.parser.current_token.kind != '{':
            self.parse_error("Expected compund tag, got '{}'".format(self.parser.current_token.lexeme))
        self.parser.next_token()

        tags = []

        # TODO: Compunds take multiple variables silly, do a while loop

        # '{,}' -> is invalid
        # While a dangling comma after at least one valid key, value pair is allowed, '{id:"Test",}'
        is_dangling_allowed = False

        while True:
            if self.parser.current_token.kind == '}':
                self.parser.next_token()
                break
            elif self.parser.current_token.kind == 'ident':
                name = self.parser.current_token
                if name.kind != 'ident':
                    self.parse_error("Expected tag name, got '{}'".format(self.parser.current_token.lexeme))
                self.parser.next_token()

                if self.parser.current_token.kind != ':':
                    self.parse_error("Expected ':', got '{}'".format(self.parser.current_token.lexeme))
                self.parser.next_token()

                value = self.parse_value()

                tags.append(NBTTag(name.lexeme, value))

                if self.parser.current_token.kind == '}':
                    self.parser.next_token()
                    break
            else:
                self.parse_error("Unexpected '{}'".format(self.parser.current_token.lexeme))

            if self.parser.current_token.kind != ',':
                self.parse_error("Expected ',', got '{}'".format(self.parser.current_token.lexeme))
            self.parser.next_token()

        import beeprint
        beeprint.pp(tags)

        return NBTCompound(tags)
