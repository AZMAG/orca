import pytest
from .. import utils


def test_func_source_data():
    filename, line, source = utils.func_source_data(test_func_source_data)

    assert filename.endswith('test_utils.py')
    assert isinstance(line, int)
    assert 'assert isinstance(line, int)' in source


@pytest.fixture
def func1():
    """
    Returns a simple func.

    """
    def f(a, b):
        pass

    return f


@pytest.fixture
def func2():
    """
    Returns a func with default values

    """
    def f(a, b, c=100):
        pass

    return f


def test_get_func_args(func1, func2):

    args1, defaults1 = utils.get_func_args(func1)
    assert args1 == ['a', 'b']
    assert defaults1 == {}

    args2, defaults2 = utils.get_func_args(func2)
    assert args2 == ['a', 'b', 'c']
    assert defaults2 == {'c': 100}


def test_get_argmap(func1, func2):

    # test 1 - no argument overrides, no defaults
    a = utils.get_arg_map(func1)
    assert a == {'a': '@a', 'b': '@b'}

    # test 2 - no argument overrides, w/ defaults
    a = utils.get_arg_map(func2)
    assert a == {'a': '@a', 'b': '@b', 'c': 100}

    # test 3 - override args, no defaults
    a = utils.get_arg_map(func1, b='@hola')
    assert a == {'a': '@a', 'b': '@hola'}

    # test 4 - override args and defaults
    a = utils.get_arg_map(func2, a=20, b='@hola', c='@amigo')
    assert a == {'a': 20, 'b': '@hola', 'c': '@amigo'}
