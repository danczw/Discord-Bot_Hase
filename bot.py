# imports
from discord.ext import commands
import dotenv
import os
import random

# load environment variables
dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# initiate bot
bot = commands.Bot(command_prefix = "!")

# connect bot
@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")

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
@bot.command(name = "dice", help = "Simulates rolling a dice. Optionally add number to increase number of dice rolls. e.g. '!dice 3'. Max rolls is 10")
async def dice(ctx, rolls: int=None):
    if  not rolls:
        rolls = 1
    if rolls > 10:
        await ctx.send("I only have 10 dice.")
    else:
        dice = [
            str(random.choice(range(1, 7)))
            for throw in range(rolls)
        ]
        await ctx.send(", ".join(dice))

# bot error handling
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, command.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

# run bot
bot.run(TOKEN)