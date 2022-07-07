# imports
import discord
from discord.ext import commands
import dotenv
import os
import random


#################################### SETUP  ####################################

# load environment variables depending on local dev or prod env
is_prod = os.environ.get('IS_HEROKU', False)
if is_prod:
    TOKEN = os.environ.get('DISCORD_TOKEN', None)
else:
    dotenv.load_dotenv()
    TOKEN = os.getenv("DISCORD_TOKEN")

print(f'prod env: {is_prod}')

# initiate bot
client = discord.Client()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)

# connect bot
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


############################### COMMANDS - BASIC ###############################

# command - show meta data to user
@bot.command(name = "info", help = "Get meta data about the Server.")
async def info(ctx):
    _line_break = "- - - -"
    _server_name =       f"**Server name:** {ctx.guild}"
    _server_owner =      f"**Server owner:** {ctx.guild.owner}:"
    _server_region =     f"**Server region:** {str(ctx.guild.region).title()}"
    _member_count =      f"**Members:** {ctx.guild.member_count}"
    _text_channels =     f"**Text Channels**: {len([channel for channel in ctx.guild.text_channels])}"
    _voice_channels =    f"**Voice Channels**: {len([channel for channel in ctx.guild.voice_channels])}"

    response = "\n".join([
        _server_name, _server_owner, _server_region, _line_break, _member_count, _text_channels, _voice_channels,
    ])

    await ctx.send(response)


################################ COMMANDS - FUN ################################

# command - greet the user
@bot.command(name = "hello", help = "Says hello... or maybe not.")
async def hello(ctx):
    quote = [
        "Whad up?",
        "Not you again...",
        "Nice!"
    ]

    response = random.choice(quote)
    await ctx.send(response)

# command - roll a dice
@bot.command(name = "dice", help = "Simulates rolling a dice. Add a number to increase number of dice _rolls. e.g. '!dice 3'. Max _rolls is 10")
async def dice(ctx, _rolls: int=None):
    if not _rolls:
        _rolls = 1
    if _rolls > 10:
        await ctx.send("I only have 10 dice.")
    else:
        _dice = [
            str(random.choice(range(1, 7))) for throw in range(_rolls)
        ]
        await ctx.send(", ".join(_dice))


############################ EVENT HANDLING - USER  ############################

# new user - greet user, assign basic role and notify owner
# @bot.event
# async def on_member_join(member):
#     await member.send(
#         f"""
#         Welcome to **{member.guild.name}**

#         Pleased to have you with us, make sure to stay respectful and read the guidelines in #rules.
#         Type '*!help*' in any channel to find available commands.
#         """
#     )
#     await member.guild.owner.send(f"{member} just joined {member.guild.name}.")

#     role = discord.utils.get(member.guild.roles, name = "XXXX") # TODO: move to .env
#     await member.add_roles(role)


################################ ERROR HANDLING ################################

# bot error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("This is not a viable comment. Type '!help' to see all available commands")


################################### RUN BOT  ###################################

# initiate bot
bot.run(TOKEN)