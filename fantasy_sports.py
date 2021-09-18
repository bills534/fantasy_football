import json
import requests
import os
import time

fs_data = 'fs_player_data.json'
# time in seconds between player data updates
# currently set to 1 hour
age_check = 3600

# need a place to store player data locally
if not os.path.exists(fs_data):
    # create empty file if it doesnt exist
    with open(fs_data, 'w') as makefile:
        pass

# the goal of this whole area is to only pull down data from fs
# when needed, not sure if this should be once a week, day, or hour
# check age of current player data
current_time = time.time()
fs_file_time = os.path.getmtime(fs_data)
fs_file_age = current_time - fs_file_time

print(f'{current_time} - {fs_file_time} = {fs_file_age}')

if fs_file_age > age_check:
    update_player_data = True
else:
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
    """Stores a json object to a file"""
    with open(up_file, 'w') as writefile:
        json.dump(in_obj, writefile)
    
class Player:
    """Holds player information"""
    def __init__(self, playerdict):
        self.name = playerdict["Name"]
        self.rank = playerdict["Rank"]
        self.pos = playerdict["Pos"]
        self.team = playerdict["Team"]
        self.opp = playerdict["Opp"]
        self.points = playerdict["FantasyPoints"]
       


class Position:
    """Holds all the players per position"""
    def __init__(self):
        # self.position = position
        self.players = []
    # maybe a top 5 method can go here
    def add_player(self, player):
        self.players.append(player)

    def player_count(self):
        print(f'There are {len(self.players)} players in this position')


if update_player_data:
    print("Projection data is too old, downloading updated info")
    # send request to get data
    get_status, fs_json = get_sharks()

    # write the data to file
    store_data(fs_json, 'fs_player_data.json')



# start processing FS data, this this will be a good oppertunity for classes
# maybe position class that is then filled with players

# instanciate postions classes
qb = Position()
rb = Position()
wr = Position()
te = Position()
de = Position()
pk = Position()

# load player data from json file
with open(fs_data, 'r') as json_file:
    raw_player_data = json.load(json_file)

for player in raw_player_data:
    if player["Pos"] == "QB":
        qb.add_player(player)


qb.player_count()

# add in a strength of opponent index? maybe based on DEF ranking

# get yahoo data, either by scraping or through yahoo api

# compare roster\free agents to fs rankings
# present options to user to make decisons

