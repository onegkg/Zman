import datetime
import json
import sys

import requests


def main():
    location = None
    default_zmanim = None
    with open(".config") as f:
        location, new_dict = read_config(f, default_zmanim)
    if location is None:
        location = input("enter the geonames.org identifier for your desired location")

    date = datetime.date.today().strftime("%Y-%m-%d")

    data = api_call(location, date)

    print(json.dumps(data, indent=4))


def read_config(f, dictionary):
    location = None
    if dictionary is not None:
        new_dict = dictionary.copy()
    else:
        new_dict = None
    try:
        content = f.read()
    except Exception:
        print("file problem")
        sys.exit(1)
    lines = content.split("\n")
    for line in lines:
        if line.startswith("location_1"):
            location = line.split("=", maxsplit=1)[1].strip()
    return (location, new_dict)


def api_call(location, date):
    api_url = f"https://www.hebcal.com/zmanim?cfg=json&geonameid={location}&date={date}"
    params = {"cfg": "json"}
    response = requests.get(api_url, params=params)

    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
        return data
    else:
        raise Exception("Error:", response.status_code, response.text)


def test_json():
    with open("data.json", "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":
    main()
