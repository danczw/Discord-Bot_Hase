# command - show meta data to user
import logging

import discord
from discord import app_commands
from discord.ext import commands

logger = logging.getLogger("discord")


async def setup(bot: commands.Bot) -> None:
    """Setup function for general commands
    """
    await bot.add_cog(GeneralCommands(bot))


class GeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Commands cog with general commands for meta data, help, etc.
        """
        self.bot = bot

    # TODO: add help command


    @app_commands.command(name="info", description="Show server meta data.")
    async def info(self, ctx: discord.Interaction) -> None:
        """Show server meta data.

        Args:
            ctx (discord.Interaction): discord context
        """
        logger.info(f"_{ctx.command.name}_ invoked by _{ctx.user}_ in _{ctx.channel}_ of _{ctx.guild}_")
        response = self.helper_get_server_info(ctx)

        logger.info("Sending server info")
        await ctx.response.send_message(response)

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