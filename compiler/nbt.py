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
        # TODO: Make a better error for this, assertions arent very user friendly
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
    def __init__(self, array: typing.List[NBTNode]):
        self.array = array


class NBTIntArray(NBTNode):
    def __init__(self, array: typing.List[NBTNode]):
        self.array = array


class NBTLongArray(NBTNode):
    def __init__(self, array: typing.List[NBTNode]):
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
            # TODO: We need to support quote escaping in the lexer, otherwise raw JSON text wont work
            self.parser.next_token()
            return NBTString(tok.lexeme)
        elif self.parser.current_token.kind == 'ident':
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

        is_array = False
        array_type = None

        if self.parser.is_ident('B') or self.parser.is_ident('I') or self.parser.is_ident('L'):
            array_type = self.parser.current_token.lexeme
            self.parser.next_token()

            if self.parser.current_token.kind != ';':
                self.parse_error("Expected ';', got '{}'".format(self.parser.current_token.lexeme))
            self.parser.next_token()

            is_array = True

        values: typing.List[typing.Tuple[NBTNode, Token]] = []

        first_value = None

        while True:
            if self.parser.current_token.kind == ']':
                self.parser.next_token()
                break
            else:
                tok = self.parser.current_token
                v = self.parse_value()
                values.append((v, tok))

                if first_value is None:
                    first_value = v

                if self.parser.current_token.kind == ']':
                    self.parser.next_token()
                    break

            if self.parser.current_token.kind != ',':
                self.parse_error("Expected ',', got '{}'".format(self.parser.current_token.lexeme))
            self.parser.next_token()

        if is_array:
            T = None
            V = None

            # Would be possible to allow all int values as long as
            # they have a value lower than the type of the array

            if array_type == 'B':
                T = NBTByteArray
                V = NBTByte
            elif array_type == 'I':
                T = NBTIntArray
                V = NBTInt
            elif array_type == 'L':
                T = NBTLongArray
                V = NBTLong
            else:
                raise Exception("Internal compiler error!")

            for (v, tok) in values:
                if not isinstance(v, V):
                    # TODO: Prettyify the type name
                    # TODO: Print what type of array this is 'byte array', 'int array', etc.
                    self.parse_error("Unexpected value in array, '{}'".format(type(v)), tok=tok)

            return T([e[0] for e in values])
        else:
            T = type(first_value)
            for (v, tok) in values:
                if not isinstance(v, T):
                    self.parse_error("Invalid tag for list, a list can only contain a single type of tags", tok=tok)

            return NBTList([e[0] for e in values], type(first_value))

    def parse_compound(self):
        if self.parser.current_token.kind != '{':
            self.parse_error("Expected compund tag, got '{}'".format(self.parser.current_token.lexeme))
        self.parser.next_token()

        tags = []

        # '{,}' -> is invalid
        # While a dangling comma after at least one valid key, value pair is allowed, '{id:"Test",}'

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

        return NBTCompound(tags)
