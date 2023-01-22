# imports
import logging
import os
import random

import discord
import dotenv
import openai
import requests
from discord.ext import commands

from command_helper import create_weather_message

# ----------------------------------- SETUP -----------------------------------

# setup logging
logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)

# load environment variables depending on local dev or prod env
is_docker = os.environ.get("ENV_DOCKER", False)

KEYS = {
    "DISCORD_TOKEN": "",
    "OPENAI_API_KEY": "",
    "OPENWEATHER_API_KEY": "",
    "BINGMAPS_API_KEY": ""
}

if is_docker:
    for key in KEYS:
        KEYS[key] = os.environ.get(key, "").strip("''")
else:
    dotenv.load_dotenv()
    for key in KEYS:
        KEYS[key] = os.getenv(key, "")

for key in KEYS:
    if key == "":
        raise ValueError(f"No token found. Please set {str(key)} in .env file.")

# initiate bot
intents = discord.Intents.all()
client = discord.Client(intents=intents)
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)


# connect bot
@bot.event
async def on_ready():
    logger.info(f"Running in docker: {is_docker}")
    logger.info(f"Logged in as {bot.user.name} - {bot.user.id}")


# ------------------------------ COMMANDS - BASIC -----------------------------

# command - show meta data to user
@bot.command(name="info", help="Get meta data about the Server.")
async def info(ctx):
    _line_break = "- - - -"
    _server_name = f"**Server name:** {ctx.guild}"
    _server_owner = f"**Server owner:** {ctx.guild.owner}:"
    _member_count = f"**Members:** {ctx.guild.member_count}"

    n_text_channels = len([channel for channel in ctx.guild.text_channels])
    _text_channels = f"**Text Channels**: {n_text_channels}"

    n_voice_channels = len([channel for channel in ctx.guild.voice_channels])
    _voice_channels = f"**Voice Channels**: {n_voice_channels}"

    response = "\n".join([
        _server_name, _server_owner,
        _line_break,
        _member_count,
        _text_channels,
        _voice_channels,
    ])

    await ctx.send(response)


# command - show weather data to user
@bot.command(name="weather", help="Get weather data for a location.")
async def weather(ctx, _location):
    _location = _location.title()

    # get geolocation data
    try:
        geo_url = f"https://dev.virtualearth.net/REST/v1/Locations?q=" \
            f"{_location}&key={KEYS['BINGMAPS_API_KEY']}"
        geo_response = requests.get(geo_url)
    except requests.exceptions.RequestException as error:
        print(error)
        await ctx.send("I don't know where that is.")
        return

    geo_json = geo_response.json()
    # pprint(geo_json)

    location = geo_json[
        "resourceSets"][0]["resources"][0]["address"]["formattedAddress"]
    lat = geo_json[
        "resourceSets"][0]["resources"][0]["point"]["coordinates"][0]
    lng = geo_json[
        "resourceSets"][0]["resources"][0]["point"]["coordinates"][1]

    if lat is None or lng is None:
        await ctx.send("I don't know where that is.")
        return

    # get weather data
    try:
        exclude = "minutely,hourly,alerts"
        weather_url = f"https://api.openweathermap.org/data/3.0/onecall?" \
            f"lat={lat}&lon={lng}&exclude={exclude}" \
            f"&appid={KEYS['OPENWEATHER_API_KEY']}&units=metric"
        weather_response = requests.get(weather_url)
    except requests.exceptions.RequestException as error:
        print(error)
        await ctx.send("I don't know where that is.")
        return

    # extract relevant weather data
    weather_json = weather_response.json()
    message = create_weather_message(weather_json, location)

    logger.info(f"Sending weather data for {location}")
    await ctx.send(message)


# ------------------------------- COMMANDS - FUN ------------------------------

# command - greet the user
@bot.command(name="hello", help="Says hello... or maybe not.")
async def hello(ctx):
    quote = [
        "Whad up?",
        "Not you again...",
        "Nice!"
    ]

    response = random.choice(quote)
    await ctx.send(response)


# command - roll a dice
@bot.command(
    name="dice",
    help="Simulates rolling a dice, e.g. '$dice 3'. Max _rolls is 10"
)
async def dice(ctx, _rolls: int = 0):
    if _rolls == 0:
        _rolls = 1
    if _rolls > 10:
        await ctx.send("I only have 10 dice.")
    else:
        _dice = [
            str(random.choice(range(1, 7))) for throw in range(_rolls)
        ]
        await ctx.send(", ".join(_dice))


# talk to the bot
@bot.command(
    name="write",
    help="Let the bot write something for you, e.g. '$write a poem'."
)
async def gpt(ctx, *, _message):

    # use GPT3 to create an answer
    openai.api_key = KEYS["OPENAI_API_KEY"]
    response = openai.Completion.create(engine="text-davinci-002",
                                        prompt=_message,
                                        max_tokens=150,
                                        n=1,
                                        temperature=0.9,
                                        frequency_penalty=1.1)

    logger.info("Sending GPT3 response.")
    await ctx.send(response.choices[0].text)


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

    # TODO: move to .env
    # role = discord.utils.get(member.guild.roles, name = "XXXX")
    # await member.add_roles(role)


# ------------------------------- ERROR HANDLING ------------------------------

# bot error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        logger.info(f"User {ctx.author} does not have the correct role.")
        await ctx.send("You do not have the correct role for this command.")
    if isinstance(error, commands.errors.CommandNotFound):
        logger.info(f"User {ctx.author} entered an invalid command.")
        await ctx.send("Not a viable comment. Type '$help'")


# ---------------------------------- RUN BOT  ---------------------------------

# initiate bot
bot.run(KEYS["DISCORD_TOKEN"])
