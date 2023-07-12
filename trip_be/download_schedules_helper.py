import json
import os
import time

import requests

SCHEDULES_DIRECTORY = os.path.join(os.getcwd(), "bus_data", "schedules")
STOP_TIMES_DIRECTORY = os.path.join(os.getcwd(), "bus_data", "stop_times.json")
DATE_INDICATOR = "stopTimes?date="


def load_schedule():
    date_len = 10
    with open(STOP_TIMES_DIRECTORY) as schedule_urls_file:
        schedule_urls = json.load(schedule_urls_file)
        total_buses_number = len(schedule_urls)
        for index, (bus_id, urls) in enumerate(schedule_urls.items()):
            print(f"{index * 100 / total_buses_number:.0f}%")
            for url in urls:
                date_start_index = url.index(DATE_INDICATOR) + len(DATE_INDICATOR)
                date = url[date_start_index : date_start_index + date_len]
                _create_directory_for_date(date)
                schedule_destination_path = os.path.join(SCHEDULES_DIRECTORY, date, f"{bus_id}.json")
                try:
                    response = requests.get(url, allow_redirects=True)
                except requests.exceptions.ConnectionError:
                    print("Connection Error - waiting two minutes to pass requests limitation...")
                    for second in range(120):
                        print(f"Waiting {second} seconds")
                        time.sleep(1)
                    response = requests.get(url, allow_redirects=True)

                with open(schedule_destination_path, mode="wb") as schedule_destination_file:
                    schedule_destination_file.write(response.content)


def _create_directory_for_date(date: str) -> None:
    try:
        os.mkdir(os.path.join(SCHEDULES_DIRECTORY, date))
    except FileExistsError:
        pass


if __name__ == "__main__":
    load_schedule()
