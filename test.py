import nose
from utils import float_equal
from json_parser import *


# unit tests

def test_lexer_input_void_json_string():
    i = ''
    r = lexer(i)
    assert r == []


def test_lexer_input_bracket():
    i = '[]'
    r = lexer(i)
    assert '[' in r and ']' in r


def test_lexer_input_brace():
    i = '{}'
    r = lexer(i)
    assert '{' in r and '}' in r


def test_lexer_ignore_whitespace_in_input():
    i = '    '
    r = lexer(i)
    assert r == []


def test_lexer_input_string():
    i = '  "hello"   '
    r = lexer(i)
    assert r == ['hello']


def test_lexer_input_void_string():
    i = '""'
    r = lexer(i)
    assert r == ['']


def test_lexer_input_unquote_string_raise_ValueError():
    i = '"hello'
    try:
        r = lexer(i)
    except Exception as e:
        assert isinstance(e, ValueError)
    else:
        assert False, "no exception raised while except ValueError"


def test_lexer_input_null():
    i = 'null'
    r = lexer(i)
    assert r == [None]


def test_lexer_input_error_null():
    i = 'nul'
    try:
        r = lexer(i)
    except Exception as e:
        assert isinstance(e, ValueError)
    else:
        assert False, "no exception raised while except ValueError"


def test_lexer_input_true():
    i = 'true'
    r = lexer(i)
    assert r == [True]


def test_lexer_input_error_true():
    i = 'tru'
    try:
        r = lexer(i)
    except Exception as e:
        assert isinstance(e, ValueError)
    else:
        assert False, "no exception raised while except ValueError"


def test_lexer_input_false():
    i = 'false'
    r = lexer(i)
    assert r == [False]


def test_lexer_input_error_false():
    i = 'fals'
    try:
        r = lexer(i)
    except Exception as e:
        assert isinstance(e, ValueError)
    else:
        assert False, "no exception raised while except ValueError"


def test_lexer_input_int_number():
    i = '42'
    r = lexer(i)
    assert r == [42]


def test_lexer_input_minus_int_number():
    i = '-42'
    r = lexer(i)
    assert r == [-42]


def test_lexer_input_scientific_enumeration():
    i = '1e4'
    r = lexer(i)
    assert float_equal(1 * 10**4, r[0])


def test_lexer_input_float():
    i = '4.2'
    r = lexer(i)
    assert float_equal(4.2, r[0])


def test_lexer_input_float_scientific_enumeration():
    i = '4.2e5'
    r = lexer(i)
    assert float_equal(4.2 * 10**5, r[0])


def test_lexer_input_error_float():
    i = '1.245.3'
    try:
        r = lexer(i)
    except Exception as e:
        assert isinstance(e, ValueError)
    else:
        assert False, "no exception raised while except ValueError"


# integration test

def test_lexer_multiple_int_element():
    i = '[12, false, true, null, {"world": 42}, "hello"]'
    r = lexer(i)
    print(r)
    assert r == ["[", 12, False, True, None, "{", "world", ":", 42, "}", "hello", "]"]

