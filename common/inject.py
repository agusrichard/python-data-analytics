from functools import wraps
from typing import Callable


def auto_inject(func: Callable) -> Callable:
    """
    Injecting dependencies into the target function using args' type hinting
    """

    @wraps(func)
    def wrapper(*args):
        print("args", args)
        return func(*args)

    return wrapper
