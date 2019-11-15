import inspect
try:
    from inspect import getfullargspec as getargspec
except ImportError:
    from inspect import getargspec


def func_source_data(func):
    """
    Return data about a function source, including file name,
    line number, and source code.

    Parameters
    ----------
    func : object
        May be anything support by the inspect module, such as a function,
        method, or class.

    Returns
    -------
    filename : str
    lineno : int
        The line number on which the function starts.
    source : str

    """
    filename = inspect.getsourcefile(func)
    lineno = inspect.getsourcelines(func)[1]
    source = inspect.getsource(func)

    return filename, lineno, source


def get_func_args(func):
    """
    Returns a function's argument names and default values. These are used by other
    functions to establish dependencies and collect inputs.

    Parameters:
    -----------
    func: callable
        The function/callable to inspect.

    Returns:
    --------
    arg_names: list of str
        List of argument names.
    default_kwargs:
        Dictionary of default values. Keyed by the argument name.

    """

    # get function arguments
    spec = getargspec(func)
    args = spec.args
    defaults = spec.defaults

    # get keyword args for the function's default values
    default_kwargs = {}
    if defaults is not None:
        kw_start_idx = len(args) - len(defaults)
        default_kwargs = dict(zip([key for key in args[kw_start_idx:]], list(defaults)))

    return args, default_kwargs


def kwarg_val_is_constant(val):
    """
    Determines if the provided value, presumably defined as a value in a function
    default (**kwargs) argument, should be treated as a static/constant value or if the
    value refers to an injected/managed item (injectable, table, etc.) that will be collected
    from the environment.

    A value is assumed to be constant if:
        - it is NOT a string OR
        - the string has a nested `'` in the name: e.g. "'my string'"

    Parameters:
    ----------
    val: value
        The default value to check.

    Returns:
    --------
    bool

    """
    if isinstance(val, str):
        if not (val[0] == "'" and val[-1] == "'"):
            return False

    return True


def get_arg_map(func, **kwargs):
    """
    Returns a dictionary mapping between the input arguments of the provided
    function and the values and/or injectables that will be used/collected
    to evaluate it.

    Parameters:
    -----------
    func: callable
        The function/callable.
    **kwargs: dictionary of keyword args, optional
        Dictionary of argument overrides. Keys are arg names to override.
        Values indicate the injected item or constant value to use.

    Note in order to differentiate between injected names and str constant
    values, str constants should have a nested `'` and be specified in the
    form "'my_constant'" whereas the name of an injected item would be simply
    "my_injectable" or 'my_injectable'. All non str values are assumed to be
    constants.

    Returns:
    --------
    dict

    Examples:
    --------
    def func1(a, b, c="'something'", d=10):
        pass

        case 1, no overrides, just follow the method signature:

            Call:
            get_arg_map(func1)

            Returns:
            {'a': 'a', 'b': 'b', 'c': "'something'", 'd': 10}

        case 2, override arg names:

            Call:
            get_arg_map(func1, a=1, b='my_injectable')

            Returns:
            {'a': 1, 'b': 'my_injectable', 'c': "'something'", 'd': 10}

        case 3, also override func defaults

            Call:
            get_arg_map(func1, b=100, c="'something else'", d='hola')

            Returns:
            {'a': 'a', 'b': 100, 'c': "'something else'", 'd': 'hola'}

    """
    # get the functions input arguments and any default values
    args, defaults = get_func_args(func)

    # by default follow the function signature
    arg_map = {a: a for a in args}
    for d, v in defaults.items():
        arg_map[d] = v

    # update using the provided kwargs
    for k, v in kwargs.items():
        arg_map[k] = v

    return arg_map
