from datetime import datetime


def create_weather_message(weather_json, location: str) -> str:
    """extracts relevant weather data from json and creates a message

    Args:
        weather_json (str, json): json of weather conditions for a location
        location (str): location name of weather conditions request

    Returns:
        str: message displayed to user with weather conditions for a location
    """
    temp_rnd = 1
    # current weather
    curr_condition = weather_json['current']['weather'][0]['description']
    curr_temp = round(weather_json['current']['temp'], temp_rnd)
    curr_temp_feels_like = round(weather_json['current']['feels_like'],
                                 temp_rnd)
    curr_humidity = weather_json['current']['humidity']
    # todays weather
    today_condition = weather_json['daily'][0]['weather'][0]['description']
    today_temp_max = round(weather_json['daily'][0]['temp']['max'], temp_rnd)
    today_temp_min = round(weather_json['daily'][0]['temp']['min'], temp_rnd)
    today_sunrise = datetime.fromtimestamp(weather_json['daily'][0]['sunrise']
                                           ).strftime('%H:%M')
    today_sunset = datetime.fromtimestamp(weather_json['daily'][0]['sunset']
                                          ).strftime('%H:%M')
    # tomorrow weather
    tomorrow_condition = weather_json['daily'][1]['weather'][0]['description']
    tomorrow_temp_max = round(weather_json['daily'][1]['temp']['max'],
                              temp_rnd)
    tomorrow_temp_min = round(weather_json['daily'][1]['temp']['min'],
                              temp_rnd)
    tomorrow_sunrise = datetime.fromtimestamp(weather_json['daily'][1]['sunrise']
                                              ).strftime('%H:%M')
    tomorrow_sunset = datetime.fromtimestamp(weather_json['daily'][1]['sunset']
                                             ).strftime('%H:%M')

    # condition to icon
    curr_condition_icon = condition_to_icon(weather_json['current']['weather'][0]['id'])
    today_condition_icon = condition_to_icon(weather_json['daily'][0]['weather'][0]['id'])
    tomorrow_condition_icon = condition_to_icon(weather_json['daily'][1]['weather'][0]['id'])

    # create bot response message
    message = \
        f"\n**Weather for {location}**\n" \
        f"{curr_condition_icon} Currently {curr_condition} " \
        f"with {curr_temp}°C, " \
        f"feels like {curr_temp_feels_like}°C " \
        f"and {curr_humidity}% humidity.\n\n" \
        f"{today_condition_icon} **Today: {today_condition}**\n" \
        f"High: {today_temp_max}°C - " \
        f"Low: {today_temp_min}°C\n" \
        f"Sunrise: {today_sunrise}h - " \
        f"Sunset: {today_sunset}h\n\n" \
        f"{tomorrow_condition_icon} **Tomorrow: {tomorrow_condition}**\n" \
        f"High: {tomorrow_temp_max}°C - " \
        f"Low: {tomorrow_temp_min}°C\n" \
        f"Sunrise: {tomorrow_sunrise}h - " \
        f"Sunset: {tomorrow_sunset}h\n"

    return message


def condition_to_icon(condition_id: int) -> str:
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
