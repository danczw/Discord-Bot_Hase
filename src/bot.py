# imports
import random

import discord
import openai
import yaml
from discord.ext import commands

from helper import (get_crypto_data, get_dice_results, get_holiday_data,
                    get_server_info, get_weather_info)
from setup import keys_setup, log_setup

# ----------------------------------- SETUP -----------------------------------

# read yaml config
config_params = yaml.safe_load(open("./conf/config.yaml"))
# setup logging
logger = log_setup(config_params=config_params)
# load environment variables depending on local dev or prod env
KEYS, is_docker = keys_setup()

# initiate bot
intents = discord.Intents.all()
client = discord.Client(intents=intents)
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)


# connect bot
@bot.event
async def on_ready():
    logger.info(f"Running in docker: {is_docker}")
    if bot.user:
        logger.info(f"Logged in as {bot.user.name} - {bot.user.id}")


# ------------------------------ COMMANDS - BASIC -----------------------------

# command - show meta data to user
@bot.command(name="info", help="Get meta data about the Server.")
async def info(ctx):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")
    response = get_server_info(ctx)

    logger.info("Sending server info")
    await ctx.send(response)


# ------------------------------- COMMANDS - DATA ------------------------------

# command - get weather data for a location
@bot.command(name="weather", help="Get weather data for a location.")
async def weather(ctx, _location: str):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")
    location = _location.title()
    response = get_weather_info(location=location, KEYS=KEYS, logger=logger, config_params=config_params)

    logger.info(f"Sending weather data for {location}")
    await ctx.send(response)


# command - get crypto data for a coin
@bot.command(name="crypto", help="Get price for a crypto currency, e.g. '$crypto Bitcoin'.")
async def crypto(ctx, _coin: str):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")
    response = get_crypto_data(_coin=_coin, logger=logger, config_params=config_params)

    logger.info(f"Sending crypto data for {_coin}")
    await ctx.send(response)


# command - get public holidays for a country
@bot.command(name="holidays", help="Get public holidays for a country, e.g. '$holidays DE'.")
async def holiday(ctx, _country: str = 'DE'):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")
    response = get_holiday_data(_country=_country, logger=logger)

    logger.info(f"Sending holiday data for {_country}")
    await ctx.send(response)


# ------------------------------- COMMANDS - FUN ------------------------------

# command - greet the user with a random greeting
@bot.command(name="hello", help="Says hello... or maybe not.")
async def hello(ctx):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")
    quote = [
        "Whad up?", "Not you again...", "Nice!", "Was geht?", "How ya doin?",
        "Greetings, fellow traveler!", "I'm not the bot you are looking for. :disguised_face:",
        ":robot:", "Hello there!", "Howdy! :cowboy:", "Hi! :wave:", "Hey! :wave:"
    ]

    response = random.choice(quote)
    await ctx.send(response)


# command - roll a dice up to 10 times
@bot.command(
    name="dice",
    help="Simulates rolling a dice, e.g. '$dice 3'. Max rolls is 10"
)
async def dice(ctx, _rolls: int = 1) -> None:
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")
    response = get_dice_results(_rolls)
    await ctx.send(response)


# ------------------------------- COMMANDS - GPT ------------------------------

# talk to the bot - let the bot write something for you using GPT3
@bot.command(
    name="write",
    help="Let the bot write something for you, e.g. '$write a poem'."
)
async def gpt_text(ctx, *, _message: str):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")

    # use GPT3 to create an answer
    openai.api_key = KEYS["OPENAI_API_KEY"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=_message,
        max_tokens=200,
        n=1,
        temperature=0.8,
        frequency_penalty=1.1
    )

    logger.info("Sending GPT3 text response.")
    await ctx.send(response.choices[0].text)


# code with the bot - let the bot write code for you using GPT3
@bot.command(
    name="code",
    help="Let the bot write code for you, e.g. '$code a function ...'."
)
async def gpt_code(ctx, *, _message):
    logger.info(f"_{ctx.command}_ invoked by _{ctx.author}_ in _{ctx.guild}_")

    # use GPT3 to create an answer
    openai.api_key = KEYS["OPENAI_API_KEY"]
    response = openai.Completion.create(
        engine="code-cushman-001",
        prompt=_message,
        max_tokens=200,
        n=1
        # temperature=0.8,
        # frequency_penalty=1.1
    )

    # TODO: format code response

    logger.info("Sending GPT3 coding response.")
    await ctx.send(":warning: - command still in beta:\n\n" + response.choices[0].text)


# --------------------------- EVENT HANDLING - USER  --------------------------

# new user - greet user and notify owner
@bot.event
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
@bot.event
async def on_command_error(ctx, error):
    # warn the user if they do not have the correct role
    if isinstance(error, commands.errors.CheckFailure):
        logger.info(f"User {ctx.author} does not have the correct role.")
        await ctx.send("You do not have the correct role for this command.")

    # warn the user if they enter an invalid command
    if isinstance(error, commands.errors.CommandNotFound):
        logger.info(f"User {ctx.author} entered an invalid command.")
        await ctx.send("Not a viable comment. Type '$help'")


# ---------------------------------- RUN BOT  ---------------------------------

if __name__ == "__main__":
    # initiate bot
    bot.run(KEYS["DISCORD_TOKEN"])
