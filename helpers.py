import json
import sys
from typing import IO

import requests

from config import *


def read_config(
    f: IO[str], dictionary: dict[str, bool]
) -> tuple[str | None, dict[str, bool]]:
    location = None
    new_dict = dictionary.copy()
    try:
        content = f.read()
    except Exception:
        print("file problem")
        sys.exit(1)
    lines = content.split("\n")
    for line in lines:
        if line.startswith("location_1"):
            location = line.split("=", maxsplit=1)[1].strip()
    return (location, new_dict)


def api_call(location: str, date: str) -> dict[str, object]:
    api_url = f"https://www.hebcal.com/zmanim?cfg=json&geonameid={location}&date={date}"
    params = {"cfg": "json"}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data: dict[str, object] = response.json()
        print(data)
        return data
    else:
        raise Exception("Error:", response.status_code, response.text)


def test_json() -> dict[str, object]:
    with open("example.json", "r", encoding="utf-8") as file:
        return json.load(file)


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


def make_default_dict() -> dict[str, bool]:
    default = {
        "chatzotNight": False,
        "alotHaShachar": False,
        "misheyakir": False,
        "misheyakirMachmir": False,
        "dawn": False,
        "sunrise": True,
        "sofZmanShmaMGA19Point8": False,
        "sofZmanShmaMGA16Point1": False,
        "sofZmanShmaMGA": False,
        "sofZmanShma": True,
        "sofZmanTfillaMGA19Point8": False,
        "sofZmanTfillaMGA16Point1": False,
        "sofZmanTfillaMGA": False,
        "sofZmanTfilla": True,
        "chatzot": True,
        "minchaGedola": True,
        "minchaGedolaMGA": False,
        "minchaKetana": True,
        "minchaKetanaMGA": False,
        "plagHaMincha": True,
        "sunset": True,
        "beinHaShmashos": False,
        "dusk": True,
        "tzeit7083deg": False,
        "tzeit85deg": False,
        "tzeit42min": False,
        "tzeit50min": False,
        "tzeit72min": False,
    }
    return default


if __name__ == "__main__":
    print(load_events_json(2025, "4950654"))
