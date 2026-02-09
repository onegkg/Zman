"""
Event handling and caching for Jewish calendar events.

This module provides functionality to fetch, cache, and display Jewish calendar
events (holidays, fasts, candle lighting times, etc.) from the Hebcal API. Events
are cached locally per year and location to minimize API calls.
"""

import datetime
import json
import os
from pathlib import Path

import requests

# Cache directory path following XDG Base Directory specification
_EVENTS_CACHE_DIR: Path = (
    Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    / "cli-zmanim"
    / "events"
)


def print_events(geoname_id: str, date: datetime.date) -> None:
    """
    Print all Jewish calendar events for a specific location and date.

    This function loads the cached events data for the given year and location,
    filters events matching the specified date, and prints them to stdout.

    Args:
        geoname_id: The Geonames location identifier
        date: The date to display events for

    Note:
        Events are automatically cached locally. If cache doesn't exist for the
        given year and location, it will be fetched from the Hebcal API first.
    """
    year_string: str = date.strftime("%Y")
    events_data: dict[str, object] = load_events_from_cache(year_string, geoname_id)
    current_date_string: str = date.strftime("%Y-%m-%d")

    # Filter events that match the current date
    # events_data["items"] is a list of event dictionaries
    events_list: list = events_data["items"]  # type: ignore
    matching_events: list[dict[str, object]] = [
        event for event in events_list if current_date_string in event.values()
    ]

    # Print each matching event's title
    for event in matching_events:
        print(f"{event['title']}")


def fetch_and_cache_events(year_string: str, geoname_id: str) -> None:
    """
    Fetch Jewish calendar events from Hebcal API and cache them locally.

    Makes a request to the Hebcal events API for all event types (major holidays,
    minor holidays, modern holidays, rosh chodesh, special Shabbatot, fasts,
    days of the Omer, molad, candle lighting, and havdalah times) for the specified
    year and location.

    Args:
        year_string: The year to fetch events for (e.g., "2025")
        geoname_id: The Geonames location identifier

    Raises:
        Exception: If the API request fails with a non-200 status code

    Note:
        The cached file is stored at:
        $XDG_CACHE_HOME/cli-zmanim/events/{geoname_id}_{year}.json
    """
    # Construct Hebcal events API URL with all event flags enabled
    api_url: str = (
        f"https://www.hebcal.com/hebcal"
        f"?v=1"
        f"&cfg=json"
        f"&maj=on"  # Major holidays
        f"&min=on"  # Minor holidays
        f"&mod=on"  # Modern holidays
        f"&nx=on"  # Rosh Chodesh
        f"&year={year_string}"
        f"&ss=on"  # Special Shabbatot
        f"&mf=on"  # Minor fasts
        f"&geo=geoname"
        f"&geonameid={geoname_id}"
        f"&d=on"  # Days of the Omer
        f"&o=on"  # Molad
        f"&mvch=on"  # Candle lighting and havdalah times
    )

    request_params: dict[str, str] = {"cfg": "json"}
    response: requests.Response = requests.get(api_url, params=request_params)

    if response.status_code == 200:
        # Extract the response data
        events_data: dict[str, object] = response.json()

        # Create cache directory if it doesn't exist
        _EVENTS_CACHE_DIR.mkdir(parents=True, exist_ok=True)

        # Construct the cache file path
        cache_file_path: Path = _EVENTS_CACHE_DIR / f"{geoname_id}_{year_string}.json"

        # Write the JSON data to the cache file
        with open(cache_file_path, "w", encoding="utf-8") as cache_file:
            json.dump(events_data, cache_file, indent=4)
    else:
        raise Exception(
            f"Hebcal Events API Error: {response.status_code} - {response.text}"
        )


def load_events_from_cache(year_string: str, geoname_id: str) -> dict[str, object]:
    """
    Load Jewish calendar events from local cache for a given year and location.

    If the cache file doesn't exist, it will be created by fetching data from
    the Hebcal API first.

    Args:
        year_string: The year to load events for (e.g., "2025")
        geoname_id: The Geonames location identifier

    Returns:
        Dictionary containing the events data with structure:
        {
            "title": str,
            "date": str,
            "items": list[dict],
            ...
        }

    Note:
        Cache files are stored at:
        $XDG_CACHE_HOME/cli-zmanim/events/{geoname_id}_{year}.json
    """
    # Construct the cache file path
    cache_file_path: Path = _EVENTS_CACHE_DIR / f"{geoname_id}_{year_string}.json"

    # Attempt to load from cache, fetch and cache if not found
    try:
        with open(cache_file_path, "r", encoding="utf-8") as cache_file:
            events_data: dict[str, object] = json.load(cache_file)
            return events_data
    except FileNotFoundError:
        # Cache doesn't exist, fetch and create it
        fetch_and_cache_events(year_string, geoname_id)

        # Now load the newly created cache
        with open(cache_file_path, "r", encoding="utf-8") as cache_file:
            loaded_events_data: dict[str, object] = json.load(cache_file)
            return loaded_events_data
