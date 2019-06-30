from dataclasses import dataclass


@dataclass
class Token:
    kind: str
    lexeme: str
    filepath: str
    line: int
    column: int


class Lexer:
    single_token_set = {
        '@', ',', '{', '}', '[', ']', '/', '(', ')', '=', '!', ':', '#', '-', '+', '-'
    }

    def __init__(self, input, path="<string>"):
        self.path = path
        self.input = input
        self.input_offset = -1  # Incremented by next_char to 0
        self.line = 1
        self.column = 0  # Incremented to 1 by next_char on first run
        self.current_char = ''
        self.next_char()
        self.parse_floats = False

    def next_char(self):
        self.input_offset = self.input_offset + 1

        if self.input_offset >= len(self.input) - 1:
            self.current_char = ''
            return

        self.current_char = self.input[self.input_offset]
        self.column = self.column + 1

    # Used to read commands following a '/'
    def read_until_newline(self):
        start = self.input_offset

        while self.current_char != '\n' and self.current_char != '':
            self.next_char()

        result = self.input[start:self.input_offset]

        return result

    def next_token(self, allow_comment=True):
        if self.current_char == '':
            return Token('eof', 'eof', self.path, self.line, self.column)

        if self.current_char == '\n':
            self.line = self.line + 1
            self.column = 0
            self.next_char()
            return self.next_token()

        while self.current_char == '\r' or self.current_char == ' ' or self.current_char == '\t':
            self.next_char()
            if self.current_char == '':
                return Token('eof', 'eof', self.path, self.line, self.column)
            return self.next_token()

        # Check for comments before anything else
        if self.current_char == '#' and allow_comment:
            start_line = self.line
            start_column = self.column

            while self.current_char != '\n':
                if self.current_char == '':
                    break
                self.next_char()

            return self.next_token()

        if self.current_char in Lexer.single_token_set:
            tok = Token(self.current_char, self.current_char, self.path, self.line, self.column)
            self.next_char()
            return tok
        elif self.current_char == '.':
            dot = Token(self.current_char, self.current_char, self.path, self.line, self.column)
            self.next_char()

            if self.current_char != '.':
                return dot

            tok = Token('..', '..', self.path, self.line, self.column)
            self.next_char()

            return tok
        elif self.current_char == '"':
            line = self.line
            column = self.column

            self.next_char()

            start = self.input_offset

            while self.current_char != '"':
                if self.current_char == '':
                    print("{}({}:{}) Unexpected end of file while parsing string".format(self.path, line, column))
                    exit(1)
                self.next_char()

            self.next_char()

            return Token('string', self.input[start:self.input_offset - 1], self.path, line, column)
        elif str.isalpha(self.current_char):
            start = self.input_offset
            line = self.line
            column = self.column

            while str.isalnum(self.current_char) or self.current_char == '_':
                self.next_char()

            return Token('ident', self.input[start:self.input_offset], self.path, line, column)
        elif str.isdigit(self.current_char):
            start = self.input_offset
            line = self.line
            column = self.column

            found_dot = False

            while str.isdigit(self.current_char) or (self.parse_floats and self.current_char == '.'):
                if self.parse_floats and self.current_char == '.':
                    if found_dot:
                        break
                    else:
                        found_dot = True
                        self.next_char()
                self.next_char()

            if found_dot:
                return Token('float', self.input[start:self.input_offset], self.path, line, column)
            else:
                return Token('number', self.input[start:self.input_offset], self.path, line, column)
        elif self.current_char == '':
            return Token('eof', 'eof', self.path, self.line, self.column)
        else:
            print("{}({}:{}) Unexpected character '{}'".format(self.path, self.line, self.column, self.current_char))
            exit(1)

        raise Exception("This should not be reachable")
