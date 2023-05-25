import logging

import discord
import openai
from database.chat_db import add_message_to_chat_db, get_chat_history
from database.helper_db import open_connection
from discord import app_commands
from discord.ext import commands
from utils.helpers import extract_command_name

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for fun commands
    """
    await bot.add_cog(NlpCommands(bot))
    logger.debug("Commands Loaded: NlpCommands")


class NlpCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Commands cog with NLP based commands such as chatting with GPT, etc.
        """
        self.bot = bot
        self.config_params = bot.config_params # type: ignore
        self.KEYS = bot.KEYS # type: ignore


    @app_commands.command(name="chat", description="Chat with totally not a robot.")
    @app_commands.describe(message="Your message to the robot, e.g. 'A poem about...'.")
    async def chat(self, ctx: discord.Interaction, message: str) -> None:
        """Chat with totally not a robot.

        Args:
            ctx (discord.Interaction): discord context
            message (str): message to send to robot
        """
        _ = extract_command_name(ctx, logger)

        await ctx.response.defer(thinking=True)

        try:
            response = self.helper_get_chat_response(
                ctx=ctx,
                message=message,
            )
        except Exception as e:
            logger.error(f"Error with OpenAI API: {e}")
            await ctx.followup.send("OpenAI's robots seem to be very tired. :zzz: Please try again later.")
            return

        logger.info("Sending GPT text response.")
        await ctx.followup.send(response)

    def helper_get_chat_response(
            self,
            ctx: discord.Interaction,
            message: str,
        ) -> str:
        """query openai api for chat response

        Args:
            ctx (discord.Interaction): interaction context
            message (str): message to send to openai

        Returns:
            str: chat response
        """
        # open chat db connection
        chat_conn = open_connection(
            db_file_path=self.config_params["chat_db_path"],
        )

        # add message to chat db
        add_message_to_chat_db(
            username=str(ctx.user),
            message=message,
            role="user",
            connection=chat_conn,
        )

        # get chat history for user from db
        chat_history = get_chat_history(
            username=str(ctx.user),
            timeframe=self.config_params["chat_history_timeframe"],
            connection=chat_conn,
        )

        # create message including chat history
        message_context = [{"role": hist[0], "content": hist[1]} for hist in chat_history]
        # use GPT3 to create an answer
        openai.api_key = self.KEYS["OPENAI_API_KEY"]
        response_oai = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=message_context,
            max_tokens=800,
            n=1,
            # temperature=1,
            # frequency_penalty=1.1
            request_timeout=90, # experimental, undocumented parameter
        )
        # extract response content
        response = response_oai.choices[0].message.content # type: ignore

        # add response to chat db
        add_message_to_chat_db(
            username=str(ctx.user),
            message=response,
            role="assistant",
            connection=chat_conn,
        )

        return response