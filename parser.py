import enum
import re


class TokenType(enum.Enum):
    T_NUM = 0
    T_PLUS = 1
    T_MINUS = 2
    T_MULT = 3
    T_DIV = 4
    T_LPAR = 5
    T_RPAR = 6
    T_END = 7


class Node:
    def __init__(self, token_type, value=None):
        self.token_type = token_type
        self.value = value
        self.children = []


def lexical_analysis(s):
    mappings = {
        '+': TokenType.T_PLUS,
        '-': TokenType.T_MINUS,
        '*': TokenType.T_MULT,
        '/': TokenType.T_DIV,
        '(': TokenType.T_LPAR,
        ')': TokenType.T_RPAR}

    tokens = []
    for c in s:
        if c in mappings:
            token_type = mappings[c]
            token = Node(token_type, value=c)
        elif re.match(r'\d', c):
            token = Node(TokenType.T_NUM, value=int(c))
        else:
            raise Exception('Invalid token: {}'.format(c))
        tokens.append(token)
    tokens.append(Node(TokenType.T_END))
    return tokens


def match(tokens, token):
    if tokens[0].token_type == token:
        return tokens.pop(0)
    else:
        raise_syntax_error(tokens)


def parse_e(tokens, parent_node):
    # TODO: Parent node is the same?
    return parse_ea(tokens, parse_e2(tokens, parent_node), parent_node)


def parse_ea(tokens, left_node, parent_node):
    if tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:
        node = tokens.pop(0)

        if parent_node is None:
            node.children.append(left_node)
            return parse_e(tokens, node)

        if parent_node.token_type in [TokenType.T_PLUS, TokenType.T_MINUS]:

            parent_node.children.append(left_node)
            node.children.append(parent_node)

            return parse_e(tokens, node)

        assert false # Unreachable code, hopefully

    elif tokens[0].token_type in [TokenType.T_END, TokenType.T_RPAR]:

        if parent_node is None:
            return left_node

        parent_node.children.append(left_node)
        return parent_node

    raise_syntax_error(tokens)


def parse_e2(tokens, parent_node):
    return parse_e2a(tokens, parse_e3(tokens), parent_node)


def parse_e2a(tokens, left_node, parent_node):
    if tokens[0].token_type in [TokenType.T_MULT, TokenType.T_DIV]:
        node = tokens.pop(0)

        if parent_node is None:
            node.children.append(left_node)
            return parse_e2(tokens, node)

        if parent_node.token_type in [TokenType.T_MULT, TokenType.T_DIV]:

            parent_node.children.append(left_node)
            node.children.append(parent_node)

            return parse_e2(tokens, node)

        node.children.append(left_node)
        parent_node.children.append(node)

        return parse_e2(tokens, node)

    elif tokens[0].token_type in [TokenType.T_PLUS, TokenType.T_MINUS, TokenType.T_END, TokenType.T_RPAR]:

        if parent_node is None:
            return left_node

        parent_node.children.append(left_node)
        return parent_node

    raise_syntax_error(tokens)


def parse_e3(tokens):
    if tokens[0].token_type == TokenType.T_NUM:
        return tokens.pop(0)
    match(tokens, TokenType.T_LPAR)
    e_node = parse_e(tokens, None)
    match(tokens, TokenType.T_RPAR)
    return e_node


def raise_syntax_error(tokens):
    raise Exception('Invalid syntax on token {}'.format(tokens[0].token_type))


def parse(inputstring):
    tokens = lexical_analysis(inputstring)
    ast = parse_e(tokens, None)
    match(tokens, TokenType.T_END)
    return ast
