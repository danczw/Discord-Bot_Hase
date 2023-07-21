import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError

import discord
import openai
from database.chat_db import add_message_to_chat_db, get_chat_history
from database.helper_db import open_connection
from discord import app_commands
from discord.ext import commands
from utils.helpers import extract_command_name

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for fun commands"""
    await bot.add_cog(NlpCommands(bot))
    logger.debug("Commands Loaded: NlpCommands")


class NlpCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Commands cog with NLP based commands such as chatting with GPT, etc."""
        self.bot = bot
        self.config_params = bot.config_params  # type: ignore
        self.KEYS = bot.KEYS  # type: ignore

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
        # filter context length
        chat_history = chat_history[-self.config_params["chat_history_ctx_length"] :]
        logger.debug(f"Chat history for {ctx.user}: {len(chat_history)} messages used as context.")
        # create message context
        message_context = [{"role": hist[0], "content": hist[1]} for hist in chat_history]

        # use Open AI'S gpt to create an answer, wrapped in a timeout
        openai.api_key = self.KEYS["OPENAI_API_KEY"]
        response_oai = self.helper_oai_call(
            message_context=message_context,
            model=self.config_params["oai_model"],
            max_tokens=self.config_params["oai_max_tokens"],
            timeout=self.config_params["oai_timeout"],
        )

        # check if timeout
        if response_oai is None:
            return "OpenAI's robots seem to be very tired. :zzz: Please try again later."
        else:
            # extract response content
            response = response_oai.choices[0].message.content  # type: ignore

            # add response to chat db
            add_message_to_chat_db(
                username=str(ctx.user),
                message=response,
                role="assistant",
                connection=chat_conn,
            )

        return response

    def helper_oai_call(
        self,
        message_context: list,
        model: str = "gpt-4",
        max_tokens: int = 800,
        n: int = 1,
        temperature: float = 1,
        frequency_penalty: float = 0,
        timeout: int = 60,
    ):
        """helper function to call openai api with client-side timeout

        Args:
            message_context (list): list of dicts with message context
            model (str, optional): openai model to use. Defaults to "gpt-4".
            max_tokens (int, optional): max tokens to use. Defaults to 800.
            n (int, optional): number of responses to return. Defaults to 1.
            temperature (float, optional): temperature to use. Defaults to 1.
            frequency_penalty (float, optional): frequency penalty to use. Defaults to 0.
            timeout (int, optional): timeout in seconds. Defaults to 60.

        Returns:
            None if timeout, else openai response
        """

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                openai.ChatCompletion.create,
                messages=message_context,
                model=model,
                max_tokens=max_tokens,
                n=n,
                temperature=temperature,
                frequency_penalty=frequency_penalty,
            )

            try:
                response_oai = future.result(timeout=timeout)  # timeout after 5 seconds
                return response_oai
            except TimeoutError:
                logger.error("TimeoutError: OpenAI API call timed out.")
                return None
