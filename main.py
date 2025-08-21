import datetime
import argparse

from helpers import api_call, format_text, make_default_dict, read_config


def main():
    parser = argparse.ArgumentParser(description="parser")

    parser.add_argument('-h', '--help', action='store_true', help='help')
    parser.add_argument('-a', '--all', action='store_true', help='print all zmanim')

    args = parser.parse_args()

    if args.help:
        print("placeholder help statement")
        return

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

    date = datetime.date.today().strftime("%Y-%m-%d")
    data = api_call(location, date)
    # data = test_json()

    times = data["times"]

    for k, v in times.items():  # pyright: ignore[reportAttributeAccessIssue, reportUnknownVariableType, reportUnknownMemberType]
        if zmanim_bool[k]:
            date_object = datetime.datetime.strptime(v[:-6], "%Y-%m-%dT%H:%M:%S")  # pyright: ignore[reportUnknownArgumentType]

            do_formatted = date_object.strftime("%I:%M:%S %p")
            k_formatted = format_text(k)  # pyright: ignore[reportUnknownArgumentType]
            print(f"{k_formatted}: {do_formatted}")


if __name__ == "__main__":
    main()
