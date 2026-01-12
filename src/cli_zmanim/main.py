import argparse
import datetime
import importlib.resources
import os
import sys
from pathlib import Path

import geocoder
from rich.traceback import install

from .date import print_events
from .helpers import format_text, friday, hebcal_call, read_config

install()


def main():
    # set up parser
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        default="today",
        help="choose the date for the data to be chosen from. Should be formatted 'YYYY-MM-DD'",
    )
    parser.add_argument(
        "-l",
        "--location",
        type=str,
        default=None,
        help="choose the location to get zmanim for.",
    )
    args = parser.parse_args()

    skip_geonames: bool = False

    # creates date object for the appropriate day
    if args.date == "today":
        date_obj = datetime.date.today()
    else:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%m/%d/%Y")
        except ValueError:
            print("please enter a date in the format MM/DD/YYYY")
            sys.exit(1)

    # Find config file
    config_dir = (
        Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "zman"
    )
    user_config_path = config_dir / "config.yaml"

    # Open config file or exit
    try:
        user_config_file = open(user_config_path)
    except FileNotFoundError:
        print(f"No config.yaml file found, please create one at {user_config_path}")
        sys.exit(1)

    # Load default config
    with importlib.resources.open_text(
        "cli_zmanim", "default_config.yaml"
    ) as default_config_file:
        zmanim_bool, location_str, geonames_key, shabbat, geonames_id = read_config(
            default_config_file, user_config_file
        )

    if geonames_id is not None or geonames_key is None:
        skip_geonames = True
        location = geonames_id

    if geonames_key is None and not skip_geonames:
        print(
            "No geonames key or ID found in config file, you can get an api key or look up the ID for your desired location at geonames.org"
        )
        sys.exit(1)

    if args.location is not None:
        location_str = args.location

    if not skip_geonames:
        try:
            geonames_obj = geocoder.geonames(location_str, key=geonames_key)
        except Exception as e:
            print(f"geonames api call failed with exception {e}")
            sys.exit(1)

        location = geonames_obj.geonames_id
        # print(location)

    date = date_obj.strftime("%Y-%m-%d")
    data = hebcal_call(location, date)

    times = data["times"]

    if date_obj.weekday() == 4:
        times = friday(times, shabbat)

    if not skip_geonames:
        print(f"Zmanim for {location_str}:")
    else:
        print(f"Zmanim for {location}")
    print_events(location, date_obj)
    print()
    for k, v in times.items():  # pyright: ignore
        if zmanim_bool[k]:
            date_object = datetime.datetime.strptime(v[:-6], "%Y-%m-%dT%H:%M:%S")

            do_formatted = date_object.strftime("%I:%M:%S %p")
            k_formatted = format_text(k)
            print(f"{k_formatted}: {do_formatted}")


if __name__ == "__main__":
    main()
