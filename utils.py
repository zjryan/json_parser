from functools import wraps


def exception_wrapper(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
        except IndexError as e:
            raise ValueError("No JSON object could be decoded") from e
        except Exception as e:
            msg = e.args[0] if len(e.args) > 0 else ''
            if not msg:
                e.args = ("No JSON object could be decoded", )
            raise
        return r
    return wrapper


def float_equal(a, b):
    epslion = 0.000001
    return abs(a - b) < epslion


class Stack(object):
    def __init__(self):
        self._list = []

    def push(self, x):
        self._list.append(x)

    def pop(self):
        return self._list.pop()

    def top(self):
        return self._list[-1]

    def is_empty(self,):
        return len(self._list) == 0