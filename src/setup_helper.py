import logging
import os

import discord
import dotenv


def log_setup(config_params: dict):
    """Sets up logging for discord bot

    Args:
        config_params (dict): dictionary of config parameters

    Returns:
        logging.logger: log handler object
    """
    log_path = config_params["log_path"]

    # define handler type and formatting
    handler = logging.FileHandler(filename=log_path, encoding='utf-8', mode='w')
    formatter = logging.Formatter('%(asctime)s: %(levelname)s :%(name)s - %(message)s')

    # include discord lib logging and set level
    discord.utils.setup_logging(handler=handler, formatter=formatter, level=logging.DEBUG)
    logger = logging.getLogger("discord")
    logger.setLevel(logging.DEBUG)

    return logger


def keys_setup():
    """Sets up API keys for discord bot

    Raises:
        ValueError: if no API key is found

    Returns:
        dict: dictionary of API keys
        bool: True if running in docker container
    """

    KEYS = {
        "DISCORD_TOKEN": "",
        "OPENAI_API_KEY": "",
        "OPENWEATHER_API_KEY": "",
        "BINGMAPS_API_KEY": "",
        "OWNER_ID": ""
    }

    # check if running in docker container
    is_docker = os.environ.get("ENV_DOCKER", False)

    # load API keys from .env file or docker environment variables
    if is_docker:
        for key in KEYS:
            KEYS[key] = os.environ.get(key, "").strip('""')
    else:
        dotenv.load_dotenv()
        for key in KEYS:
            KEYS[key] = os.getenv(key, "")

    # check if all keys are set
    for key in KEYS:
        if key == "":
            raise ValueError(f"No token found. Please set {str(key)} in .env file.")

    return KEYS, is_docker
