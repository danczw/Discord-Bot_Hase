<p align="center"> <font size="5"> <b> Hase - Discord Bot </b> </font> </p>
<p align="center"> <font size="5"> <b> Hase - Discord Bot </b> </font> </p>

<p align="center">
<a href="https://github.com/danczw/discord_assistant_bot/actions"><img src="https://github.com/danczw/discord_assistant_bot/workflows/Docker/badge.svg?branch=main"></a>
</p>

<br>

This bot is designed to provide a variety of useful features for users in a Discord server, and is built using the Python programming language. The Hase Bot offers a range of capabilities, including basic user commands, fun user commands, a new user private message (PM) greeting, an owner notification when a new user joins the server, and the ability to talk to the bot just like a real human, thanks to the power of the GPT text generation tool.

<br>

------------

<br>

## Bot commands

The BDB features a range of commands, which are organized into different categories based on their functionality. These categories include GENERAL, FUN, DATA and GPT. `_abc_` shows a argument required by the command.

Here are the commands that fall under each category:

### GENERAL commands

The following commands fall under the category of BASIC:

- */info:* This command displays information about the server, including its name, owner, and member count.
- */help:* This command provides help and guidance on how to use all of the available commands.

### DATA commands
- */weather \_city\_:* This command displays the weather for a given city, using data provided by the OpenWeatherMap API.
- */crypto \_name\_:* This command displays the current price of a specified cryptocurrency, using data provided by the CoinGecko API.
- */holidays \_country code\_:* This command displays the holidays for a given country, using data provided by the date.nager.at API.

### FUN commands
- */hello:* This command displays a friendly greeting message to the user.
- */dice \_n rolls\_:* This command rolls a six-sided dice a specified number of times and displays the results.

### GPT commands
- */chat \_message\_:* This command allows you to talk to the bot about anything you want, using the OpenAI GPT API. 

<br>

In addition to these commands, the bot also includes event handlers that can be triggered by certain actions in the server. These handlers include:

- *on_ready:* Notifies the bot owner when the bot is ready to use.
- *on_member_join:* This event handler notifies the server owner when a new user joins the server and greets the new user with a PM.
- *on_member_remove:* This event handler notifies the server owner when a user leaves the server.

<br>

------------

<br>

## Development environment setup:

- create virtual virtual environment using `pyproject.toml` via `poetry install`
- create `.env` file with your personal discord bot token (see `.env.example`) and [invite the bot to your server](https://discordpy.readthedocs.io/en/stable/discord.html)
- update further secrets in `.env` file, such as bot owner ID and guild ID (i.e. server ID)
- run `poetry run python src/main.py`

SQLite is used to store message history for GPT. The database and relevant tables are created on start up if not existant and are located in `data/chat.db`. This allows for a persistent chat history and a more natural conversation flow, as the context is retainable for the model.

Logging is configured to write to `logs/discord.log` for debugging purposes. Dependencies can be found in `pyproject.toml`. For local development, secrets can be set in `.env` file. See `conf/config.yaml` for configuration options.

<br>

------------

<br>

## Deployment:

For deployment via Azure Container Instances, following steps are required.

```bash

    # 1. - build docker image locally
    docker build -t bot:<version> .

    # 2. - run the container in Docker Container
    docker run -d --env-file ./.env bot:<version>

```