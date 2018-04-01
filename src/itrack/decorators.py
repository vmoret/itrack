"""decorators.py

Provides decorator functions used when working with iTrack.
"""
from functools import wraps

import pandas as pd


def catch(error, default=None):
    """Decorator factory to catch `error`."""

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except error:
                return default
        return wrapper
    return decorator

key_error = catch(KeyError)
type_error = catch(TypeError)
value_error = catch(ValueError)


def to_dataframe(func):
    """Converts the result of `func` to a pandas DataFrame."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        return pd.DataFrame(func(*args, **kwargs))

    return wrapper



def set_index(keys, **kws):
    """
    Set the DataFrame index (row labels) using one or more existing columns.

    Parameters
    ----------
    keys -- unicode or list
        column label or list of column labels / arrays
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            obj = func(*args, **kwargs)
            if isinstance(obj, pd.DataFrame):
                return obj.set_index(keys, **kws)
            return obj

        return wrapper
    return decorator
