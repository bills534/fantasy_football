import csv
import json
import requests
import urllib.request
from datetime import datetime
import os


fs_data = 'fs_player_data.json'

if not os.path.exists(fs_data):
    # create empty file if it doesnt exist
    with open(fs_data) as makefile:
        pass

# the goal of this whole area is to only pull down data from fs
# when needed, not sure if this should be once a week, day, or hour
# check date of current player data
print(os.path.getmtime(fs_data))

update_player_data = False


# get fantasy shark data
def get_sharks():
    """Retrives Weekly projection data from fantasy sharks, returns status code, json object"""
    # https://www.fantasysharks.com/apps/Projections/WeeklyProjections.php?pos=ALL&format=json
    fs_url = "https://www.fantasysharks.com/apps/Projections/WeeklyProjections.php"
    querystring = {"pos":"ALL","format":"json"}
    headers = {"User-Agent": "insomnia/2021.5.3"} # this is to trick the website into thinking im not a python script.

    # this is some kinda magic thing that helps handle cookies? etc...
    session = requests.Session()
    session.headers.update(headers) # trick injection
    response = session.get(url=fs_url, params=querystring)
    status_code = response.status_code
    if status_code == 200:
        print("FantasyShark data retrieved!")
        json_data = response.json()
        return status_code, json_data
    elif status_code == 400:
        print("400 Error!")
        return status_code, {}
    else:
        print(f"Something else broke, status code: {status_code}")
        return status_code, {}


def store_data(in_obj, up_file):
    with open(up_file, 'w') as writefile:
        json.dump(in_obj, writefile)
    

if update_player_data:
    # send request to get data
    get_status, fs_json = get_sharks()

    # write the data to file
    store_data(fs_json, 'fs_player_data.json')



# start processing FS data, this this will be a good oppertunity for classes
# maybe position class that is then filled with players

# separate players out by position

# add in a strength of opponent index? maybe based on DEF ranking

# get yahoo data, either by scraping or through yahoo api

# compare roster\free agents to fs rankings
# present options to user to make decisons

