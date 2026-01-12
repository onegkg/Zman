import datetime
from typing import TextIO

import requests
import yaml


def read_config(
    default_config: TextIO, user_config: TextIO | None
) -> tuple[dict, str, str, int, str]:
    defaults = yaml.safe_load(default_config)

    if user_config is not None:
        user_data = yaml.safe_load(user_config)
        merged = merge(user_data, defaults)
    else:
        merged = defaults

    try:
        zmanim: dict = merged["Zmanim"]
        location: str = merged["Settings"]["location"]
        geonames_key: str = merged["APIs"]["geonames_key"]
        shabbat_start: int = merged["Settings"]["shabbat_start"]
        geonames_id: str = merged["Settings"]["geonames_loc"]
    except TypeError:
        print(
            "Couldn't properly parse your config.yaml, if your config file contains an empty category (eg. APIs), try removing it"
        )
        exit(1)
    return (zmanim, location, geonames_key, shabbat_start, geonames_id)


def hebcal_call(location: str, date: str) -> dict:
    api_url = f"https://www.hebcal.com/zmanim?cfg=json&geonameid={location}&date={date}"
    # print(api_url)
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
    names: dict[str, str] = {
        "chatzotNight": "Chatzot Night",
        "alotHaShachar": "Alot Hashachar",
        "misheyakir": "Misheyakir (Earliest Tallit)",
        "misheyakirMachmir": "Misheyakir (Earliest Tallit; Machmir)",
        "dawn": "Civil Dawn",
        "sunrise": "Sunrise",
        "sofZmanShmaMGA19Point8": "Sof Zman Shma (Magen Avraham 19.8)",
        "sofZmanShmaMGA16Point1": "Sof Zman Shma (Magen Avraham 16.1)",
        "sofZmanShmaMGA": "Sof Zman Shma (Magen Avraham 72min)",
        "sofZmanShma": "Sof Zman Shma (Gra)",
        "sofZmanTfillaMGA19Point8": "Sof Zman Tfilla (Magen Avraham 19.8)",
        "sofZmanTfillaMGA16Point1": "Sof Zman Tfilla (Magen Avraham 16.1)",
        "sofZmanTfillaMGA": "Sof Zman Tfilla (Magen Avraham 72min)",
        "sofZmanTfilla": "Sof Zman Tfilla (Gra)",
        "chatzot": "Chatzot",
        "minchaGedola": "Mincha Gedola (Gra)",
        "minchaGedolaMGA": "Mincha Gedola (Magen Avraham)",
        "minchaKetana": "Mincha Ketana (Gra)",
        "minchaKetanaMGA": "Mincha Ketana (Magen Avraham)",
        "plagHaMincha": "Plag Hamincha",
        "sunset": "Sunset",
        "beinHaShmashos": "Bein Hashmashot",
        "dusk": "Dusk",
        "tzeit7083deg": "Tzeit (7.083 degrees)",
        "tzeit85deg": "Tzeit (8.5 degrees)",
        "tzeit42min": "tzeit (42 min)",
        "tzeit50min": "tzeit (50 min)",
        "tzeit72min": "tzeit (72 min)",
    }

    stripped: str = string.strip()

    if stripped in names:
        return names[stripped]
    else:
        # print("manually processing")
        output_str = ""
        for index, char in enumerate(stripped):
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
