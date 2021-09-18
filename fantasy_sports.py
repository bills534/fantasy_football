import json
import os
import time
import player_data

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

print('Current Time - Timestamp of player data = Age of player data')
print(f'{current_time} - {fs_file_time} = {fs_file_age}')

# setting if we need to download new data or not
UPDATE_PLAYER_DATA = fs_file_age > age_check


    
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
        self.qb = []
        self.rb = []
        self.wr = []
        self.te = []


    def add_player(self, player):
        if player["Pos"] == 'QB':
            self.qb.append(player)
        elif player["Pos"] == 'RB':
            self.rb.append(player)
        elif player["Pos"] == 'WR':
            self.wr.append(player)
        elif player["Pos"] == 'TE':
            self.te.append(player)


    def player_count(self, pos):
        player_count = 0
        if pos.lower() == 'qb':
            player_count = len(self.qb)
        elif pos.lower() == 'rb':
            player_count = len(self.rb)
        elif pos.lower() == 'wr':
            player_count = len(self.wr)
        elif pos.lower() == 'te':
            player_count = len(self.te)
        else:
            print(f'{pos} is not a valid positon')
            return player_count
        
        print(f'There are {len(self.qb)} players in the {pos.upper()} position')
        return player_count


if UPDATE_PLAYER_DATA:
    print("Projection data is too old, downloading updated info")
    # send request to get data
    get_status, fs_json = player_data.get_sharks()

    # write the data to file
    player_data.store_data(fs_json, 'fs_player_data.json')



# start processing FS data, this this will be a good oppertunity for classes
# maybe position class that is then filled with players

# instantiate postions classes
allProjected = Position()

# load player data from json file
with open(fs_data, 'r') as json_file:
    raw_player_data = json.load(json_file)

for player in raw_player_data:
    allProjected.add_player(player)

qb_count = allProjected.player_count('qb')
print(qb_count)

# add in a strength of opponent index? maybe based on DEF ranking

# get yahoo data, either by scraping or through yahoo api

# compare roster\free agents to fs rankings
# present options to user to make decisons

