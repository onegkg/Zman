import datetime
import json

import requests


def main():
    location = None
    with open(".config") as f:
        content = f.read()
        lines = content.split("\n")
        for line in lines:
            print(line)
            if line.startswith("LOCATION_1"):
                location = line.split("=", maxsplit=1)[1].strip()
            # if line.startswith("LOCATION_2"):
            #     if loc_index == "-2":
            #     location2 = line.split("=", maxsplit=1)[1].strip()

    if location is None:
        raise Exception("no location provided")
    date = datetime.date.today().strftime("%Y-%m-%d")
    api_url = f"https://www.hebcal.com/zmanim?cfg=json&geonameid={location}&date={date}"
    params = {"cfg": "json"}

    response = requests.get(api_url, params=params)
    print(response)
    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        raise Exception("Error:", response.status_code, response.text)

    print(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
