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
    def f(a, b, c=100, d="'a str const'"):
        pass

    return f


def test_get_func_args(func1, func2):

    args1, defaults1 = utils.get_func_args(func1)
    assert args1 == ['a', 'b']
    assert defaults1 == {}

    args2, defaults2 = utils.get_func_args(func2)
    assert args2 == ['a', 'b', 'c', 'd']
    assert defaults2 == {'c': 100, 'd': "'a str const'"}


def test_get_arg_maps(func1, func2):

    # test 1 - no argument overrides, no defaults
    inj, const = utils.get_arg_maps(func1)
    assert inj == {'a': 'a', 'b': 'b'}
    assert const == {}

    # test 2 - no argument overrides, w/ defaults
    inj, const = utils.get_arg_maps(func2)
    assert inj == {'a': 'a', 'b': 'b'}
    assert const == {'c': 100, 'd': 'a str const'}

    # test 3: override args, no defaults
    inj, const = utils.get_arg_maps(func1, b='hola')
    assert inj == {'a': 'a', 'b': 'hola'}
    assert const == {}

    # test 4: override args and defaults
    inj, const = utils.get_arg_maps(
        func2, a=20, b="'hola'", c='amigo', d="'another const'")
    assert inj == {'c': 'amigo'}
    assert const == {'a': 20, 'b': 'hola', 'd': 'another const'}
