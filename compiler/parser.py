from .lexer import Lexer, Token
from sys import stderr


class Node:
    def __init__(self, type):
        self.type = type


class NodeFunc(Node):
    def __init__(self):
        super().__init__(NodeFunc)


class NodeCommand(Node):
    def __init__(self, command):
        super().__init__(NodeCommand)
        self.command = command


class NodeFunction(Node):
    def __init__(self, name, block, tags):
        super().__init__(NodeFunction)
        self.name = name
        self.block = block
        self.tags = tags


class ExecuteChain:
    def __init__(self):
        pass


class ExecuteChainAs(ExecuteChain):
    def __init__(self, target):
        super().__init__()
        self.target = target


class ExectueChainAt(ExecuteChain):
    def __init__(self, target):
        super().__init__()
        self.target = target


class ExecuteChainPositioned(ExecuteChain):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z


class ExecuteChainPositionedAsEntity(ExecuteChain):
    def __init__(self, target):
        super().__init__()
        self.target = target


class ExecuteChainAlign(ExecuteChain):
    def __init__(self, axes):
        super().__init__()
        self.axes = axes


class ExecuteChainFacingPos(ExecuteChain):
    def __init__(self, x, y, z):
        super().__init__()
        self.x = x
        self.y = y
        self.z = z


class ExecuteChainFacingEntity(ExecuteChain):
    def __init__(self, target, anchor):
        super().__init__()
        self.target = target
        self.anchor = anchor


class ExecuteChainRotatedAsEntity(ExecuteChain):
    def __init__(self, target):
        super().__init__()
        self.target = target


class ExecuteChainRotated(ExecuteChain):
    def __init__(self, y, x):
        super().__init__()
        self.y = y
        self.x = x


class ExecuteChainIn(ExecuteChain):
    def __init__(self, dimension):
        super().__init__()
        self.dimension = dimension


class ExecuteChainAnchored(ExecuteChain):
    def __init__(self, anchor):
        super().__init__()
        self.anchor = anchor


class ExecuteIfBlock(ExecuteChain):
    def __init__(self, if_or_unless, pos, block):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.pos = pos
        self.block = block


class ExecuteIfBlocks(ExecuteChain):
    def __init__(self, if_or_unless, pos_begin, pos_end, pos_dest, all_or_masked):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.pos_begin = pos_begin
        self.pos_end = pos_end
        self.pos_dest = pos_dest
        self.all_or_masked = all_or_masked


class ExecuteIfDataEntity(ExecuteChain):
    def __init__(self, if_or_unless, target, nbt_path):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.target = target
        self.nbt_path = nbt_path


class ExecuteIfDataBlock(ExecuteChain):
    def __init__(self, if_or_unless, pos, nbt_path):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.pos = pos
        self.nbt_path = nbt_path


class ExecuteIfEntity(ExecuteChain):
    def __init__(self, if_or_unless, target):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.target = target


class ExecuteIfScore(ExecuteChain):
    def __init__(self, if_or_unless, target, target_obj, source, source_obj, op):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.target = target
        self.target_obj = target_obj
        self.source = source
        self.source_obj = source_obj
        self.op = op


class ExecuteIfScoreMatches(ExecuteChain):
    def __init__(self, if_or_unless, target, objective, range):
        super().__init__()
        self.if_or_unless = if_or_unless
        self.target = target
        self.objective = objective
        self.range = range


class NodeExecuteBlock(Node):
    def __init__(self, chains, block):
        super().__init__(NodeExecuteBlock)
        self.chains = chains
        self.block = block


class NodeFunctionBlock(Node):
    def __init__(self, nodes):
        super().__init__(NodeFunctionBlock)
        self.nodes = nodes


class Selector:
    pass


class SelectorXYZ(Selector):
    def __init__(self, axis: str, value):
        self.axis = axis
        self.value = value


class SelectorDistance(Selector):
    def __init__(self, range):
        self.range = range


class SelectorVolumeXYZ(Selector):
    def __init__(self, axis: str, value):
        self.axis = axis
        self.value = value


class SelectorScores(Selector):
    def __init__(self, score: str, range):
        self.score = score
        self.range = range


