# NOTE: currently not loaded in main.py
import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for error listeners
    """
    await bot.add_cog(MsgListeners(bot))
    logger.debug("Listeners Loaded: MsgListeners")


class MsgListeners(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Listener for errors
        """
        self.bot = bot
        logger.debug(f"Listeners: {self.get_listeners()}")

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        logger.debug(f"Message: {msg}")