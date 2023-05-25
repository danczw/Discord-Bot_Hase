import logging

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for error listeners
    """
    await bot.add_cog(GuildListeners(bot))
    logger.debug("Listeners Loaded: GuildListeners")


class GuildListeners(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Listener for guild related events
        """
        self.bot = bot
        logger.debug(f"Listeners: {self.get_listeners()}")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """
        Listener for when a member joins the guild. Greet the user and notify the guild owner.
        
        Args:
            member (discord.Member): member that joined the guild
        """
        await member.send(
            (
                f"Welcome to **{member.guild.name}**  :100:\n\n"
                "Pleased to have you with us, make sure to stay respectful.\n"
                "Type '/help' in any channel to find available commands."
            )
        )
        await member.guild.owner.send(f"{member} just joined {member.guild.name}.") # type: ignore


    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """
        Listener for when a member leaves the guild. Notify the guild owner.

        Args:
            member (discord.Member): member that left the guild
        """
        await member.guild.owner.send(f"{member} just left {member.guild.name}.") # type: ignore