# imports
import os
import random
from datetime import datetime

import discord
import dotenv
import openai
import requests
from discord.ext import commands

# TODO: add logger

# ----------------------------------- SETUP -----------------------------------


# TODO: make dynamic
# load environment variables depending on local dev or prod env
is_docker = os.environ.get('ENV_DOCKER', False)
if is_docker:
    DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN', None).strip('""')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None).strip('""')
    OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY', None
                                         ).strip('""')
    BINGMAPS_API_KEY = os.environ.get('BINGMAPS_API_KEY', None).strip('""')
else:
    dotenv.load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    BINGMAPS_API_KEY = os.getenv('BINGMAPS_API_KEY')

print(f'is_docker: {is_docker}')

for i in [DISCORD_TOKEN, OPENAI_API_KEY,
          OPENWEATHER_API_KEY, BINGMAPS_API_KEY]:
    if i is None:
        raise ValueError(f"No token found. Please set {str(i)} in .env file.")

# initiate bot
intents = discord.Intents.all()

client = discord.Client(intents=intents)

intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)


# connect bot
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

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
        geo_url = f'https://dev.virtualearth.net/REST/v1/Locations?q=' \
            f'{_location}&key={BINGMAPS_API_KEY}'
        geo_response = requests.get(geo_url)
    except requests.exceptions.RequestException as error:
        print(error)
        await ctx.send("I don't know where that is.")
        return

    geo_json = geo_response.json()
    # pprint(geo_json)

    location = geo_json[
        'resourceSets'][0]['resources'][0]['address']['formattedAddress']
    lat = geo_json[
        'resourceSets'][0]['resources'][0]['point']['coordinates'][0]
    lng = geo_json[
        'resourceSets'][0]['resources'][0]['point']['coordinates'][1]

    if lat is None or lng is None:
        await ctx.send("I don't know where that is.")
        return

    # get weather data
    try:
        exclude = 'minutely,hourly,alerts'
        weather_url = f'https://api.openweathermap.org/data/3.0/onecall?' \
            f'lat={lat}&lon={lng}&exclude={exclude}' \
            f'&appid={OPENWEATHER_API_KEY}&units=metric'
        weather_response = requests.get(weather_url)
    except requests.exceptions.RequestException as error:
        print(error)
        await ctx.send("I don't know where that is.")
        return

    # extract relevant weather data
    weather_json = weather_response.json()
    temp_rnd = 1
    # current weather
    curr_condition = weather_json['current']['weather'][0]['description']
    curr_temp = round(weather_json['current']['temp'], temp_rnd)
    curr_temp_feels_like = round(weather_json['current']['feels_like'],
                                 temp_rnd)
    curr_humidity = weather_json['current']['humidity']
    # todays weather
    today_condition = weather_json['daily'][0]['weather'][0]['description']
    today_temp_max = round(weather_json['daily'][0]['temp']['max'], temp_rnd)
    today_temp_min = round(weather_json['daily'][0]['temp']['min'], temp_rnd)
    today_sunrise = datetime.fromtimestamp(weather_json['daily'][0]['sunrise']
                                           ).strftime('%H:%M')
    today_sunset = datetime.fromtimestamp(weather_json['daily'][0]['sunset']
                                          ).strftime('%H:%M')
    # tomorrow weather
    tomorrow_condition = weather_json['daily'][1]['weather'][0]['description']
    tomorrow_temp_max = round(weather_json['daily'][1]['temp']['max'],
                              temp_rnd)
    tomorrow_temp_min = round(weather_json['daily'][1]['temp']['min'],
                              temp_rnd)
    tomorrow_sunrise = datetime.fromtimestamp(weather_json['daily'][1]['sunrise']
                                              ).strftime('%H:%M')
    tomorrow_sunset = datetime.fromtimestamp(weather_json['daily'][1]['sunset']
                                             ).strftime('%H:%M')

    message = \
        f"\n**Weather for {location}**\n" \
        f"Currently {curr_condition} " \
        f"with {curr_temp}°C, " \
        f"feels like {curr_temp_feels_like}°C " \
        f"and {curr_humidity}% humidity.\n\n" \
        f"**Today: {today_condition}**\n" \
        f"High: {today_temp_max}°C - " \
        f"Low: {today_temp_min}°C\n" \
        f"Sunrise: {today_sunrise}h - " \
        f"Sunset: {today_sunset}h\n\n" \
        f"**Tomorrow: {tomorrow_condition}**\n" \
        f"High: {tomorrow_temp_max}°C - " \
        f"Low: {tomorrow_temp_min}°C\n" \
        f"Sunrise: {tomorrow_sunrise}h - " \
        f"Sunset: {tomorrow_sunset}h\n"

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
    help="Let the bot write something for you, e.g. '$write a poem'"
)
async def gpt(ctx, *, _message):

    # use GPT3 to create an answer
    openai.api_key = OPENAI_API_KEY
    response = openai.Completion.create(engine="text-davinci-002",
                                        prompt=_message,
                                        max_tokens=150,
                                        n=1,
                                        temperature=0.9,
                                        frequency_penalty=1.1)

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
        await ctx.send('You do not have the correct role for this command.')
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("Not a viable comment. Type '$help'")


# ---------------------------------- RUN BOT  ---------------------------------

# initiate bot
bot.run(DISCORD_TOKEN)
