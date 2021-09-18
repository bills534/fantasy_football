import json
import requests
import time
import os


# time in seconds between player data updates
# currently set to 1 hour
age_check = 3600


# get fantasy shark data
def get_sharks(position):
    """Retrives Weekly projection data from fantasy sharks, returns status code, json object"""
    # https://www.fantasysharks.com/apps/Projections/WeeklyProjections.php?pos=ALL&format=json
    fs_url = "https://www.fantasysharks.com/apps/Projections/WeeklyProjections.php"
    querystring = {"pos": position,"format":"json"}
    headers = {"User-Agent": "insomnia/2021.5.3"} # this is to trick the website into thinking im not a python script.

    # this is some kinda magic thing that helps handle cookies? etc...
    session = requests.Session()
    session.headers.update(headers) # trick injection
    response = session.get(url=fs_url, params=querystring)
    status_code = response.status_code
    if status_code == 200:
        print(f"FantasyShark {position} data retrieved!")
        json_data = response.json()
        return status_code, json_data
    elif status_code == 400:
        print("400 Error!")
        return status_code, {}
    else:
        print(f"Something else broke, status code: {status_code}")
        return status_code, {}


def store_data(in_obj, up_file):
    """Stores a json object to a file"""
    with open(up_file, 'w') as writefile:
        json.dump(in_obj, writefile)


def check_updates(positions):
    """Function checks for all the player files and updates if needed"""
    for position in positions:
        pos_file = f'fs_{position}_data.json'
        if not os.path.exists(pos_file):
            with open(pos_file, 'w') as makefile:
                pass
            status, current_data = get_sharks(position)
            if status == 200:
                store_data(current_data, pos_file)
        else:
            current_time = time.time()
            fs_file_time = os.path.getmtime(pos_file)
            fs_file_age = current_time - fs_file_time
            print(f'Current Time - Timestamp of player data = Age of {position} data')
            print(f'{current_time} - {fs_file_time} = {fs_file_age}')
            if fs_file_age > age_check:
                status, current_data = get_sharks(position)
                if status == 200:
                    store_data(current_data, pos_file)
