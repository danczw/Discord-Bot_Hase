# imports
import os
import random

import discord
import dotenv
import openai
from discord.ext import commands

# ----------------------------------- SETUP -----------------------------------

# load environment variables depending on local dev or prod env
is_docker = os.environ.get('ENV_DOCKER', False)
if is_docker:
    TOKEN = os.environ.get('DISCORD_TOKEN', None).strip('""')
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', None).strip('""')
else:
    dotenv.load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

print(f'is_docker: {is_docker}')

if TOKEN is None:
    raise ValueError("No token found. Please set DISCORD_TOKEN.")
if OPENAI_API_KEY is None:
    raise ValueError("No token found. Please set OPENAI_API_KEY.")

print('Discord Token: ' + TOKEN)
print('OpenAI API Key: ' + OPENAI_API_KEY)

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
bot.run(TOKEN)
