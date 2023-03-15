# imports
import random

import discord
import yaml
from command_helper import (
    get_chat_response,
    get_crypto_data,
    get_dice_results,
    get_holiday_data,
    get_server_info,
    get_weather_info,
)
from database.chat_db import create_chat_db
from discord import app_commands
from discord.ext import commands
from helper_setup import keys_setup, log_setup


def main():
    # ----------------------------------- SETUP -----------------------------------

    # read yaml config
    config_params = yaml.safe_load(open("./conf/config.yaml"))
    # setup logging
    logger = log_setup(config_params=config_params)
    # load environment variables depending on local dev or prod env
    KEYS, is_docker = keys_setup()

    # setup database to store chat history for GPT
    create_chat_db(
        db_file_path=config_params["chat_db_path"],
        logger=logger
    )

    # initiate bot
    # MY_GUILD = discord.Object(id=KEYS["SERVER_ID"])
    class MyClient(discord.Client):
        def __init__(self, *, intents: discord.Intents):
            super().__init__(intents=intents)
            # A CommandTree is a special type that holds all the application command
            # state required to make it work. This is a separate class because it
            # allows all the extra state to be opt-in.
            # Whenever you want to work with application commands, your tree is used
            # to store and work with them.
            # Note: When using commands.Bot instead of discord.Client, the bot will
            # maintain its own tree instead.
            self.tree = app_commands.CommandTree(self)

        # Synchronize the app commands to a single guild:
        # Instead of specifying a guild to every command, we copy over our global commands instead.
        # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
        # async def setup_hook(self):
            # This copies the global commands over to your guild.
        #     self.tree.copy_global_to(guild=MY_GUILD)
        #     await self.tree.sync(guild=MY_GUILD)

    intents = discord.Intents.default()
    intents.message_content = True
    client = MyClient(intents=intents)

    @client.event
    async def on_ready():
        logger.debug(f"Running in docker: {is_docker}")
        if client.user:
            logger.info(f"Logged in as {client.user.name} - {client.user.id}")

        # message server owner
        owner = await client.fetch_user(int(KEYS["BOT_OWNER_ID"]))
        await owner.send("Bot is online!")


    # ------------------------------ COMMANDS - BASIC -----------------------------

    # command - show meta data to user
    @client.tree.command(name="info", description="Show server meta data.")
    async def info(ctx: discord.Interaction) -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        response = get_server_info(ctx)

        logger.info("Sending server info")
        await ctx.response.send_message(response)


    @client.tree.context_menu(name='Show Join Date')
    async def show_join_date(interaction: discord.Interaction, member: discord.Member) -> None:
        # The format_dt function formats the date time into a human readable representation in the official client
        await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


    # ------------------------------- COMMANDS - DATA ------------------------------

    # command - get weather data for a location
    @client.tree.command(name="weather", description="Get weather data for a location.")
    @app_commands.describe(location="The location to get weather data for, e.g. 'Berlin'.")
    async def weather(ctx: discord.Interaction, location: str) -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        location = location.title()
        response = get_weather_info(location=location, KEYS=KEYS, logger=logger, config_params=config_params)

        logger.info(f"Sending weather data for {location}")
        await ctx.response.send_message(response)


    # command - get crypto data for a coin
    @client.tree.command(name="crypto", description="Get price for a crypto currency, e.g. '$crypto Bitcoin'.")
    @app_commands.describe(coin="The crypto currency to get price data for, e.g. 'Bitcoin'.")
    async def crypto(ctx: discord.Interaction, coin: str) -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        response = get_crypto_data(_coin=coin, logger=logger, config_params=config_params)

        logger.info(f"Sending crypto data for {coin}")
        await ctx.response.send_message(response)


    # command - get public holidays for a country
    @client.tree.command(name="holidays", description="Get public holidays for a country, e.g. '$holidays DE'.")
    @app_commands.describe(country="The country to get public holidays for, e.g. 'DE'.")
    async def holiday(ctx: discord.Interaction, country: str = "DE") -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        response = get_holiday_data(_country=country, logger=logger)

        logger.info(f"Sending holiday data for {country}")
        await ctx.response.send_message(response)


    # ------------------------------- COMMANDS - FUN ------------------------------

    # command - greet the user with a random greeting
    @client.tree.command(name="hello", description="Says hello... or maybe not.")
    async def hello(ctx: discord.Interaction) -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        quote = [
            "Whad up?", "Not you again...", "Nice!", "Was geht?", "How ya doin?",
            "Greetings, fellow traveler!", "I'm not the bot you are looking for. :disguised_face:",
            ":robot:", "Hello there!", "Howdy! :cowboy:", "Hi! :wave:", "Hey! :wave:"
        ]

        response = random.choice(quote)
        await ctx.response.send_message(response)


    # command - roll a dice up to 10 times
    @client.tree.command(name="dice", description="Simulates rolling a dice, e.g. '$dice 3'. Max rolls is 10")
    @app_commands.describe(rolls="The number of times to roll the dice, e.g. '3'.")
    async def dice(ctx: discord.Interaction, rolls: int = 1) -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        response = get_dice_results(rolls)
        await ctx.response.send_message(response)


    # ------------------------------- COMMANDS - GPT ------------------------------

    # talk to the bot - let the bot write something for you using GPT
    @client.tree.command(name="chat", description="Chat with totally not a robot.")
    @app_commands.describe(message="Your message to the robot, e.g. 'a poem about...'.")
    async def chat(ctx: discord.Interaction, message: str) -> None:
        logger.info(f"_{ctx.command}_ invoked by _{ctx.user}_ in _{ctx.guild}_")
        await ctx.response.defer()

        response = get_chat_response(
            ctx=ctx,
            message=message,
            logger=logger,
            config_params=config_params,
            OPENAI_API_KEY=KEYS["OPENAI_API_KEY"]
        )

        logger.info("Sending GPT text response.")
        await ctx.followup.send(response)

    # --------------------------- EVENT HANDLING - USER  --------------------------

    # new user - greet user and notify owner
    @client.event
    async def on_member_join(member):
        await member.send(
            f"""
            Welcome to **{member.guild.name}**

            Pleased to have you with us, make sure to stay respectful.
            Type '*$help*' in any channel to find available commands.
            """
        )
        await member.guild.owner.send(f"{member} just joined {member.guild.name}.")


    # ------------------------------- ERROR HANDLING ------------------------------

    # bot error handling
    @client.event
    async def on_command_error(ctx: discord.Interaction, error):
        # warn the user if they do not have the correct role
        if isinstance(error, commands.errors.CheckFailure):
            logger.info(f"User {ctx.user} does not have the correct role.")
            await ctx.send("You do not have the correct role for this command.")

        # warn the user if they enter an invalid command
        if isinstance(error, commands.errors.CommandNotFound):
            logger.info(f"User {ctx.user} entered an invalid command.")
            await ctx.send("Not a viable comment. Type '$help'")


    # ------------------------------- RUN BOT ------------------------------------

    client.run(KEYS["DISCORD_TOKEN"])


# ---------------------------------- INIT APPLICATION  ---------------------------

if __name__ == "__main__":
    main()
