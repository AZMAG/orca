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


def get_arg_maps(func, **kwargs):
    """
    Returns mappings between the input arguments of the provided
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
    injected_args: dict
        Dictionary of input arguments that are injected items.
        Keys are the corresponding func arg names. Values are the names
        of injected items that will be collected from the environment.

    constant_args: dict
        Dictionary of input arguments that are constant values.
        Key are the corresponding func arg names. Values are the constants.

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

    # organize into injected items and constants
    inj = {}
    const = {}

    for k, v in arg_map.items():
        if isinstance(v, str):
            if v[0] == "'" and v[-1] == "'":
                # str constant, e.g. "'abcd'"
                const[k] = v[1:-1]
            else:
                # injected item
                inj[k] = v
        else:
            # non str assumed to be constant
            const[k] = v

    return inj, const
