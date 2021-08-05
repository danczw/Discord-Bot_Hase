# imports
import discord
import dotenv
import os
import random

dotenv.load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
SERVER = os.getenv('DISCORD_SERVER')

client = discord.Client()

@client.event
async def on_ready():
    server = discord.utils.get(client.guilds, name = SERVER)
    
    print(f"### {client.user} is connected to Discord! ###")
    print(f"{client.user} is connected to: {server.name} - {server.id}\n")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    quote = [
        "What?",
        "Go Away!"
    ]

    if message.content == "hi":
        response = random.choice(quote)
        await message.channel.send(response)

client.run(TOKEN)