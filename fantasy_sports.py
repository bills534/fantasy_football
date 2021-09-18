import json
import os
import player_data

    
class Player:
    """Holds player information"""
    def __init__(self, playerdict, position):
        self.name = playerdict["Name"]
        self.rank = playerdict["Rank"]
        self.team = playerdict["Team"]
        self.opp = playerdict["Opp"]
        self.points = playerdict["FantasyPoints"]
        if position == "PK":
            self.pos = "PK"
        elif position == "D":
            self.pos == "D"
        else:
            self.pos = playerdict["Pos"]
       

class Position:
    """Holds all the players per position"""
    def __init__(self):
        self.qb = []
        self.rb = []
        self.wr = []
        self.te = []
        self.pk = []
        self.de = []


    def add_player(self, player, position):
        if position == "PK":
            self.pk.append(player)
        elif position == "D":
            self.de.append(player)
        else:
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
        elif pos.lower() == 'de':
            player_count = len(self.de)
        elif pos.lower() == 'pk':
            player_count = len(self.pk)
        else:
            print(f'{pos} is not a valid positon')
            return player_count
        
        print(f'There are {player_count} players in the {pos.upper()} position')
        return player_count


positions = ("ALL", "PK", "D")
player_data.check_updates(positions)

# start processing FS data, this this will be a good oppertunity for classes
# maybe position class that is then filled with players

# instantiate postions class
allProjected = Position()

for position in positions:
    # load player data from json file
    with open(f'fs_{position}_data.json', 'r') as json_file:
        raw_player_data = json.load(json_file)

    for player in raw_player_data:
        if position == 'ALL':
            allProjected.add_player(player, player["Pos"])
        else:
            allProjected.add_player(player, position)
            

qb_count = allProjected.player_count('qb')
print(qb_count)
allProjected.player_count('wr')
allProjected.player_count('rb')
allProjected.player_count('de')
allProjected.player_count('pk')

# add in a strength of opponent index? maybe based on DEF ranking

# get yahoo data, either by scraping or through yahoo api

# compare roster\free agents to fs rankings
# present options to user to make decisons

