"""
Helper utilities for CLI-Zmanim.

This module provides core functionality for configuration management, API interactions,
text formatting, and time calculations for the zmanim application.
"""

import datetime
from typing import TextIO

import requests
import yaml


def read_config(
    default_config_file: TextIO, user_config_file: TextIO | None
) -> tuple[dict[str, bool], str, str | None, int, str | None]:
    """
    Read and merge user configuration with default configuration.

    Args:
        default_config_file: File handle to the default configuration YAML file
        user_config_file: File handle to the user's configuration YAML file, or None

    Returns:
        A tuple containing:
            - zmanim_toggles: Dictionary mapping zmanim names to their enabled/disabled state
            - location_name: String representation of the location (e.g., "New York, NY")
            - geonames_api_key: API key for Geonames service, or None if not provided
            - shabbat_start_minutes: Number of minutes before sunset that Shabbat starts
            - geonames_location_id: Geoname ID if provided directly, or None

    Raises:
        SystemExit: If the configuration file cannot be properly parsed
    """
    # Load default configuration
    default_config_data = yaml.safe_load(default_config_file)

    # Load and merge user configuration with defaults
    if user_config_file is not None:
        user_config_data = yaml.safe_load(user_config_file)
        merged_config = _merge_configs(user_config_data, default_config_data)
    else:
        merged_config = default_config_data

    # Extract configuration values, exit on parse failure
    try:
        zmanim_toggles: dict[str, bool] = merged_config["Zmanim"]
        location_name: str = merged_config["Settings"]["location"]
        geonames_api_key: str | None = merged_config["APIs"]["geonames_key"]
        shabbat_start_minutes: int = merged_config["Settings"]["shabbat_start"]
        geonames_location_id: str | None = merged_config["Settings"]["geonames_loc"]
    except (TypeError, KeyError):
        print(
            "Couldn't properly parse your config.yaml. If your config file contains "
            "an empty category (e.g. APIs), try removing it."
        )
        exit(1)

    return (
        zmanim_toggles,
        location_name,
        geonames_api_key,
        shabbat_start_minutes,
        geonames_location_id,
    )


def fetch_zmanim_from_hebcal(geoname_id: str, date_string: str) -> dict[str, object]:
    """
    Fetch zmanim data from the Hebcal API for a specific location and date.

    Args:
        geoname_id: The Geonames location identifier
        date_string: Date in YYYY-MM-DD format

    Returns:
        Dictionary containing the API response with zmanim times and metadata

    Raises:
        Exception: If the API request fails with a non-200 status code
    """
    api_url = (
        f"https://www.hebcal.com/zmanim"
        f"?cfg=json&geonameid={geoname_id}&date={date_string}"
    )

    request_params = {"cfg": "json"}
    response: requests.Response = requests.get(api_url, params=request_params)

    if response.status_code == 200:
        zmanim_data: dict[str, object] = response.json()
        return zmanim_data
    else:
        raise Exception(f"Hebcal API Error: {response.status_code} - {response.text}")


def format_zman_name(zman_key: str) -> str:
    """
    Convert camelCase zman keys to human-readable Hebrew/English names.

    This function uses a predefined mapping for known zmanim. For unmapped keys,
    it performs automatic formatting by adding spaces before uppercase letters
    and capitalizing the first letter.

    Args:
        zman_key: The camelCase key from the Hebcal API response

    Returns:
        A formatted, human-readable string for display

    Examples:
        >>> format_zman_name("sofZmanShma")
        'Sof Zman Shma (Gra)'
        >>> format_zman_name("sunrise")
        'Sunrise'
        >>> format_zman_name("customZman")
        'Custom Zman'
    """
    # Predefined mappings for known zmanim
    zman_display_names: dict[str, str] = {
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

    zman_key_stripped: str = zman_key.strip()

    # Return predefined name if available
    if zman_key_stripped in zman_display_names:
        return zman_display_names[zman_key_stripped]

    # Otherwise, format by adding spaces before capitals
    formatted_name: str = ""
    for index, character in enumerate(zman_key_stripped):
        if index == 0:
            # Capitalize first character
            formatted_name += character.upper()
        elif character.isupper():
            # Add space before uppercase letters
            formatted_name += " " + character
        else:
            formatted_name += character

    return formatted_name


def add_candle_lighting_time(
    zmanim_times: dict[str, str], shabbat_start_minutes: int
) -> dict[str, str]:
    """
    Add candle lighting time to the zmanim dictionary for Friday.

    Calculates candle lighting time by subtracting the configured number of minutes
    from sunset time. The candle lighting entry is inserted before the sunset entry
    to maintain proper ordering.

    Args:
        zmanim_times: Dictionary of zmanim with camelCase keys and ISO 8601 time values
        shabbat_start_minutes: Number of minutes before sunset to light candles
                               (typically 18 in diaspora, 40 in Jerusalem)

    Returns:
        New dictionary with candleLighting entry added before sunset

    Note:
        This function expects sunset time in the format: "YYYY-MM-DDTHH:MM:SS+OFFSET"
    """
    sunset_time_string: str = zmanim_times["sunset"]

    # Parse sunset time (remove timezone offset for calculation)
    sunset_datetime: datetime.datetime = datetime.datetime.strptime(
        sunset_time_string[:-6], "%Y-%m-%dT%H:%M:%S"
    )

    # Calculate candle lighting time
    candle_lighting_datetime: datetime.datetime = sunset_datetime - datetime.timedelta(
        minutes=shabbat_start_minutes
    )

    # Format back to string (add padding to match API format)
    candle_lighting_string: str = (
        candle_lighting_datetime.strftime("%Y-%m-%dT%H:%M:%S") + "      "
    )

    # Insert candle lighting before sunset
    return _insert_before_key(
        zmanim_times, "sunset", "candleLighting", candle_lighting_string
    )


def _insert_before_key(
    source_dict: dict[str, str], target_key: str, new_key: str, new_value: str
) -> dict[str, str]:
    """
    Create a new dictionary with a key-value pair inserted before a target key.

    Args:
        source_dict: The source dictionary to copy from
        target_key: The key before which the new entry should be inserted
        new_key: The key to insert
        new_value: The value for the new key

    Returns:
        A new dictionary with the entry inserted at the specified position

    Note:
        This function preserves the order of dictionary entries, which is
        guaranteed in Python 3.7+.
    """
    result_dict: dict[str, str] = {}

    for key, value in source_dict.items():
        if key == target_key:
            # Insert new key-value pair before the target key
            result_dict[new_key] = new_value
        result_dict[key] = value

    return result_dict


def _merge_configs(user_config: dict, default_config: dict) -> dict:
    """
    Recursively merge user configuration with default configuration.

    User configuration values take precedence. If both dictionaries contain
    the same key with dictionary values, they are merged recursively.

    Args:
        user_config: User's configuration dictionary
        default_config: Default configuration dictionary

    Returns:
        Merged configuration dictionary with user values taking precedence

    Note:
        This function modifies the user_config dictionary in place and returns it.
    """
    if isinstance(user_config, dict) and isinstance(default_config, dict):
        for key, default_value in default_config.items():
            if key not in user_config:
                # Key missing in user config, use default
                user_config[key] = default_value
            else:
                # Key exists in both, recursively merge if both are dicts
                user_config[key] = _merge_configs(user_config[key], default_value)

    return user_config
