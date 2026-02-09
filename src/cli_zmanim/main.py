"""
CLI-Zmanim: Command-line interface for Jewish prayer times (zmanim).

This is the main entry point for the CLI-Zmanim application. It handles command-line
argument parsing, configuration loading, API calls, and output formatting for displaying
zmanim (Jewish prayer times) and Jewish calendar events for any location and date.
"""

import argparse
import datetime
import importlib.resources
import os
import sys
from pathlib import Path

import geocoder
from rich.traceback import install

from .date import print_events
from .helpers import (
    add_candle_lighting_time,
    fetch_zmanim_from_hebcal,
    format_zman_name,
    read_config,
)

# Install rich traceback for better error messages
install()


def main() -> None:
    """
    Main entry point for the CLI-Zmanim application.

    Parses command-line arguments, loads configuration, fetches zmanim data from
    the Hebcal API, and displays formatted output of prayer times and Jewish
    calendar events.

    Command-line Arguments:
        -d, --date: Date in MM/DD/YYYY format (default: today)
        -l, --location: Location string (e.g., "Boston, MA") to override config

    Exit Codes:
        0: Success
        1: Error (invalid date format, missing config, API failure, etc.)
    """
    # Parse command-line arguments
    argument_parser = argparse.ArgumentParser(
        description="Display Jewish prayer times (zmanim) for any location and date"
    )
    argument_parser.add_argument(
        "-d",
        "--date",
        type=str,
        default="today",
        help="Date to display zmanim for. Format: MM/DD/YYYY (default: today)",
    )
    argument_parser.add_argument(
        "-l",
        "--location",
        type=str,
        default=None,
        help="Location to get zmanim for (overrides config setting)",
    )
    parsed_args = argument_parser.parse_args()

    # Create date object for the requested day
    if parsed_args.date == "today":
        target_date: datetime.date = datetime.date.today()
    else:
        try:
            target_datetime = datetime.datetime.strptime(parsed_args.date, "%m/%d/%Y")
            target_date = target_datetime.date()
        except ValueError:
            print("Error: Please enter a date in the format MM/DD/YYYY")
            sys.exit(1)

    # Locate user configuration file
    config_directory = (
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "zman"
    )
    user_config_path = config_directory / "config.yaml"

    # Open user config file or exit with helpful message
    try:
        user_config_file = open(user_config_path, encoding="utf-8")
    except FileNotFoundError:
        print(
            f"Error: No config.yaml file found.\n"
            f"Please create one at: {user_config_path}"
        )
        sys.exit(1)

    # Load default configuration bundled with the package
    with importlib.resources.open_text(
        "cli_zmanim", "default_config.yaml"
    ) as default_config_file:
        (
            zmanim_toggles,
            location_name,
            geonames_api_key,
            shabbat_start_minutes,
            geonames_location_id,
        ) = read_config(default_config_file, user_config_file)

    # Close user config file
    user_config_file.close()

    # Override default location with command-line argument if provided
    if parsed_args.location is not None:
        location_name = parsed_args.location

    # Determine if we can skip the Geonames API call
    should_skip_geonames: bool = geonames_location_id is not None
    resolved_geoname_id: str

    if should_skip_geonames:
        # Geoname ID provided directly in config
        resolved_geoname_id = geonames_location_id
    else:
        # Need to use Geonames API to resolve location name to ID
        if geonames_api_key is None:
            print(
                "Error: No geonames_key or geonames_loc found in config file.\n"
                "You can either:\n"
                "  1. Get a free API key from https://www.geonames.org/login\n"
                "  2. Look up your location's Geoname ID at https://www.geonames.org\n"
                "     and set it as 'geonames_loc' in your config"
            )
            sys.exit(1)

        # Call Geonames API to resolve location name to geoname ID
        try:
            geonames_result = geocoder.geonames(location_name, key=geonames_api_key)
            resolved_geoname_id = geonames_result.geonames_id
        except Exception as error:
            print(f"Error: Geonames API call failed with exception: {error}")
            sys.exit(1)

    # Convert date to API-compatible string format
    date_string: str = target_date.strftime("%Y-%m-%d")

    # Fetch zmanim data from Hebcal API
    try:
        hebcal_response_data = fetch_zmanim_from_hebcal(
            resolved_geoname_id, date_string
        )
    except Exception as error:
        print(f"Error: Hebcal API call failed: {error}")
        sys.exit(1)

    # Extract times dictionary from the API response
    zmanim_times: dict[str, str] = hebcal_response_data["times"]  # type: ignore

    # If it's Friday, add candle lighting time
    is_friday: bool = target_date.weekday() == 4
    if is_friday:
        zmanim_times = add_candle_lighting_time(zmanim_times, shabbat_start_minutes)

    # Print location header
    if should_skip_geonames:
        print(f"Zmanim for location with Geoname ID: {resolved_geoname_id}")
    else:
        print(f"Zmanim for {location_name}:")

    # Print Jewish calendar events for the date
    print_events(resolved_geoname_id, target_date)
    print()

    # Print each enabled zman with formatted time
    for zman_key, time_string in zmanim_times.items():
        # Only display zmanim that are enabled in config
        if zmanim_toggles.get(zman_key, False):
            # Parse the ISO 8601 datetime string (remove timezone offset)
            time_datetime = datetime.datetime.strptime(
                time_string[:-6], "%Y-%m-%dT%H:%M:%S"
            )

            # Format time for display (12-hour format with AM/PM)
            formatted_time: str = time_datetime.strftime("%I:%M:%S %p")

            # Format the zman name for display
            formatted_zman_name: str = format_zman_name(zman_key)

            # Print the zman with formatted name and time
            print(f"{formatted_zman_name}: {formatted_time}")


if __name__ == "__main__":
    main()
