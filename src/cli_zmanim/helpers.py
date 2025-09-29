from typing import TextIO
import datetime
import yaml

import requests


def read_config(
    default_config: TextIO, user_config: TextIO | None
) -> tuple[dict, str, str, int]:
    defaults = yaml.safe_load(default_config)

    if user_config is not None:
        user_data = yaml.safe_load(user_config)
        merged = merge(user_data, defaults)
    else:
        merged = defaults

    zmanim = merged["Zmanim"]
    location = merged["Settings"]["location"]
    geonames = merged["APIs"]["geonames_key"]
    shabbat_start = merged["Settings"]["shabbat_start"]
    return (zmanim, location, geonames, shabbat_start)


def hebcal_call(location: str, date: str) -> dict:
    api_url = f"https://www.hebcal.com/zmanim?cfg=json&geonameid={location}&date={date}"
    params = {"cfg": "json"}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data: dict[str, object] = response.json()
        return data
    else:
        raise Exception("Error:", response.status_code, response.text)


# def test_json() -> dict[str, object]:
#     with open("example.json", "r", encoding="utf-8") as file:
#         return json.load(file)


def format_text(string: str) -> str:
    output_str = ""
    for index, char in enumerate(string):
        if index == 0:
            output_str += char.upper()
        elif char.isupper():
            output_str += " "
            output_str += char
        else:
            output_str += char
    return output_str


def friday(dictionary: dict, shabbat: int) -> dict:
    sunset = dictionary["sunset"]
    sunset_do = datetime.datetime.strptime(sunset[:-6], "%Y-%m-%dT%H:%M:%S")
    candles_do = sunset_do - datetime.timedelta(minutes=shabbat)
    value = candles_do.strftime("%Y-%m-%dT%H:%M:%S") + "      "
    output = insert_before(dictionary, "sunset", "candleLighting", value)
    return output


def insert_before(dictionary: dict, before_key: str, key: str, value: str) -> dict:
    output = {}
    for k, v in dictionary.items():
        if k == before_key:
            output[key] = value
        output[k] = v
    return output


def merge(user: dict, default: dict) -> dict:
    if isinstance(user, dict) and isinstance(default, dict):
        for k, v in default.items():
            if k not in user:
                user[k] = v
            else:
                user[k] = merge(user[k], v)
    return user
