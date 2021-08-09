# Discord Bot

Basic discord bot with various features based on Python:
- basic user commands
- fun user commands 
- new user PM greeting
- owner notification on new user joining

You can also talk to the bot just like a real human, utilizing GPT3 text generation.

<br>

------------

<br>

### Bot commands:

Following commands are available:

- *!info:* displays server info such as name, owner, member count, etc.
- *!hello:* displays a greeting message to the user
- *!dice _rolls:* rolls a six sided dice _rolls times
- *!talk _message:* talk to the bot about anything you want (gpt3 based)
- *!help:* displays help for all available commands

Following event handlers are available:

- *on_member_join:*  informs server owner, greets the new user ~~and automatically assigns a role to a new user~~

<br>

------------

<br>

### Development environment setup:

- create virtual virtual environment using `environment.yml` - `conda env create --name <ENV NAME> --file environment.yml`
- create `.env` file with your personal discord bot token (see `.env.example`) and [invite the bot to your server](https://discordpy.readthedocs.io/en/stable/discord.html)
- run `python bot.py`

Dependencies can be found in `environment.yml`. For local development, secrets can be set in `.env` file. For deployment, secrets should be set in the app settings under config vars.

<br>

------------

<br>

### Productive environment setup:

View *main* branch for deployment to [Heroku](https://www.heroku.com). Including:
- `Procfile` for initializing bot on Heroku
- `runtime.txt` for definition of Heroku runtime
- `requirements.txt` used for environment in Heroku