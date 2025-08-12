import datetime
import json

import requests


def main():
    location = "4950654"
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
