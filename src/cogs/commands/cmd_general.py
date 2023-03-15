# command - show meta data to user
import logging

import discord
from discord import app_commands
from discord.ext import commands
from utils.helpers import extract_command_name

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for general commands
    """
    await bot.add_cog(GeneralCommands(bot))
    logger.debug("Commands Loaded: GeneralCommands")


class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Commands cog with general commands for meta data, help, etc.
        """
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name="Show Join Date",
            callback=self.show_join_date
        )
        self.bot.tree.add_command(self.ctx_menu)


    # >>> GENERAL COMMANDS <<< #
    @app_commands.command(name="help", description="Show help.")
    async def help(self, ctx: discord.Interaction) -> None:
        """Show help.

        Args:
            ctx (discord.Interaction): discord context
        """
        _ = extract_command_name(ctx, logger)

        response = (
            "Since introducing slash commands, the help command is no longer needed.\n"
            "You can now use the `/` key to open the command menu and see all available commands."
        )

        await ctx.response.send_message(response, ephemeral=True if ctx.guild else False)


    @app_commands.command(name="info", description="Show server meta data.")
    async def info(self, ctx: discord.Interaction) -> None:
        """Show server meta data.

        Args:
            ctx (discord.Interaction): discord context
        """
        _ = extract_command_name(ctx, logger)

        response = self.helper_get_server_info(ctx)
        logger.info("Sending server info")

        await ctx.response.send_message(response, ephemeral=True if ctx.guild else False)

    def helper_get_server_info(self, ctx: discord.Interaction) -> str:
        """creates a message with server info

        Args:
            ctx (ctx): discord context

        Returns:
            str: message displayed to user with server info
        """
        # check if user is in a server or private message
        if not ctx.guild:
            return ":face_with_monocle: You are not in a server."

        # create message
        _line_break = "- - - -"
        _server_name = f":desktop: Server **{ctx.guild}**"
        _server_owner = f"Created on {ctx.guild.created_at.strftime('%d %b %Y')} by {ctx.guild.owner}:"
        _member_count = f"{ctx.guild.member_count} members"

        n_text_channels = len([channel for channel in ctx.guild.text_channels])
        _text_channels = f"{n_text_channels} text channels"

        n_voice_channels = len([channel for channel in ctx.guild.voice_channels])
        _voice_channels = f"{n_voice_channels} voice channels"

        message = "\n".join([
            _server_name,
            _server_owner,
            _line_break,
            _member_count,
            _text_channels,
            _voice_channels
        ])

        return message


    # >>> GENERAL CONTEXT MENUS <<< #
    async def show_join_date(self, ctx: discord.Interaction, member: discord.Member) -> None:
        """Shows the join date of a member.

        Args:
            ctx (discord.Interaction): discord context
            member (discord.Member): member to show join date of
        """
        _ = extract_command_name(ctx, logger)

        response = f'{member} joined at {discord.utils.format_dt(member.joined_at) if member.joined_at else "unknown"}'
        # The format_dt function formats the date time into a human readable representation in the official client
        await ctx.response.send_message(response, ephemeral=True if ctx.guild else False)