
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
# from IPython.display import display
import requests, time
from nba_api.stats.endpoints import commonplayerinfo, LeagueLeaders, scoreboardv2, leaguestandingsv3, shotchartdetail, commonallplayers, commonteamroster, playerfantasyprofile
from datetime import date
import json, sys
from nba_api.stats.library.parameters import LeagueID, PerMode48, Scope, Season, SeasonTypeAllStar, PerModeSimple, StatCategoryAbbreviation


# teamRosters1 = {}
# teamRosters2 = {}
# teamRosters3 = {}
# for teamID in teamIDs[13:14]:
#     commonRoster = commonteamroster.CommonTeamRoster(team_id=teamID, timeout=100).get_data_frames()[
#         0][["PLAYER_ID", "PLAYER"]].to_numpy()
#     team = {}
#     for i in commonRoster:
#         player = {}
#         player["FULL_NAME"] = i[1]
#         player["Stats"] = playerfantasyprofile.PlayerFantasyProfile(
#             player_id=i[0], per_mode36="PerGame").get_data_frames()[0].to_dict()
#         team[i[0]] = player
#         time.sleep(2)
#     # print(commonRoster)
#     # players = {}
#     # players["FULL_NAME"] = commonRoster[1]
#     teamRosters1[teamID] = team
#     # print(teamRosters1)
# print(teamRosters1)

# teamRosters1_json_str = json.dumps(teamRosters1)
# with open(str(teamIDs[13]) + ".json", "w") as output_file:
#     output_file.write(teamRosters1_json_str)

args = sys.argv[1:]

for arg in args:
    print(arg)