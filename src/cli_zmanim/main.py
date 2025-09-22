import datetime
import argparse
import sys
import geocoder
import importlib.resources
from pathlib import Path
import os

from .helpers import hebcal_call, format_text, read_config, friday
from .dates.date import print_events


def main():
    parser = argparse.ArgumentParser()

    # parser.add_argument("-a", "--all", action="store_true", help="print all zmanim")
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
            help="choose the location to get zmanim for."
            )

    args = parser.parse_args()

    if args.date == "today":
        date_obj = datetime.date.today()
    else:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%m/%d/%Y")
        except ValueError:
            print("please enter a date in the format MM/DD/YYYY")
            sys.exit(1)

    config_dir = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "zman"
    user_config_path = config_dir / "config.yaml"

    try: 
        user_config_file = open(user_config_path)
    except FileNotFoundError:
        print(f"No config.yaml file found, please create one at {user_config_path}")
        sys.exit(1)

    with importlib.resources.open_text("cli_zmanim", "default_config.yaml") as default_config_file:
        zmanim_bool, location_str, geonames_key, shabbat = read_config(default_config_file, user_config_file)

    if geonames_key is None:
        print("It looks like you haven't included a geonames_key in your config.yaml file. If you need a geonames API key, you can create an account at https://www.geonames.org/login")
        sys.exit(1)

    if args.location is not None:
        location_str = args.location

    try:
        geonames_obj = geocoder.geonames(location_str, key=geonames_key)
    except Exception as e:
        print(f"geonames api call failed with exception {e}")
        sys.exit(1)

    location = geonames_obj.geonames_id

    date = date_obj.strftime("%Y-%m-%d")
    data = hebcal_call(location, date)

    times = data["times"]

    if date_obj.weekday() == 4:
        times = friday(times, shabbat)

    print(f"Zmanim for {location_str}:")
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
