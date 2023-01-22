# Discord Bot

Basic discord bot with various features based on Python:
- basic user commands
- fun user commands 
- new user PM greeting
- owner notification on new user joining
- talk to the bot just like a real human :speech_balloon: (utilizing GPT3 text generation)

<br>

------------

<br>

### Bot commands:

Following commands are available:

- *$info:* displays server info such as name, owner, member count, etc.
- *$hello:* displays a greeting message to the user
- *$dice _n rolls_:* rolls a six sided dice _rolls times
- *$write _message_:* talk to the bot about anything you want (gpt3 based)
- *$weather _city_:* displays weather for a given city
- *$help:* displays help for all available commands

Following event handlers are available:

- *on_member_join:*  informs server owner, greets the new user ~~and automatically assigns a role to a new user~~

<br>

------------

<br>

### Development environment setup:

- create virtual virtual environment using `pyproject.toml` via `poetry install`
- create `.env` file with your personal discord bot token (see `.env.example`) and [invite the bot to your server](https://discordpy.readthedocs.io/en/stable/discord.html)
- run `poetry run python src/bot.py`

Dependencies can be found in `pyproject.toml`. For local development, secrets can be set in `.env` file.

<br>

------------

<br>

### Deployment:

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