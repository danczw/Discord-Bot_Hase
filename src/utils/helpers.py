import logging
import math

import discord


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


def extract_command_name(ctx: discord.Interaction, logger: logging.Logger):
    """Extracts invoked command name and logs command

    Args:
        ctx (discord.Interaction): discord context
        logger (logging.Logger): log handler object

    Returns:
        str: invoked command name
    """
    command_name = ctx.command.name if ctx.command else "unknwon"
    logger.info(f"_{command_name}_ invoked by _{ctx.user}_ in _{ctx.channel}_ of _{ctx.guild}_")

    if command_name == "Unknown":
        logger.error("Unknown command invoked")

    return command_name