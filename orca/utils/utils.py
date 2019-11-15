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
        Values prefixed with '@' indicate the item to collect,
        values without '@' are treated as static values.

    Returns:
    --------
    dict
        - Keys are the func's input argument names
        - Values:
            - If prefixed with '@' indicate the argument will be collected from
                the orca environment
            - Otherwise the provided value will be used as is
                (sort of like a functools.partial)

    Examples:
    --------
    def func1(a, b, c, d=10):
        pass

        case 1, just follow the method signature and func defaults:

            Call:
            get_arg_map(func1)

            Returns:
            {'a': '@a', 'b': '@b', 'c': '@c', 'd': 10}

        case 2, override arg names:

            Call:
            get_arg_map(func1, a=1, b='@something')

            Returns:
            {'a': 1, 'b': '@something', 'c': '@c', 'd': 10}

        case 3, also override func defaults

            Call:
            get_arg_map(func1, b=100, d='@hola')

            Returns:
            {'a': '@a', 'b': 100, 'c': '@c', 'd': '@hola'}

    """
    # get the functions input arguments and any default values
    args, defaults = get_func_args(func)

    # by default follow the function signature
    arg_map = {a: '@{}'.format(a) for a in args}
    for d, v in defaults.items():
        arg_map[d] = v

    # update using the provided kwargs
    for k, v in kwargs.items():
        arg_map[k] = v

    return arg_map
