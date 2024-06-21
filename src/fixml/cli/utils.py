from typing import Any


def parse_list(raw_input: Any, delim: str = ',') -> tuple:
    """Parse input into list.

    Given any input, this function will try its best to convert it into a list,
    while preventing doing character splitting on a string.

    For example, python-fire will parse input like "1bc,30" as a string, but
    parse inputs such as "10,40" and "abc,bcd" as list.

    This function makes sure that all inputs would be normalized into a tuple
    before further processing.

    Parameters
    ----------
    raw_input : Any
        The input passed on by python-fire.
    delim : str, optional
        Delimiter to split the input into when the input is string.
        Defaults to ','.

    Returns
    -------
    tuple
        The converted input as tuple.
    """
    if raw_input is None:
        return tuple()
    input_type = type(raw_input)
    if input_type in [tuple, list, set]:
        return tuple(raw_input)
    elif input_type in [int, float]:
        return tuple([raw_input])
    elif input_type in [str]:
        # split with delimiter
        return tuple(raw_input.split(delim))
    else:
        raise ValueError(f"The input is expected to be a list, but got type "
                         f"{input_type}.")
