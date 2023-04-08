# -*- encoding: utf-8 -*-

from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from datetime import date
from jinja2 import TemplateNotFound
from nba_api.stats.endpoints import commonplayerinfo, LeagueLeaders, scoreboardv2, LeagueStandingsV3,commonallplayers, commonteamroster, playerfantasyprofile 
import pandas, json, requests, os

# parsing player stats json files from local

# team IDs for 30 teams
teamIDs = [1610612743, 1610612749, 1610612738, 1610612763, 1610612758, 1610612755, 1610612739, 1610612746, 1610612752, 1610612756, 1610612744, 1610612748, 1610612750, 1610612751, 1610612737,
           1610612747, 1610612740, 1610612761, 1610612741, 1610612760, 1610612754, 1610612742, 1610612762, 1610612764, 1610612753, 1610612757, 1610612766, 1610612759, 1610612765, 1610612745]
teamIDs.sort()

@ blueprint.route('/index')
# @ login_required
def index():
    headshot_BA = requests.get(
        'https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/1628389.png')

    # top 10 average points per game leaders
    ptsLeadersPerGame = LeagueLeaders(
        per_mode48='PerGame', stat_category_abbreviation='PTS')

    ptsLeadersPerGameJson = ptsLeadersPerGame.league_leaders.get_json()
    AvgPtsTopTenLeaders = json.loads(ptsLeadersPerGameJson)['data'][0:5]
    # print(ptsLeadersPerGameJson)

    # top 10 average rebounds per game leaders
    rebLeadersPerGame = LeagueLeaders(
        per_mode48='PerGame', stat_category_abbreviation='REB')

    rebLeadersPerGameJson = rebLeadersPerGame.league_leaders.get_json()
    AvgRebTopTenLeaders = json.loads(rebLeadersPerGameJson)['data'][0:5]

    # top 10 average assists per game leaders
    astLeadersPerGame = LeagueLeaders(
        per_mode48='PerGame', stat_category_abbreviation='AST')

    astLeadersPerGameJson = astLeadersPerGame.league_leaders.get_json()
    AvgAstTopTenLeaders = json.loads(astLeadersPerGameJson)['data'][0:5]

    # top 10 average steals per game leaders
    stlLeadersPerGame = LeagueLeaders(
        per_mode48='PerGame', stat_category_abbreviation='STL')

    stlLeadersPerGameJson = stlLeadersPerGame.league_leaders.get_json()
    AvgStlTopTenLeaders = json.loads(stlLeadersPerGameJson)['data'][0:5]

    # top 10 average blocks per game leaders
    blkLeadersPerGame = LeagueLeaders(
        per_mode48='PerGame', stat_category_abbreviation='BLK')

    blkLeadersPerGameJson = blkLeadersPerGame.league_leaders.get_json()
    AvgBlkTopTenLeaders = json.loads(blkLeadersPerGameJson)['data'][0:5]

    # top 10 FG3_PCT per game leaders
    FG3_PctLeadersPerGame = LeagueLeaders(
        per_mode48='Totals', stat_category_abbreviation='FG3_PCT')

    FG3_PctLeadersPerGameJson = FG3_PctLeadersPerGame.league_leaders.get_json()
    FG3_PctTopTenLeaders = json.loads(FG3_PctLeadersPerGameJson)['data'][0:5]
    # function to round the 3pt% to 1 decimal


    def roundNum(num, decimal=1):
        return round(num, decimal)


    # League Standing
    leagueStandings = LeagueStandingsV3(
        season="2022-23", season_type="Regular Season")
    leagueStandingsJson = leagueStandings.standings.get_json()
    leagueStandings = json.loads(
        leagueStandingsJson)['data']
    # print(leagueStandings)
    eastLeagueStandings = [team for team in leagueStandings if team[6] == "East"]
    westLeagueStandings = [team for team in leagueStandings if team[6] == "West"]
    # print(eastLeagueStandings)

    # Scoreboard
    scoreboard = scoreboardv2.ScoreboardV2(
        game_date=date.today())
    line_Score_DF = scoreboard.line_score.get_data_frame(
    )
    game_Header_DF = scoreboard.game_header.get_data_frame()
    print(len(game_Header_DF))
    for game in game_Header_DF.itertuples():
        print(game.GAME_ID)

    print("____________________")
    print(line_Score_DF)
    # print(scoreboardDF[['PTS', 'TEAM_ABBREVIATION', 'GAME_ID']])

    teamRosterArray = {}
    for index in range(30):
        teamIDstr = "apps/static/player_stats_all/" + str(teamIDs[0] + index) +".json"
        with open(teamIDstr, 'r') as statsFile:
            data = json.load(statsFile);
            # data_json_string = json.dumps(data)
            teamRosterArray[str(teamIDs[0] + index)
                            ] = data[str(teamIDs[0] + index)]

    return render_template('home/index.html', segment='index', title="NBA", date=date.today(), playerStatsAll=teamRosterArray, teamIDs = teamIDs,lineScoreDF=line_Score_DF, gameHeaderDF=game_Header_DF, AvgPtsTopTenLeaders=AvgPtsTopTenLeaders, AvgRebTopTenLeaders=AvgRebTopTenLeaders, AvgAstTopTenLeaders=AvgAstTopTenLeaders, AvgStlTopTenLeaders=AvgStlTopTenLeaders, AvgBlkTopTenLeaders=AvgBlkTopTenLeaders, FG3_PctTopTenLeaders=FG3_PctTopTenLeaders, roundNum=roundNum, leagueStandings= leagueStandings, eastLeagueStandings=eastLeagueStandings, westLeagueStandings=westLeagueStandings, url="https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/")


@ blueprint.route('/<template>')
# @ login_required
def route_template(template):

    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
