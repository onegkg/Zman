import datetime
import argparse
import sys
import geocoder

from helpers import hebcal_call, format_text, read_config, friday
from dates.date import print_events


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--all", action="store_true", help="print all zmanim")
    parser.add_argument(
        "-d",
        "--date",
        type=str,
        default="today",
        help="choose the date for the data to be chosen from. Should be formatted 'YYYY-MM-DD'",
    )

    args = parser.parse_args()

    if args.date == "today":
        date_obj = datetime.date.today()
    else:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("please enter a date in the format YYYY-MM-DD")
            sys.exit(1)

    default_config = open("default_config.yaml")
    try: 
        user_config = open("config.yaml")
    except Exception:
        user_config = None


    zmanim_bool, location_str, geonames_key, shabbat = read_config(default_config, user_config)

    try:
        geonames_obj = geocoder.geonames(location_str, key=geonames_key)
    except Exception as e:
        print(f"geonames api call failed with exception {e}")
        print("The most likely issue is that you forgot to include your geonames api key in your config.yaml, see the docs for more info.")
        sys.exit(1)

    location = geonames_obj.geonames_id

    date = date_obj.strftime("%Y-%m-%d")
    data = hebcal_call(location, date)

    times = data["times"]

    if date_obj.weekday() == 4:
        times = friday(times, shabbat)

    print_events(location, date_obj)
    for k, v in times.items():  # pyright: ignore
        if zmanim_bool[k]:
            date_object = datetime.datetime.strptime(v[:-6], "%Y-%m-%dT%H:%M:%S")

            do_formatted = date_object.strftime("%I:%M:%S %p")
            k_formatted = format_text(k)
            print(f"{k_formatted}: {do_formatted}")

if __name__ == "__main__":
    main()
