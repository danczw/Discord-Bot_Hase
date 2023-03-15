import logging
import random

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("discord")


async def setup(bot: commands.Bot) -> None:
    """Setup function for fun commands
    """
    await bot.add_cog(FunCommands(bot))


class FunCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Commands cog with fun commands such as rolling dice, getting greeted, etc.
        """
        self.bot = bot


    @app_commands.command(name="dice", description="Simulates rolling a dice N times.")
    @app_commands.describe(rolls="The number of times to roll the dice, e.g. '3'.")
    async def dice(self, ctx: discord.Interaction, rolls: int = 1) -> None:
        """Simulates rolling a dice, e.g. '/dice 3'. Max rolls is 10

        Args:
            ctx (discord.Interaction): discord context
            rolls (int, optional): number of dice rolls. Defaults to 1.
        """
        logger.info(f"_{ctx.command.name}_ invoked by _{ctx.user}_ in _{ctx.channel}_ of _{ctx.guild}_")
        response = self.helper_get_dice_results(rolls)
        await ctx.response.send_message(response)

    def helper_get_dice_results(self, n_rolls: int = 1) -> str:
        """Rolls a 6 sided dice X times and returns results.

        Args:
            n_rolls (int, optional): number of dice rolls. Defaults to 1.

        Returns:
            str: string of dice results
        """
        if n_rolls > 10:
            return "I only have 10 dice."
        else:
            _dice = [str(random.choice(range(1, 7))) for throw in range(n_rolls)]
            return ", ".join(_dice)


    @app_commands.command(name="hello", description="Says hello... or maybe not.")
    async def hello(self, ctx: discord.Interaction) -> None:
        """Greets the user with a random greeting.

        Args:
            ctx (discord.Interaction): discord context
        """
        logger.info(f"_{ctx.command.name}_ invoked by _{ctx.user}_ in _{ctx.channel}_ of _{ctx.guild}_")
        quote = [
            "Whad up?", "Not you again...", "Nice!", "Was geht?", "How ya doin?",
            "Greetings, fellow traveler!", "I'm not the bot you are looking for. :disguised_face:",
            ":robot:", "Hello there!", "Howdy! :cowboy:", "Hi! :wave:", "Hey! :wave:"
        ]

        response = random.choice(quote)
        await ctx.response.send_message(response)