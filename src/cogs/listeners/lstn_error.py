import logging

from discord.ext import commands

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for error listeners
    """
    await bot.add_cog(ErrorListeners(bot))
    logger.debug("Listeners Loaded: ErrorListeners")


class ErrorListeners(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Listener for errors
        """
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        """Listener for command errors

        Args:
            ctx (commands.Context): discord context
            error (Error): command error to handle
        """
        cmd_name = ctx.command.name if ctx.command else "unknwon"
        if cmd_name == "Unknown":
            logger.error("Unknown command invoked")

        # warn the user if they do not have the correct role
        if isinstance(error, commands.errors.CheckFailure):
            logger.info(f"User {ctx.author} does not have the correct role to execute {cmd_name}.")
            await ctx.reply("You do not have the correct role for this command.")

        # warn the user if they enter an invalid command
        if isinstance(error, commands.errors.CommandNotFound):
            logger.info(f"User {ctx.author} entered an invalid command.")
            await ctx.reply("Not a viable comment. Type '/' to see a list of commands.")