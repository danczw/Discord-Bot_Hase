# imports
import itertools

import discord
import yaml
from bot import MyBot
from database.chat_db import create_chat_db
from utils.setup import keys_setup, log_setup


def main():
    # read yaml config
    config_params = yaml.safe_load(open("./conf/config.yaml"))
    # setup logging
    logger = log_setup(config_params=config_params)
    # load environment variables depending on local dev or prod env
    KEYS, is_docker = keys_setup()
    # setup database to store chat history for GPT
    create_chat_db(db_file_path=config_params["chat_db_path"],)

    # initiate bot
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    # define extensions to be loaded
    cmd_extensions = [
        "cogs.commands.cmd_general", "cogs.commands.cmd_fun", "cogs.commands.cmd_data", "cogs.commands.cmd_nlp"
    ]
    lstn_extensions = ["cogs.listeners.lstn_error", "cogs.listeners.lstn_guild",] # "cogs.listeners.lstn_msg"
    extensions = list(itertools.chain(cmd_extensions, lstn_extensions))

    # initiate bot and load extensions
    bot = MyBot(
        intents=intents,
        KEYS=KEYS,
        is_docker=is_docker,
        initial_extensions=extensions,
        config_params=config_params
    )

    # run bot
    logger.info("Starting bot...")
    bot.run(KEYS["DISCORD_TOKEN"])

if __name__ == "__main__":
    main()
