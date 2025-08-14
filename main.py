import datetime

from helpers import make_default_dict, read_config, test_json  # , api_call


def main():
    location = None
    default_zmanim = make_default_dict()
    with open(".config") as f:
        location, zmanim_bool = read_config(f, default_zmanim)
    if location is None:
        location = input("enter the geonames.org identifier for your desired location")

    date = datetime.date.today().strftime("%Y-%m-%d")

    # data = api_call(location, date)
    data = test_json()

    times = data["times"]

    for k, v in times.items():
        if zmanim_bool[k]:
            date_object = datetime.datetime.strptime(v[:-6], "%Y-%m-%dT%H:%M:%S")

            do_formatted = date_object.strftime("%I:%M:%S %p")
            print(f"{k}: {do_formatted}")


if __name__ == "__main__":
    main()
