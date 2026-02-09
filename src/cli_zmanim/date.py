import datetime
import json
import os
from pathlib import Path

import requests

# Path of the cache directory
_CACHE_DIR: Path = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "cli-zmanim"
    / "events"
)


# Prints the events for a given location and date
def print_events(location: str, date: datetime.date) -> None:
    year: str = date.strftime("%Y")
    events: dict = load_events_json(year, location)
    current_date: str = date.strftime("%Y-%m-%d")
    # creates a list of events for the current date
    filtered: list[dict[str, object]] = [
        event for event in events["items"] if current_date in event.values()
    ]

    # prints the events for the current date
    for item in filtered:
        print(f"{item['title']}")


# Creates a json file with the events for a given location and year
def write_events_json(year: str, location: str) -> None:
    # Hit the events api
    api_url: str = f"https://www.hebcal.com/hebcal?v=1&cfg=json&maj=on&min=on&mod=on&nx=on&year={year}&ss=on&mf=on&geo=geoname&geonameid={location}&d=on&o=on&mvch=on"
    params: dict[str, str] = {"cfg": "json"}
    response: requests.Response = requests.get(api_url, params=params)

    if response.status_code == 200:
        # Extract the response data
        events: dict[str, object] = response.json()
        
        # Create a new directory if it doesn't exist
        _CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Construct the file path of the json file
        file_path = _CACHE_DIR / f"{location}_{year}.json"
        
        # Write the json data to the file
        with open(file_path, "w") as f:
            json.dump(events, f, indent=4)
    else:
        raise Exception("Error:", response.status_code, response.text)


# Loads the events json file for a given location and year from cache
def load_events_json(year: str, location: str) -> dict[str, object]:
    # Construct the file path of the json file
    file_path = _CACHE_DIR / f"{location}_{year}.json"
    # Attempt to load the json data, if the file doesn't exist, write it, then read it
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        write_events_json(year, location)
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
