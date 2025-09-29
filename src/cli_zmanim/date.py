import json
import requests
from pathlib import Path
import os

_CACHE_DIR = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "cli-zmanim"
    / "events"
)


def print_events(location: str, date):
    year = date.strftime("%Y")
    data = load_events_json(year, location)
    val = date.strftime("%Y-%m-%d")
    filtered = [d for d in data["items"] if val in d.values()]
    for item in filtered:
        print(f"{item['title']}")


def write_events_json(year: str, location: str):
    api_url = f"https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&year={year}&ss=on&mf=on&geo=geoname&geonameid={location}&d=on&o=on&mvch=on"
    params = {"cfg": "json"}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data: dict[str, object] = response.json()
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        file_path = _CACHE_DIR / f"{location}_{year}.json"
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
    else:
        raise Exception("Error:", response.status_code, response.text)


def load_events_json(year: str, location: str):
    file_path = _CACHE_DIR / f"{location}_{year}.json"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        write_events_json(year, location)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
