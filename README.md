<div align="center">

<font size="8"> <h1> <b> Hase - Discord Bot </b> </h> </font>

<img src="./assets/hase-bot.png" width="200" height="200">

<br>

<a href="https://github.com/danczw/hase_discbot/actions"><img src="https://github.com/danczw/hase_discbot/workflows/Docker/badge.svg"></a>
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
</div>

<br>

**Hase** is a feature-rich Discord bot built using Python programming language. It offers various functionalities to enhance the user experience within a Discord server. From basic user commands to fun interactions, Hase aims to bring joy and utility to your server members. 🐰 The bot leverages the power of generative AI to provide image generation capabilities, making it even more intriguing to chat with.

It also helps server owners to manage their servers by providing notifications when a new user joins or leaves the server. The bot also greets new users with a private message (PM) to make them feel welcome.

<br>

------------

<br>

## Bot commands

The bot offers a range of commands, which are organized into different categories for easy navigation. These categories include GENERAL, FUN, DATA and GEN-AI. *\_abc\_* shows a argument required by the command.

Here are the commands that fall under each category:

### GENERAL commands

The following commands fall under the category of BASIC:

- */info:* Get information about the server, including its name, owner, and member count.
- */help:* Access a comprehensive guide on using all available commands.

### DATA commands
- */weather \_city\_:* Check the weather for a given city using data from the OpenWeatherMap API.
- */crypto \_name\_:* Get the current price of a specified cryptocurrency using data from the CoinGecko API.
- */holidays \_country code\_:* Discover the upcoming holidays in a specific country with data from the date.nager.at API.

### FUN commands
- */hello:* Receive a friendly greeting message from the bot.
- */dice \_n rolls\_:* Roll a six-sided dice a specified number of times and see the results.

### GEN-AI commands
- */chat \_message\_:* Engage in a conversation with the bot on any topic using the OpenAI GPT API. 💬
- */img \_description\_:* Generate an image based on a description using the OpenAI image generation API.

<br>

------------

<br>

## Event handlers

Hase comes with event handlers that react to certain actions within the server:

- *on_ready:* Notifies the bot owner when the bot is ready to use.
- *on_member_join:* Greets new users with a private message and notifies the server owner when someone joins the server.
- *on_member_remove:* Notifies the server owner when a user leaves the server.

<br>

------------

<br>

## Development environment setup

This project uses [uv](https://github.com/astral-sh/uv) for handling dependencies. To set up the development environment:

- create virtual virtual environment using `pyproject.toml` via `uv sync`
- create `.env` file with your personal discord bot token (refer to `.env.example`) and [invite the bot to your server](https://discordpy.readthedocs.io/en/stable/discord.html)
- update further secrets in `.env` file, such as bot owner ID and guild ID (i.e. server ID)
- run `uv run src/main.py`

SQLite is used to store message history for chat. The database and relevant tables are created on start up if not existent and are located in `data/chat.db`. This allows for a persistent chat history and a more natural conversation flow, as the context is retainable for the model. The number of messages used as context while generating a chat response can be configured in `conf/config.yaml`.

Logging is configured to write to `logs/discord.log` for debugging purposes. Dependencies can be found in `pyproject.toml`. For local development, secrets can be set in the `.env` file. Configuration options are available in `conf/config.yaml`.

<br>

------------

<br>

## Deployment:

For deployment via Docker Container, follow these steps:

```bash

    # 1. - build docker image locally
    docker build -t bot:<version> .

    # 2. - run the container in Docker Container
    docker run -d --env-file ./.env bot:<version>

```

Enjoy the features and capabilities of Hase in your Discord server! If you have any questions or need assistance, feel free to reach out to the bot owner.