from functools import wraps


def exception_wrapper(func):

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            r = func(*args, **kwargs)
        except IndexError:
            raise ValueError("No JSON object could be decoded")
        return r
    return wrapper


def float_equal(a, b):
    epslion = 0.000001
    return abs(a - b) < epslion
