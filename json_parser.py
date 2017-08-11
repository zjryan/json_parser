# -*- coding: utf-8 -*-
from utils import exception_wrapper, Stack

PARSE_ELEMENTS = ['[', ']', '{', '}', ':']


@exception_wrapper
def parse_true(json_str, i):
    if json_str[i + 1: i + 4] != 'rue':
        raise ValueError
    return i + 3


@exception_wrapper
def parse_false(json_str, i):
    if json_str[i + 1: i + 5] != 'alse':
        raise ValueError
    return i + 4


@exception_wrapper
def parse_null(json_str, i):
    if json_str[i + 1: i + 4] != 'ull':
        raise ValueError
    return i + 3


@exception_wrapper
def parse_string(json_str, i):
    token = ''
    while json_str[i + 1] != '"':
        i += 1
        if i >= len(json_str):
            raise ValueError("Unterminated string")
        token += json_str[i]
    i += 1
    return token, i


@exception_wrapper
def parse_number(json_str, i):
    token = json_str[i]
    while i + 1 < len(json_str) and (json_str[i + 1].isdigit() or json_str[i + 1] == 'e' or json_str[i + 1] == '.'):
        i += 1
        token += json_str[i]
    if token.count('.') > 1:
        raise ValueError

    if 'e' in token:
        n, e = token.split('e')
        r = float(n) * 10 ** int(e)
    elif '.' in token:
        r = float(token)
    else:
        r = int(token)
    return r, i


def lexer(json_str):
    """
    a lexical analyzer take a json string as argument
    return a series of token
    """
    tokens = []
    str_length = len(json_str)
    i = 0
    while i < str_length:
        c = json_str[i]

        if c.isspace() or c == ',':
            pass
        elif c in PARSE_ELEMENTS:
            tokens.append(c)
        elif c == '"':
            token, i = parse_string(json_str, i)
            tokens.append(token)
        elif c == 'n':
            i = parse_null(json_str, i)
            tokens.append(None)
        elif c == 't':
            i = parse_true(json_str, i)
            tokens.append(True)
        elif c == 'f':
            i = parse_false(json_str, i)
            tokens.append(False)
        elif c.isdigit() or c == '-':
            token, i = parse_number(json_str, i)
            tokens.append(token)

        i += 1

    return tokens


def parse_object(tokens):
    s = Stack()
    tokens_count = len(tokens)
    n = 0
    while n < tokens_count:
        elem = tokens[n]
        n += 1
        if elem == ']':
            l = []
            while s.top() != '[':
                top = s.pop()
                l.insert(0, top)
            s.pop()
            s.push(l)
            continue

        if elem == '}':
            l = []
            while s.top() != '{':
                top = s.pop()
                l.insert(0, top)
            s.pop()
            if len(l) > 0 and not len(l) % 3 == 0 and not l.count(':') == len(l) / 3:
                raise ValueError
            d = {l[i]: l[i + 2] for i in range(0, len(l), 3)}
            s.push(d)
            continue

        s.push(elem)

    return s.top()


@exception_wrapper
def json_obj_from_tokens(tokens):
    if len(tokens) == 1:
        elem = tokens[0]
        if elem in PARSE_ELEMENTS:
            raise ValueError
        return elem

    r = parse_object(tokens)

    return r


def loads(json_str):
    tokens = lexer(json_str)
    r = json_obj_from_tokens(tokens)
    return r


def main():
    pass


if __name__ == '__main__':
    main()
