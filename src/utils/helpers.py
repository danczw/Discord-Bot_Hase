import math


def millify(n: float) -> str:
    """Converts large numbers to short, readable string format

    Args:
        n (float): number to convert

    Returns:
        str: converted number
    """    
    millnames = ['',' k',' m',' bn',' tn']
    n = float(n)
    millidx = max(
        0,
        min(
            len(millnames)-1,
            int(math.floor(0 if n == 0 else math.log10(abs(n))/3))
        )
    )

    return '{:.0f}{}'.format(n / 10**(3 * millidx), millnames[millidx])


def up_down_emoji(_value: float) -> str:
    """Returns up or down chart emoji based on value

    Args:
        _value (float): value to check

    Returns:
        str: up or down shart emoji
    """
    if _value > 0:
        return ":chart_with_upwards_trend:"
    elif _value < 0:
        return ":chart_with_downwards_trend:"
    else:
        return ":arrow_right:"