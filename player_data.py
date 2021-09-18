import json
import requests

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
    """Stores a json object to a file"""
    with open(up_file, 'w') as writefile:
        json.dump(in_obj, writefile)