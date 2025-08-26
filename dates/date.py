from dates.date_helpers import load_events_json
import datetime


def print_events(location: str, date):
    year = date.strftime("%Y")
    data = load_events_json(year, location)
    val = date.strftime("%Y-%m-%d")
    filtered = [d for d in data["items"] if val in d.values()]
    for item in filtered:
        print(f"{item["title"]}")
    