class SelectorTeam(Selector):
    def __init__(self, invert, name):
        self.invert = invert
        self.name = name


class SelectorLimit(Selector):
    def __init__(self, limit: int):
        self.limit = limit


class SelectorSort(Selector):
    def __init__(self, sort_op: str):
        self.sort_op = sort_op


class SelectorLevel(Selector):
    def __init__(self, range):
        self.range = range


class SelectorGamemode(Selector):
    def __init__(self, invert, gamemode):
        self.invert = invert
        self.gamemode = gamemode


class SelectorName(Selector):
    def __init__(self, invert, name, ):
        self.invert = invert
        self.name = name


class SelectorType(Selector):
    def __init__(self, invert, is_tag, name, namespace):
        self.invert = invert
        self.name = name
        self.is_tag = is_tag
        self.namespace = namespace


class SelectorRotation(Selector):
    def __init__(self, axis, invert, range):
        self.axis = axis
        self.invert = invert
        self.range = range


class SelectorTag(Selector):
    def __init__(self, invert, name):
        self.invert = invert
        self.name = name


class SelectorNBT(Selector):
    def __init__(self, nbt):
        self.nbt = nbt


class SelectorAdvancement(Selector):
    def __init__(self, advancements):
        self.advancements = advancements


class NodeTargetSelector(Node):
    def __init__(self, target, selectors):
        super().__init__(NodeTargetSelector)
        self.target = target
        self.selectors = selectors


class NodeDatapack(Node):
    def __init__(self, options):
        super().__init__(NodeDatapack)
        self.options = options


class NodeTargetName(Node):
    def __init__(self, name):
        super().__init__(NodeTargetName)
        self.name = name


class NodeIntegerLiteral(Node):
    def __init__(self, value: int):
        super().__init__(NodeIntegerLiteral)
        self.value = value


class NodeDoubleLiteral(Node):
    def __init__(self, value: float):
        super().__init__(NodeDoubleLiteral)
        self.value = value


class NodeRange(Node):
    # start..end, start.., end..
    # The open side is None
    # These starts and ends could be all sort of stuff
    # Fuck non-static checking languages
    # Does shit all with helping refactorability
    # Now I could use type hinting, but im no encouraged to
    # So why fucking would I
    def __init__(self, start, end):
        super().__init__(NodeRange)
        self.start = start
        self.end = end


