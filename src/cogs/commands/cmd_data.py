import logging
from datetime import datetime, timedelta

import discord
import requests
from dateutil import tz
from discord import app_commands
from discord.ext import commands
from utils.helpers import extract_command_name, millify, up_down_emoji

logger = logging.getLogger(__name__)


async def setup(bot: commands.Bot) -> None:
    """Setup function for general commands"""
    await bot.add_cog(DataCommands(bot))
    logger.debug("Commands Loaded: DataCommands")


class DataCommands(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        """Commands cog with data commands for crypto data, weather, etc."""
        self.bot = bot
        self.config_params = bot.config_params  # type: ignore
        self.KEYS = bot.KEYS  # type: ignore

    # >>> CRYPTO <<< #
    @app_commands.command(name="crypto", description="Get price for a crypto currency.")
    @app_commands.describe(coin="The crypto currency to get price data for, e.g. 'Bitcoin'.")
    async def crypto(self, ctx: discord.Interaction, coin: str) -> None:
        """Get market data for a crypto currency.

        Args:
            ctx (discord.Interaction): discord context
            coin (str): crypto currency name
        """
        _ = extract_command_name(ctx, logger)

        await ctx.response.defer(thinking=True)
        response = self.helper_get_crypto_data(_coin=coin)

        logger.info(f"Sending crypto data for {coin}")
        await ctx.followup.send(response, ephemeral=True if ctx.guild else False)

    def helper_get_crypto_data(self, _coin: str) -> str:
        """Gets crypto data from coingecko API

        Args:
            _coin (str): crypto currency name
            logger (logging.Logger): logger object
            config_params (dict): config parameters

        Returns:
            str: Message with crypto data or error message
        """

        # define variables for API call
        coin_id = _coin.lower()
        message_error = "I can't find your currency, are you sure it is correct?"
        coin_data_url = (
            f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            "/?localization=false&tickers=false&market_data=true&community_data=true&developer_data=false"
        )
        logger.debug(f"crypto request url: {coin_data_url}")

        try:
            # get coin data from coingecko API and parse to json
            coin_data_response = requests.get(coin_data_url).json()
            if "error" in coin_data_response:
                # if coin not found, return error message
                logger.error(f"Error in coin data response: {coin_data_response['error']}")
                return message_error
            logger.info(f"Coin data received for {coin_id}")

            # create message with coin data
            message = self.helper_create_crypto_message(
                coin_id=coin_id,
                coin_data=coin_data_response,
            )
            return message

        except requests.exceptions.RequestException as error:
            logger.error(error)
            return message_error

    def helper_create_crypto_message(self, coin_id: str, coin_data: dict) -> str:
        """Creates message with crypto data

        Args:
            coin_id (str): coin id
            coin_data (dict): coingecko API response data for coin id
            config_params (dict): config parameters

        Returns:
            str: message with crypto data
        """
        cur_perc_round = self.config_params["currency_perc_rounding"]

        # prepare response message
        coin_name = coin_data["name"]
        coin_symbol = coin_data["symbol"]
        coin_price = format(coin_data["market_data"]["current_price"]["eur"], ",.2f")
        coin_ath_date = coin_data["market_data"]["ath_date"]["eur"].split("T")[0]
        coin_ath_price = format(coin_data["market_data"]["ath"]["eur"], ",.2f")
        coin_ath_change_perc = round(coin_data["market_data"]["ath_change_percentage"]["eur"], cur_perc_round)
        coin_curr_market_cap = millify(coin_data["market_data"]["market_cap"]["eur"])
        coin_curr_market_cap_rank = coin_data["market_data"]["market_cap_rank"]
        coin_high_24h = format(coin_data["market_data"]["high_24h"]["eur"], ",.2f")
        coin_low_24h = format(coin_data["market_data"]["low_24h"]["eur"], ",.2f")
        coin_price_change_perc_24h = round(coin_data["market_data"]["price_change_percentage_24h"], cur_perc_round)
        coin_price_change_perc_7d = round(coin_data["market_data"]["price_change_percentage_7d"], cur_perc_round)
        coin_price_change_perc_14d = round(coin_data["market_data"]["price_change_percentage_14d"], cur_perc_round)
        coin_price_change_perc_30d = round(coin_data["market_data"]["price_change_percentage_30d"], cur_perc_round)
        coin_price_change_perc_60d = round(coin_data["market_data"]["price_change_percentage_60d"], cur_perc_round)
        coin_price_change_perc_200d = round(coin_data["market_data"]["price_change_percentage_200d"], cur_perc_round)
        coin_price_change_perc_1y = round(coin_data["market_data"]["price_change_percentage_1y"], cur_perc_round)
        coin_coingecko_url = f"https://www.coingecko.com/en/coins/{coin_id}"

        message = (
            f":coin: **{coin_name} ({coin_symbol}) - {coin_price}**€\n"
            "----------------------------------------\n"
            f"**24h:** {coin_low_24h}€ - {coin_high_24h}€\n"
            f"**Market Cap:** {coin_curr_market_cap}€ (rank {coin_curr_market_cap_rank})\n"
            f"**ATH:** {coin_ath_price}€ on {coin_ath_date} "
            f"({coin_ath_change_perc}% since)\n\n"
            f"**Price Change:**\n"
            f"24h: {up_down_emoji(coin_price_change_perc_24h)} {coin_price_change_perc_24h}%\n"
            f"7d: {up_down_emoji(coin_price_change_perc_7d)} {coin_price_change_perc_7d}%\n"
            f"14d: {up_down_emoji(coin_price_change_perc_14d)} {coin_price_change_perc_14d}%\n"
            f"30d: {up_down_emoji(coin_price_change_perc_30d)} {coin_price_change_perc_30d}%\n"
            f"60d: {up_down_emoji(coin_price_change_perc_60d)} {coin_price_change_perc_60d}%\n"
            f"200d: {up_down_emoji(coin_price_change_perc_200d)} {coin_price_change_perc_200d}%\n"
            f"1y: {up_down_emoji(coin_price_change_perc_1y)} {coin_price_change_perc_1y}%\n\n"
            f"More: {coin_coingecko_url}"
        )

        return message

    # >>> HOLIDAYS <<< #
    @app_commands.command(name="holidays", description="Get public holidays for a country.")
    @app_commands.describe(country="The country code to get public holidays for, e.g. 'DE'.")
    async def holiday(self, ctx: discord.Interaction, country: str = "DE") -> None:
        """Get a list public holidays of the current year for a country.

        Args:
            ctx (discord.Interaction): interaction context
            country (str, optional): country code for holiday data. Defaults to 'DE'.
        """
        _ = extract_command_name(ctx, logger)

        await ctx.response.defer(thinking=True)
        response = self.helper_get_holiday_data(_country=country)

        logger.info(f"Sending holiday data for {country}")
        await ctx.followup.send(response, ephemeral=True if ctx.guild else False)

    def helper_get_holiday_data(self, _country: str = "DE") -> str:
        """Get holiday data for a country and create a response message.

        Args:
            _country (str, optional): country code for holiday data. Defaults to 'DE'.
        Returns:
            str: Message with holiday data or error message
        """
        country_code = _country.upper()

        # get current year
        curr_year = datetime.now().year

        # get holiday data from country code
        holiday_data_url = f"https://date.nager.at/api/v3/publicholidays/{curr_year}/{country_code}"
        try:
            holiday_data_response = requests.get(holiday_data_url)
            logger.info(f"Holiday data received for {country_code}")
            logger.debug(holiday_data_response.json())

            if holiday_data_response.status_code == 404:
                return "I can't find your country, are you sure it is a correct country code?"

            # create response message
            message = f"**Holidays for {country_code}**\n"
            for holiday in holiday_data_response.json():
                # extract counties from response
                if holiday["counties"]:
                    counties = ", ".join([county.split("-")[1] for county in holiday["counties"]])
                    counties = f" ({counties})\n"
                else:
                    counties = "\n"

                row = f"{holiday['date']} - {holiday['name']}" + counties
                message += row

            return message

        except requests.exceptions.RequestException as error:
            logger.error(error)
            return "I can't find your country, are you sure it is a correct country code?"
        except TypeError as error:
            logger.error(error)
            return "There is something wrong here. Ask the mighty developer to check the logs."

    # >>> WEATHER <<< #
    @app_commands.command(name="weather", description="Get weather data for a location.")
    @app_commands.describe(location="The location to get weather data for, e.g. 'Berlin'.")
    async def weather(self, ctx: discord.Interaction, location: str) -> None:
        """Get weather data for a location.

        Args:
            ctx (discord.Interaction): interaction context
            location (str): location name of weather conditions request
        """
        _ = extract_command_name(ctx, logger)

        await ctx.response.defer(thinking=True)
        location = location.title()
        response = self.helper_get_weather_info(location=location)

        logger.info(f"Sending weather data for {location}")
        await ctx.followup.send(response, ephemeral=True if ctx.guild else False)

    def helper_get_weather_info(self, location: str) -> str:
        """Gets weather info for a location and creates a message

        Args:
            location (str): location name of weather conditions request
            KEYS (dict): dictionary of API keys
            config_params (dict): config parameters

        Returns:
            str: message displayed to user with weather conditions for a location
        """
        # get geolocation data
        try:
            geo_url = (
                f"https://dev.virtualearth.net/REST/v1/Locations?q=" f"{location}&key={self.KEYS['BINGMAPS_API_KEY']}"
            )
            geo_response = requests.get(geo_url)
        except requests.exceptions.RequestException as error:
            logger.error(error)
            return "I don't know where that is."

        geo_json = geo_response.json()

        # extract relevant geolocation data
        location, lat, lng = self.helper_extract_geo_data(geo_json=geo_json)

        if lat is None or lng is None:
            return "I don't know where that is."

        # get weather data
        try:
            exclude = "minutely,hourly,alerts"
            weather_url = (
                f"https://api.openweathermap.org/data/3.0/onecall?"
                f"lat={lat}&lon={lng}&exclude={exclude}"
                f"&appid={self.KEYS['OPENWEATHER_API_KEY']}&units=metric"
            )
            weather_response = requests.get(weather_url)
        except requests.exceptions.RequestException as error:
            logger.error(error)
            return "I don't know where that is."

        # extract relevant weather data
        weather_json = weather_response.json()
        message = self.helper_create_weather_message(
            weather_json=weather_json,
            location=location,
        )

        return message

    def helper_extract_geo_data(self, geo_json: dict) -> tuple:
        """extracts relevant geolocation data from json

        Args:
            geo_json (str, json): json of geolocation data for a location

        Returns:
            tuple: location name, latitude, longitude
        """
        location = geo_json["resourceSets"][0]["resources"][0]["address"]["formattedAddress"]
        lat = geo_json["resourceSets"][0]["resources"][0]["point"]["coordinates"][0]
        lng = geo_json["resourceSets"][0]["resources"][0]["point"]["coordinates"][1]

        return location, lat, lng

    def helper_create_weather_message(self, weather_json: dict, location: str) -> str:
        """extracts relevant weather data from json and creates a message

        Args:
            weather_json (str, json): json of weather conditions for a location
            location (str): location name of weather conditions request
            config_params (dict): config parameters

        Returns:
            str: message displayed to user with weather conditions for a location
        """
        decimal_round = self.config_params["temperature_rounding"]

        # current weather
        curr_condition = weather_json["current"]["weather"][0]["description"]
        curr_temp = round(weather_json["current"]["temp"], decimal_round)
        curr_temp_feels_like = round(weather_json["current"]["feels_like"], decimal_round)
        curr_humidity = weather_json["current"]["humidity"]

        # todays weather
        today_condition = weather_json["daily"][0]["weather"][0]["description"]
        today_temp_max = round(weather_json["daily"][0]["temp"]["max"], decimal_round)
        today_temp_min = round(weather_json["daily"][0]["temp"]["min"], decimal_round)
        today_sunrise = self.helper_convert_timezone(
            timestamp=weather_json["daily"][0]["sunrise"], to_zone_name=weather_json["timezone"]
        )
        today_sunset = self.helper_convert_timezone(
            timestamp=weather_json["daily"][0]["sunset"], to_zone_name=weather_json["timezone"]
        )

        # tomorrow weather
        tomorrow_condition = weather_json["daily"][1]["weather"][0]["description"]
        tomorrow_temp_max = round(weather_json["daily"][1]["temp"]["max"], decimal_round)
        tomorrow_temp_min = round(weather_json["daily"][1]["temp"]["min"], decimal_round)
        tomorrow_sunrise = self.helper_convert_timezone(
            timestamp=weather_json["daily"][1]["sunrise"], to_zone_name=weather_json["timezone"]
        )
        tomorrow_sunset = self.helper_convert_timezone(
            timestamp=weather_json["daily"][1]["sunset"], to_zone_name=weather_json["timezone"]
        )

        # condition to icon
        curr_condition_icon = self.helper_condition_to_icon(condition_id=weather_json["current"]["weather"][0]["id"])
        today_condition_icon = self.helper_condition_to_icon(condition_id=weather_json["daily"][0]["weather"][0]["id"])
        tomorrow_condition_icon = self.helper_condition_to_icon(
            condition_id=weather_json["daily"][1]["weather"][0]["id"]
        )

        # create bot response message
        message = (
            f"\n**Weather for {location}**\n"
            f"{curr_condition_icon} Currently {curr_condition} with {curr_temp}°C, \n"
            f"feels like {curr_temp_feels_like}°C and {curr_humidity}% humidity.\n\n"
            f"{today_condition_icon} **Today: {today_condition}**\n"
            f"Low: {today_temp_min}°C -- High: {today_temp_max}°C\n"
            f"Sunrise: {today_sunrise}h -- Sunset: {today_sunset}h\n\n"
            f"{tomorrow_condition_icon} **Tomorrow: {tomorrow_condition}**\n"
            f"Low: {tomorrow_temp_min}°C -- High: {tomorrow_temp_max}°C\n"
            f"Sunrise: {tomorrow_sunrise}h -- Sunset: {tomorrow_sunset}h\n"
        )

        return message

    def helper_condition_to_icon(self, condition_id: int) -> str:
        """converts openweathermap condition id to discord icon

        Args:
            condition_id (int): openweathermap weather condition id

        Returns:
            str: discord icon string
        """
        if condition_id >= 200 and condition_id < 300:
            icon_str = ":thunder_cloud_rain:"
        elif condition_id >= 300 and condition_id < 400:
            icon_str = ":cloud_rain:"
        elif condition_id == 500:
            icon_str = ":white_sun_rain_cloud:"
        elif condition_id >= 501 and condition_id < 600:
            icon_str = ":cloud_rain:"
        elif condition_id >= 600 and condition_id < 700:
            icon_str = ":cloud_snow:"
        elif condition_id >= 700 and condition_id < 800:
            icon_str = ":fog:"
        elif condition_id == 800:
            icon_str = ":sunny:"
        elif condition_id == 801:
            icon_str = ":white_sun_cloud:"
        elif condition_id > 801 and condition_id < 900:
            icon_str = ":cloud:"
        else:
            icon_str = ":question:"

        return icon_str

    def helper_convert_timezone(self, timestamp: int, to_zone_name: str, from_zone_name: str = "UTC") -> str:
        """converts timestamp from one timezone to another

        Args:
            timestamp (int): timestamp to convert
            to_zone_name (str): timezone to convert to
            from_zone_name (str, optional): timezone to convert from. Defaults to "UTC".

        Returns:
            str: converted timestamp in format HH:MM
        """
        from_zone = tz.gettz(from_zone_name)
        to_zone = tz.gettz(to_zone_name)

        utc = datetime.utcfromtimestamp(timestamp)
        utc = utc.replace(tzinfo=from_zone)
        converted = utc.astimezone(to_zone)

        return converted.strftime("%H:%M")
