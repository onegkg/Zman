import datetime
import argparse
import sys

from helpers import api_call, format_text, make_default_dict, read_config, friday
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

    location: str | None = None
    default_zmanim: dict[str, bool] = make_default_dict()
    zmanim_bool = {}

    with open(".config") as f:
        if args.all:
            for k in default_zmanim.keys():
                zmanim_bool[k] = True
        else:
            location, zmanim_bool = read_config(f, default_zmanim)
    if location is None:
        location = input("enter the geonames.org identifier for your desired location")

    if args.date == "today":
        date_obj = datetime.date.today()
    else:
        try:
            date_obj = datetime.datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError:
            print("please enter a date in the format YYYY-MM-DD")
            sys.exit(1)


    date = date_obj.strftime("%Y-%m-%d")
    data = api_call(location, date)
    # data = test_json()

    times = data["times"]

    print_events(location, date_obj)
    for k, v in times.items():  # pyright: ignore
        if zmanim_bool[k]:
            date_object = datetime.datetime.strptime(v[:-6], "%Y-%m-%dT%H:%M:%S")

            do_formatted = date_object.strftime("%I:%M:%S %p")
            k_formatted = format_text(k)
            print(f"{k_formatted}: {do_formatted}")

if __name__ == "__main__":
    main()