class Parser:
    execute_block_start_idents_set = {
        'as', 'at', 'if', 'unless',
        'positioned', 'align', 'facing', 'rotated',
        'in', 'anchored'
    }

    valid_java_target_selectors = {
        'x', 'y', 'z',
        'distance',
        'dx', 'dy', 'dz',
        'scores', 'tag', 'team',
        'limit', 'sort',
        'level',
        'gamemode', 'name',
        'x_rotation', 'y_rotation',
        'type', 'nbt', 'advancements',
    }

    xyz_set = {
        'x', 'y', 'z'
    }

    axes_set = {
        'x', 'y', 'z'
    }

    dxyz_set = {
        'dx', 'dy', 'dz'
    }

    valid_gamemodes = {
        'survival', 'creative', 'adventure', 'spectator',
    }

    valid_sort_modes = {
        'nearest', 'furthest', 'random', 'arbitrary'
    }

    valid_facing_anchor = {
        'feet', 'eyes'
    }

    def __init__(self, input_str, path="<string>"):
        self.lexer = Lexer(input_str, path)
        self.current_token = Token(None, None, None, None, None)
        self.next_token()

    def next_token(self, allow_comment=True):
        self.current_token = self.lexer.next_token(allow_comment=allow_comment)

    def is_ident(self, name):
        return self.current_token.kind == 'ident' and self.current_token.lexeme == name

    def syntax_error(self, msg: str, token: Token):
        # TODO: When we do file watch, live rebuild, just have this throw an Exception, easy fix
        stderr.write("{}({}:{}): Syntax Error: {}".format(token.filepath, token.line, token.column, msg))
        exit(1)

    def parse(self):
        nodes = []

        while self.current_token.kind != 'eof':
            if self.is_ident('func'):
                nodes.append(self.parse_func())
            elif self.is_ident('datapack'):
                nodes.append(self.parse_datapack())
            else:
                stderr.write("{}({}:{}): Syntax Error: Unexpected '{}'!".format(self.current_token.filepath, self.current_token.line, self.current_token.column, self.current_token.lexeme))
                exit(1)

        return nodes

    def parse_datapack(self):
        if self.current_token.kind != 'ident' and self.current_token.lexeme == 'datapack':
            raise Exception("Unreachable!")

        self.next_token()

        if self.current_token.kind != '(':
            self.syntax_error("Expected '(' after 'datapack', got {}".format(self.current_token.lexeme), self.current_token)

        self.next_token()

        options = dict()

        while True:
            if self.current_token.kind == ')':
                self.next_token()
                break
            elif self.current_token.kind == 'ident':
                name = self.current_token.lexeme
                self.next_token()

                if self.current_token.kind != '=':
                    self.syntax_error("Expected '=', got '{}'".format(self.current_token.lexeme), self.current_token)
                self.next_token()

                value = self.current_token.lexeme

                if self.current_token.kind != 'string':
                    self.syntax_error("Expected string, got '{}'".format(self.current_token.lexeme), self.current_token)

                self.next_token()

                if self.current_token.kind == ')':
                    self.next_token()
                    break

                options[name] = value
            else:
                self.syntax_error("Expected option or ')' while parsing 'datapack' options, got '{}'".format(self.current_token.lexeme), self.current_token)

            if self.current_token.kind != ',':
                self.syntax_error("Expected ',', got '{}'".format(self.current_token.lexeme), self.current_token)
            self.next_token()

        return NodeDatapack(options)

    def parse_function_block(self):
        # TODO: Store location of the first left brace, useful when generating mcfunctions
        nodes = []

        if self.current_token.kind != '{':
            stderr.write("{}({}:{}): Syntax Error: Expected '{{', got '{}'!".format(self.current_token.filepath, self.current_token.line, self.current_token.column, self.current_token.lexeme))
            exit(1)

        self.next_token()

        while self.current_token.kind != 'eof':
            if self.current_token.kind == '/':
                nodes.append(self.parse_command())
            elif self.current_token.kind == 'ident' and self.current_token.lexeme in Parser.execute_block_start_idents_set:
                nodes.append(self.parse_execute_block())
            elif self.current_token.kind == '{':
                nodes.append(self.parse_function_block())
            elif self.current_token.kind == '}':
                self.next_token()
                break
            else:
                stderr.write("{}({}:{}): Syntax Error: '{}'!".format(self.current_token.filepath, self.current_token.line, self.current_token.column, self.current_token.lexeme))
                exit(1)

        return NodeFunctionBlock(nodes)

    def check_if_and_eat_token(self, kind: str, allow_comment: bool = False):
        if self.current_token.kind == kind:
            self.next_token(allow_comment=allow_comment)
            return True
        else:
            return False

    def parse_double(self):
        unary_op = ''
        if self.current_token.kind == '+':
            unary_op = '+'
            self.next_token()
        elif self.current_token.kind == '-':
            unary_op = '-'
            self.next_token()

        if self.current_token.kind == 'number':
            first = self.current_token
            self.next_token()

            if self.current_token.kind == '.':
                self.next_token()
                if self.current_token.kind == 'number':
                    last = self.current_token
                    self.next_token()

                    return NodeDoubleLiteral(float("{}{}.{}".format(unary_op, first.lexeme, last.lexeme)))
                else:
                    return NodeDoubleLiteral(float("{}{}.".format(unary_op, first.lexeme)))
            else:
                return NodeDoubleLiteral(float(first.lexeme))
        elif self.current_token.kind == '.':
            self.next_token()
            if self.current_token.kind == 'number':
                last = self.current_token
                self.next_token()

                #                            This is fine
                return NodeDoubleLiteral(float("{}0.{}".format(unary_op, last.lexeme)))
            else:
                self.syntax_error("Expected double, got '{}'".format(self.current_token.lexeme), self.current_token)
        else:
            self.syntax_error("Expected double, got '{}'".format(self.current_token.lexeme), self.current_token)

    def parse_number(self):
        unary_op = ''
        if self.current_token.kind == '+':
            unary_op = '+'
            self.next_token()
        elif self.current_token.kind == '-':
            unary_op = '-'
            self.next_token()

        num = self.current_token
        if self.current_token.kind != 'number':
            self.syntax_error("Expected integer, got '{}'".format(self.current_token.lexeme), self.current_token)
        self.next_token()

        return int("{}{}".format(unary_op, num.lexeme))

    def parse_range(self):
        start = None
        end = None
        # TODO: Support unary ops

        if self.current_token.kind == '..':
            self.next_token()

            if self.current_token.kind == 'number':
                end = int(self.current_token.lexeme)
                self.next_token()
            else:
                self.syntax_error("Ranges requires at least a start or an end, got '{}'".format(self.current_token.lexeme), self.current_token)

            return NodeRange(start, end)
        elif self.current_token.kind == 'number' or self.current_token.kind == '+' or self.current_token.kind == '-':
            start = self.parse_number()

            if self.current_token.kind == '..':
                self.next_token()

                if self.current_token.kind == 'number' or self.current_token.kind == '+' or self.current_token.kind == '-':
                    end = self.parse_number()

                    return NodeRange(start, end)
                else:
                    return NodeRange(start, end)

            return NodeIntegerLiteral(start)
        else:
            self.syntax_error("Expected range, got '{}'".format(self.current_token.lexeme), self.current_token)

    def parse_selectors(self, selectors):
        if self.current_token.kind != '[':
            raise Exception("Internal compiler error! parse_selecotrs called when current_token is not '['")
        self.next_token()

        while True:
            if self.current_token.kind == ']':
                self.next_token()
                break
            elif self.current_token.kind == 'ident':
                name_tok = self.current_token
                name = self.current_token.lexeme
                self.next_token()

                if self.current_token.kind != '=':
                    self.syntax_error("Expected '=', got '{}'".format(self.current_token.lexeme), self.current_token)
                self.next_token()

                if name == 'tag':
                    invert = self.check_if_and_eat_token('!')

                    tag_name = ''

                    if self.current_token.kind == 'ident':
                        tag_name = self.current_token.lexeme
                        self.next_token()

                    if self.current_token.kind != ',' and self.current_token.kind != ']':
                        self.syntax_error("Unexpected '{}' while parsing selector 'tag'".format(self.current_token.lexeme), self.current_token)

                    selectors.append(SelectorTag(invert, tag_name))
                elif name == 'type':
                    invert = self.check_if_and_eat_token('!')

                    is_tag = self.check_if_and_eat_token('#', allow_comment=False)

                    name = self.current_token.lexeme
                    if self.current_token.kind != 'ident':
                        self.syntax_error("Unexpected '{}' while parsing selector 'type'".format(self.current_token.lexeme), self.current_token)
                    self.next_token()

                    namespace_name = ''

                    if self.current_token.kind == ':':
                        self.next_token()
                        # TODO: Check that this is indeed an identifier
                        namespace_name = self.current_token.lexeme
                        self.next_token()

                    selectors.append(SelectorType(invert, is_tag, namespace_name, name))
                elif name == 'gamemode':
                    invert = self.check_if_and_eat_token('!')

                    gamemode = self.current_token
                    if self.current_token.kind != 'ident':
                        self.syntax_error("Unexpected '{}', expected gamemode".format(self.current_token.lexeme), self.current_token)
                    self.next_token()

                    if gamemode.lexeme not in Parser.valid_gamemodes:
                        self.syntax_error("'{}' is not a valid gamemode".format(gamemode.lexeme), gamemode)

                    selectors.append(SelectorGamemode(invert, gamemode.lexeme))
                elif name == 'limit':
                    limit = self.current_token
                    if self.current_token.kind != 'number':
                        self.syntax_error("Selector 'limit' requires a numerical argument, got '{}'".format(self.current_token.lexeme), self.current_token)
                    self.next_token()

                    selectors.append(SelectorLimit(int(limit.lexeme)))
                elif name == 'sort':
                    sort_key = self.current_token
                    if self.current_token.kind != 'ident':
                        self.syntax_error("Unexpected '{}' while parsing selector 'sort'".format(self.current_token.lexeme), self.current_token)
                    self.next_token()

                    if sort_key.lexeme not in Parser.valid_sort_modes:
                        self.syntax_error("'{}' is not a valid 'sort' argument".format(sort_key.lexeme), sort_key)

                    selectors.append(SelectorSort(sort_key.lexeme))
                elif name == 'team':
                    invert = self.check_if_and_eat_token('!')

                    team_name = ''

                    if self.current_token.kind == 'ident':
                        team_name = self.current_token.lexeme
                        self.next_token()

                    if self.current_token.kind != ',' and self.current_token.kind != ']':
                        self.syntax_error("Unexpected '{}' while parsing selector 'team'".format(self.current_token.lexeme), self.current_token)

                    selectors.append(SelectorTeam(invert, team_name))
                elif name == 'level':
                    range = self.parse_range()
                    selectors.append(SelectorLevel(range))
                elif name == 'name':
                    invert = self.check_if_and_eat_token('!')

                    if self.current_token.kind != 'ident' and self.current_token.kind != 'string':
                        self.syntax_error("Expected an identifier or string, got '{}'".format(self.current_token.lexeme), self.current_token)
                    name = self.current_token
                    self.next_token()

                    selectors.append(SelectorName(invert, name.lexeme))
                elif name in Parser.xyz_set:
                    value = self.parse_double()

                    selectors.append(SelectorXYZ(name, value))
                elif name == 'distance':
                    range = self.parse_range()

                    selectors.append(SelectorDistance(range))
                elif name in Parser.dxyz_set:
                    value = self.parse_double()

                    selectors.append(SelectorVolumeXYZ(name, value))
                elif name == 'x_rotation':
                    invert = self.check_if_and_eat_token('!')

                    range = self.parse_range()

                    selectors.append(SelectorRotation(name[:1], invert, range))
                elif name == 'y_rotation':
                    invert = self.check_if_and_eat_token('!')

                    range = self.parse_range()

                    selectors.append(SelectorRotation(name[:1], invert, range))
                else:
                    # We assume its supposed to be a score
                    range = self.parse_range()
                    selectors.append(SelectorScores(name, range))

                if self.current_token.kind == ']':
                    self.next_token()
                    break
            else:
                self.syntax_error("Unexpected '{}', expected ']' or selector".format(self.current_token.lexeme), self.current_token)

            if self.current_token.kind != ',':
                self.syntax_error("Expected ',', got '{}'".format(self.current_token.lexeme), self.current_token)
            self.next_token()

    def parse_target(self):
        if self.current_token.kind == 'ident':
            # Player name
            name = self.current_token
            self.next_token()
            return NodeTargetName(name.lexeme)
        elif self.current_token.kind == '@':
            self.next_token()

            select_name = self.current_token.lexeme

            if self.current_token.kind != 'ident':
                self.syntax_error("Expected identifier, got '{}'".format(self.current_token.lexeme), self.current_token)
            self.next_token()

            selectors = []

            if self.current_token.kind == '[':
                self.parse_selectors(selectors)

            return NodeTargetSelector(select_name, selectors)
        else:
            self.syntax_error("Unexpected '{}', expected target".format(self.current_token.lexeme), self.current_token)

    def parse_execute_block(self):
        if self.current_token.lexeme not in Parser.execute_block_start_idents_set:
            raise Exception("Unreachable!")

        chains = []

        while self.current_token.lexeme in Parser.execute_block_start_idents_set:
            if self.current_token.lexeme == 'as':
                self.next_token()

                target = self.parse_target()
                chains.append(ExecuteChainAs(target))
            elif self.current_token.lexeme == "at":
                self.next_token()

                target = self.parse_target()

                chains.append(ExectueChainAt(target))
            elif self.current_token.lexeme == 'positioned':
                self.next_token()

                if self.is_ident('as'):
                    self.next_token()

                    target = self.parse_target()

                    chains.append(ExecuteChainPositionedAsEntity(target))
                else:
                    x = self.parse_double()
                    y = self.parse_double()
                    z = self.parse_double()
                    chains.append(ExecuteChainPositioned(x, y, z))
            elif self.current_token.lexeme == 'align':
                self.next_token()

                if self.current_token.kind != 'ident':
                    self.syntax_error("Expected axes, ex. 'xy' or 'xyz', got '{}'".format(self.current_token.lexeme), self.current_token)

                axes = self.current_token.lexeme

                for c in axes:
                    if c not in Parser.axes_set:
                        self.syntax_error("Unexpected character '{}' in 'align' axes".format(c), self.current_token)

                self.next_token()

                chains.append(ExecuteChainAlign(axes))
            elif self.current_token.lexeme == 'facing':
                self.next_token()

                if self.is_ident('entity'):
                    self.next_token()

                    target = self.parse_target()

                    anchor = self.current_token
                    if self.current_token.kind != 'ident':
                        self.syntax_error("Expected anchor point (eyes or feet), got '{}'".format(self.current_token.lexeme), self.current_token)

                    if anchor.lexeme not in Parser.valid_facing_anchor:
                        self.syntax_error("Expected either 'eyes' or 'feet', got '{}'".format(anchor.lexeme), self.current_token)

                    self.next_token()

                    chains.append(ExecuteChainFacingEntity(target, anchor.lexeme))
                else:
                    x = self.parse_double()
                    y = self.parse_double()
                    z = self.parse_double()

                    chains.append(ExecuteChainFacingPos(x, y, z))
            elif self.current_token.lexeme == 'rotated':
                self.next_token()

                if self.is_ident('as'):
                    self.next_token()

                    target = self.parse_target()

                    chains.append(ExecuteChainRotatedAsEntity(target))
                else:
                    y = self.parse_double()
                    x = self.parse_double()

                    chains.append(ExecuteChainRotated(y, x))
            elif self.current_token.lexeme == 'anchored':
                self.next_token()

                anchor = self.current_token
                if self.current_token.kind != 'ident':
                    self.syntax_error("Expected 'eyes' or 'feet', got '{}'".format(self.current_token.lexeme), self.current_token)
                self.next_token()

                if anchor.lexeme != 'feet' and anchor.lexeme != 'eyes':
                    self.syntax_error("Invalid anchor '{}', expected 'feet' or 'eyes'".format(anchor.lexeme), anchor)

                chains.append(ExecuteChainAnchored(anchor.lexeme))
            elif self.current_token.lexeme == 'in':
                self.next_token()

                namespace = self.current_token
                if self.current_token.kind != 'ident':
                    self.syntax_error("Unexpected '{}'".format(self.current_token.lexeme), self.current_token)
                self.next_token()

                if self.current_token.kind == ':':
                    self.next_token()

                    name = self.current_token
                    if self.current_token.kind != 'ident':
                        self.syntax_error("Expected identifier after namespace '{}', got '{}'".format(namespace.lexeme, name.lexeme), name)
                    self.next_token()

                    chains.append(ExecuteChainIn("{}:{}".format(namespace.lexeme, name.lexeme)))
                else:
                    chains.append(ExecuteChainIn(namespace.lexeme))
            else:
                raise Exception("Internal compiler error! Unhandled execute chain command '{}'!".format(self.current_token.lexeme))

        if self.current_token.kind != '{':
            self.syntax_error("Unexpected '{}', expected '{{'".format(self.current_token.lexeme), self.current_token)

        block = self.parse_function_block()

        return NodeExecuteBlock(chains, block)

    def parse_func(self):
        if self.current_token.kind != 'ident' and self.current_token.lexeme == 'func':
            raise Exception("Unreachable!")

        self.next_token()

        name = self.current_token
        if self.current_token.kind != 'ident':
            self.syntax_error("Expected identifier after 'func', got '{}'".format(name.lexeme), name)
        self.next_token()

        tags = []

        while self.current_token.kind == '@':
            self.next_token()

            tag = self.current_token

            if tag.kind != 'ident':
                self.syntax_error("Expected identifier after '@' while parsing func '{}', got '{}'".format(name.lexeme, tag.lexeme), tag)
            self.next_token()

            tags.append(tag.lexeme)

        block = self.parse_function_block()

        return NodeFunction(name, block, tags)

    def parse_command(self):
        cmd = self.lexer.read_until_newline()
        self.next_token()
        return NodeCommand(cmd)
