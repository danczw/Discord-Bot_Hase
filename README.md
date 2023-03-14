# Basic Discord Bot - BDB

This bot is designed to provide a variety of useful features for users in a Discord server, and is built using the Python programming language. The BDB offers a range of capabilities, including basic user commands, fun user commands, a new user private message (PM) greeting, an owner notification when a new user joins the server, and the ability to talk to the bot just like a real human, thanks to the power of the GPT text generation tool.

<br>

------------

<br>

## Bot commands

The BDB features a range of commands, which are organized into different categories based on their functionality. These categories include BASIC, FUN, and GPT3. `_abc_` shows a argument required by the command.

Here are the commands that fall under each category:

### BASIC commands

The following commands fall under the category of BASIC:

- *$info:* This command displays information about the server, including its name, owner, and member count.
- *$help:* This command provides help and guidance on how to use all of the available commands.

### DATA commands
- *$weather \_city\_:* This command displays the weather for a given city, using data provided by the OpenWeatherMap API.
- *$crypto \_name\_:* This command displays the current price of a specified cryptocurrency, using data provided by the CoinGecko API.
- *$holidays \_country code\_:* This command displays the holidays for a given country, using data provided by the date.nager.at API.

### FUN commands
- *$hello:* This command displays a friendly greeting message to the user.
- *$dice \_n rolls\_:* This command rolls a six-sided dice a specified number of times and displays the results.

### GPT3 commands
- *$write \_message\_:* This command allows you to talk to the bot about anything you want, using the OpenAI GPT API. 
- *$code \_message\_:* This command allows you to talk to the bot about code, using the OpenAI GPT3 API. **Please note that this feature is currently in alpha.**

<br>

In addition to these commands, the BDB also includes ~~several~~ event handlers that can be triggered by certain actions in the server. These handlers include:

- *on_member_join:* This event handler notifies the server owner when a new user joins the server and greets the new user with a PM.

<br>

------------

<br>

## Development environment setup:

- create virtual virtual environment using `pyproject.toml` via `poetry install`
- create `.env` file with your personal discord bot token (see `.env.example`) and [invite the bot to your server](https://discordpy.readthedocs.io/en/stable/discord.html)
- update further secrets in `.env` file
- run `poetry run python src/bot.py`

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

    # 2. - login to Azure
    docker login azure

    # 3. (optional) - create Azure Container Registry via Azure Portal or Azure CLI
    az acr create --resource-group <resource-group> --name <registry> --sku Basic

    # 4. - login to Azure Container Registry
    docker login <registry>.azurecr.io

    # 5. - tag docker image
    docker tag bot:<version> <registry>.azurecr.io/bot:<version>

    # 6. - push docker image to Azure Container Registry
    docker push <registry>.azurecr.io/bot:<version> 

    # 7. (optional) - create Azure Container Instance context
    docker context create aci <context-name>

    # 8. - set Azure Container Instance context
    docker context use <context-name>

    # 9. - run the container in Azure Container Instance
    docker run -d --env-file ./.env <registry>.azurecr.io/bot:<version>

```