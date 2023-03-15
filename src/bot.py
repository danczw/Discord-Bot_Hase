import logging
from datetime import datetime

import discord
from discord.ext import commands

logger = logging.getLogger(__name__)

class MyBot(commands.Bot):
    def __init__(
            self, *,
            intents: discord.Intents,
            initial_extensions: list = [],
            config_params: dict,
            KEYS: dict,
            is_docker: bool
        ):
        """Initiate custom discord bot class 

        Args:
            intents (discord.Intents): discord intents used to subscribe to specific buckets of events
            KEYS (dict): environment variables
            config_params (dict): config parameters
            is_docker (bool): flag to indicate if bot is running in docker
            initial_extensions (list, optional): list of extensions to load. Defaults to [].
        """
        super().__init__(command_prefix="!", intents=intents)
        self.KEYS = KEYS
        self.config_params = config_params
        self.is_docker = is_docker
        self.initial_extensions = initial_extensions

    async def setup_hook(self):
        """Hook to run after bot is ready, including loading extensions and syncing commands to a specified guild.
        """
        # loading extensions prior to sync to ensure we are syncing interactions defined in those extensions.
        logger.debug("Loading extensions...")
        for extension in self.initial_extensions:
            await self.load_extension(extension)
        
        # Synchronize the app commands to a single guild:
        # Instead of specifying a guild to every command, we copy over our global commands instead.
        # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
        guild = discord.Object(self.KEYS["SERVER_ID"])
        # copy in the global commands
        self.tree.copy_global_to(guild=guild)
        # syncing to guild
        # await self.tree.sync(guild=guild)
        # syncing to global
        await self.tree.sync()

    async def on_ready(self):
        """Hook to run after bot is ready, including messaging server owner.
        """
        logger.debug(f"Running in docker: {self.is_docker}")
        if self.user:
            logger.info(f"Logged in as {self.user.name} - {self.user.id}")

        # message server owner
        owner = await self.fetch_user(int(self.KEYS["BOT_OWNER_ID"]))
        await owner.send(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Bot is ready!")
