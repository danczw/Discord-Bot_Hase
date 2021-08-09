# Discord Bot

Basic discord bot with various features based on Python:
- basic user commands
- fun user commands 
- new user PM greeting and automatic role assignment
- owner notification on new user joining

### Setup:
- create virtual virtual environment using `environment.yml` - `conda env create --name <ENV NAME> --file environment.yml`
- create `.env` file with your personal discord bot token and [invite the bot to your server](https://discordpy.readthedocs.io/en/stable/discord.html) (name it DISCORD_TOKEN)
- run `python bot.py`
- add bot to your Discord server

Dependencies can be found in `environment.yml`

### Production:
View *master* branch for deployment to [Heroku](https://www.heroku.com). Including:
- `Procfile` for initializing bot on Heroku
- `requirements.txt` used for environment in Heroku