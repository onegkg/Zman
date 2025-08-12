from datetime import datetime


def main():
    # declare api variables
    api_user = None
    api_key = None
    api_location = None

    # initialize variables with values from .config
    with open(".config") as file:
        content = file.read()
        lines = content.split("\n")

    for line in lines:
        if line.startswith("USER"):
            api_user = line.split("=", maxsplit=1)[1].strip()
        if line.startswith("KEY"):
            api_key = line.split("=", maxsplit=1)[1].strip()
        if line.startswith("LOCATION"):
            api_location = line.split("=", maxsplit=1)[1].strip()

    api_url = "https://api.myzmanim.com/getDay"

    params = {
        "user": api_user,
        "key": api_key,
        "coding": "PY",
        "language": "en",
        "locationID": api_location,
        "inputDate": datetime.now().strftime("%Y-%m-%d"),
    }

    for k, v in params.items():
        print(k, v)

    # response = requests.get(api_url)
    # print(response.json())


if __name__ == "__main__":
    main()
