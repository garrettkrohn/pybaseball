from enum import Enum
from typing import NotRequired, TypedDict
from pandas import DataFrame
import pybaseball
from loguru import logger as log

YEAR = 2025
NUMBER_OF_STARTERS = 5
NUMBER_OF_RELIEVERS = 4

class PitcherPosition(Enum):
    SP = "SP"
    RP = "RP"

class Stat(Enum):
    HOMERUNS = "HR"
    STRIKEOUTS = "SO"

class Pitcher(TypedDict):
    name: str
    position: PitcherPosition
    strikeouts: NotRequired[int]
    used: NotRequired[bool]

class Batter(TypedDict):
    name: str
    homeruns: NotRequired[int]

class Team(TypedDict):
    teamName: str
    pitchingPlayers: list[Pitcher]
    battingPlayers: list[Batter]
    finalStrikeoutTotal: NotRequired[int]
    finalHomerunTotal: NotRequired[int]

all_teams: list[Team] = [
    {
        "teamName": "Aaron",
        "pitchingPlayers": [
            {"name": "Paul Skenes", "position": PitcherPosition.SP},
            {"name": "Zack Wheeler", "position": PitcherPosition.SP},
            {"name": "Chris Sale", "position": PitcherPosition.SP},
            {"name": "Jack Flaherty", "position": PitcherPosition.SP},
            {"name": "Shota Imanaga", "position": PitcherPosition.SP},
            {"name": "Jacob deGrom", "position": PitcherPosition.SP},
            {"name": "Sandy Alcantara", "position": PitcherPosition.SP},
            {"name": "Tanner Scott", "position": PitcherPosition.RP},
            {"name": "Devin Williams", "position": PitcherPosition.RP},
            {"name": "Cade Smith", "position": PitcherPosition.RP},
            {"name": "Felix Bautista", "position": PitcherPosition.RP},
            {"name": "Ryan Helsley", "position": PitcherPosition.RP},
            {"name": "Edwin Uceta", "position": PitcherPosition.RP}
        ],
        "battingPlayers": [
            {"name": "Christian Walker"},
            {"name": "Ketel Marte"},
            {"name": "Jose Ramirez"},
            {"name": "Gunnar Henderson"},
            {"name": "William Contreras"},
            {"name": "Riley Greene"},
            {"name": "Jackson Merrill"},
            {"name": "Juan Soto"},
            {"name": "Brent Rooker"},
            {"name": "Kyle Tucker"},
        ]
    },
    {
        "teamName": "Garrett",
        "pitchingPlayers" : [
            {"name": "Michael King", "position": PitcherPosition.SP},
            {"name": "Logan Gilbert", "position": PitcherPosition.SP},
            {"name": "Garrett Crochet", "position": PitcherPosition.SP},
            {"name": "Hunter Greene", "position": PitcherPosition.SP},
            {"name": "Reid Detmers", "position": PitcherPosition.SP},
            {"name": "MacKenzie Gore", "position": PitcherPosition.SP},
            {"name": "Jose Berrios", "position": PitcherPosition.SP},
            {"name": "Justin Martinez", "position": PitcherPosition.RP},
            {"name": "Bryan Abreu", "position": PitcherPosition.RP},
            {"name": "Griffin Jax", "position": PitcherPosition.RP},
            {"name": "Ryan Walker", "position": PitcherPosition.RP},
            {"name": "Jose Butto", "position": PitcherPosition.RP},
            {"name": "Jose Leclerc", "position": PitcherPosition.RP}
        ],
        "battingPlayers": [
            {"name": "Jake Burger"},
            {"name": "Jazz Chisholm Jr."},
            {"name": "Austin Riley"},
            {"name": "Elly De La Cruz"},
            {"name": "Salvador Perez"},
            {"name": "Taylor Ward"},
            {"name": "Julio Rodriguez"},
            {"name": "Teoscar Hernandez"},
            {"name": "Kyle Schwarber"},
            {"name": "Vladimir Guerrero Jr."},
        ]
    }
]

def main():

    pitching_stats: DataFrame = pybaseball.pitching_stats(start_season=YEAR, qual=0, stat_columns=Stat.STRIKEOUTS.value)
    pitching_stats_key_value = dataframe_to_key_value_pairs(pitching_stats, Stat.STRIKEOUTS.value)

    batting_stats: DataFrame = pybaseball.batting_stats(start_season=YEAR, qual=0, stat_columns=Stat.HOMERUNS.value)
    batting_stats_key_value = dataframe_to_key_value_pairs(batting_stats, Stat.HOMERUNS.value)

    teams = add_stats_to_player_objects(pitching_stats_key_value, batting_stats_key_value, all_teams)

    sorted_teams = sort_teams(teams)

    calculated_teams = calculate_team_totals(sorted_teams)

    print_team_totals(teams)
    

    # hitters
    # final_players_hitting = get_player_objects_with_stat(hitting_teams, Stat.HOMERUNS)
    # hitting_sorted_list = sorted(final_players_hitting, key=lambda x: x[Stat.HOMERUNS])
    # hitting_reversed_list = hitting_sorted_list[::-1]
    # homeRuns(hitting_reversed_list)

    # pitchers
    # final_players_pitching = get_player_objects_with_stat(pitching_teams, Stat.STRIKEOUTS)
    # pitching_sorted_list = sorted(final_players_pitching, key=lambda x: x[Stat.STRIKEOUTS])
    # pitching_reversed_list = pitching_sorted_list[::-1]
    # strikeouts(pitching_reversed_list)

def dataframe_to_key_value_pairs(df: DataFrame, stat: str) -> dict[str, int]:
    key_value_dict = {}
    for _, row in df.iterrows():
        key_value_dict[row['Name']] = row[stat]
    return key_value_dict

def add_stats_to_player_objects(pitching_stats: dict[str,int], batting_stats: dict[str,int], teams: list[Team]) -> list[Team]:
    for team in teams:
        pitchers = team['pitchingPlayers']
        for pitcher in pitchers:
            try:
                pitcher['strikeouts'] = pitching_stats[pitcher['name']]
            except:
                log.error(f'could not find pitcher {pitcher["name"]}')
                continue

        batters = team['battingPlayers']
        for batter in batters:
            try:
                batter['homeruns'] = batting_stats[batter['name']]
            except:
                log.error(f'could not find batter {batter["name"]}')
                continue

    return teams

def sort_teams(teams: list[Team]):
    for team in teams:
        team['pitchingPlayers'].sort(key=lambda pitcher: pitcher.get('strikeouts', 0), reverse=True)
        team['battingPlayers'].sort(key=lambda batter: batter.get('homeruns', 0), reverse=True)
    return teams


def calculate_team_totals(teams: list[Team]):
    for team in teams:
        total_homeruns = 0
        for batter in team.get('battingPlayers'):
            total_homeruns += batter.get('homeruns', 0)
        team['finalHomerunTotal'] = total_homeruns

        total_strikeouts = 0
        used_sp = 0
        used_rp = 0
        for pitcher in team.get('pitchingPlayers'):
            if pitcher.get('position') == PitcherPosition.SP:
                if used_sp < NUMBER_OF_STARTERS:
                    total_strikeouts += pitcher.get('strikeouts', 0)
                    pitcher['used'] = True
                    used_sp += 1
            else:
                if used_rp < NUMBER_OF_RELIEVERS:
                    total_strikeouts += pitcher.get('strikeouts', 0)
                    pitcher['used'] = True
                    used_rp += 1
        team['finalStrikeoutTotal'] = total_strikeouts

def print_team_totals(teams: list[Team]):
    for team in teams:
        print(f"\n{team['teamName']} strikeout total is: {team.get('finalStrikeoutTotal', 0)}")
        for pitcher in team['pitchingPlayers']:
            try:
                print(f"{"*" if pitcher.get('used') else ''} {pitcher.get('position').value} {pitcher['name']}: {pitcher.get('strikeouts')}")
            except:
                print(f"{pitcher['name']}: 0")
        print(f"\n{team['teamName']} homerun total is: {team.get('finalHomerunTotal', 0)}")
        for batter in team['battingPlayers']:
            try:
                print(f"{batter['name']}: {batter.get('homeruns')}")
            except:
                print(f"{batter['name']}: 0")





# def get_player_objects_with_stat(teams, stat):
#     final_players = []
#     for team_name, player_list in teams.items():
#         log.info(f'fetching players for {team_name}')
#         for player in player_list:
#             player_name = player.get("name")
#             if LOG_LEVEL == "debug":
#                 print(f'fetching data for {player_name}')
#             player_obj = look_up_single_stat(player_name, stat)
#             player_obj["team_name"] = team_name
#             player_obj["position"] = player.get("position")
#             final_players.append(player_obj)
#     return final_players
#
# def look_up_single_stat(player_name, stat_name):
#     player = statsapi.lookup_player(player_name)
#     if not player:
#         print(f'can\'t find player {player_name}')
#         return {"name": player_name, stat_name: 0}
#     id = player[0].get("id")
#
#     stats = statsapi.player_stats(id)
#     pattern = fr'{stat_name}: \s*(\d+)'
#
#     match = re.search(pattern, stats)
#
#     final_stat = None
#
#     if match:
#         final_stat = int(match.group(1))
#     else:
#         print("error")
#
#     final_player = {"name": player[0].get("fullName"), stat_name: final_stat}
#     return final_player
#
# def homeRuns(final_players):
#     garrett_total = 0
#     aaron_total = 0
#
#     for player_obj in final_players:
#         if player_obj.get("team_name") == "team_garrett":
#             garrett_total += player_obj.get(Stat.HOMERUNS)
#         elif player_obj.get("team_name") == "team_aaron":
#             aaron_total += player_obj.get(Stat.HOMERUNS)
#
#     print(f'\ngarrett total: {garrett_total}\naaron total: {aaron_total}\n')
#
#     for item in final_players:
#         print(f'{item.get(Stat.HOMERUNS)} for {item.get("name")} for {item.get("team_name")}')
#
# def print_pitchers(pitcher_list, number_of_pitchers, header):
#     print(header)
#     count = 1
#     for pitcher in pitcher_list[:number_of_pitchers]:
#         print(f'{count} {pitcher.get("name")} {pitcher.get(Stat.STRIKEOUTS)}')
#         count += 1
#
# def strikeouts(final_players):
#     garrett_total = 0
#     aaron_total = 0
#     garrett_sp = []
#     garrett_rp = []
#     aaron_sp = []
#     aaron_rp = []
#
#     for player_obj in final_players:
#         position = player_obj.get("position")
#         team = player_obj.get("team_name") 
#         if team == "team_garrett":
#             if position == "SP":
#                 garrett_sp.append(player_obj)
#             elif position == "RP":
#                 garrett_rp.append(player_obj)
#         elif team == "team_aaron":
#             if position == "SP":
#                 aaron_sp.append(player_obj)
#             elif position == "RP":
#                 aaron_rp.append(player_obj)
#
#     if LOG_LEVEL == 'debug':
#         print('garrett_sp', garrett_sp)
#         print('garrett_rp', garrett_rp)
#         print('aaron_sp', aaron_sp)
#         print('aaron_rp', aaron_rp)
#
#     garrett_5_sp = garrett_sp[:5]
#     garrett_4_rp = garrett_rp[:4]
#     aaron_5_sp= aaron_sp[:5]
#     aaron_4_rp = aaron_rp[:4]
#
#     for starter in garrett_5_sp:
#         garrett_total += starter.get(Stat.STRIKEOUTS)
#
#     for reliever in garrett_4_rp:
#         garrett_total += reliever.get(Stat.STRIKEOUTS)
#
#     for starter in aaron_5_sp[:5]:
#         aaron_total+= starter.get(Stat.STRIKEOUTS)
#
#     for reliever in aaron_4_rp[:4]:
#         aaron_total += reliever.get(Stat.STRIKEOUTS)
#
#     print(f'\nGarrett total: {garrett_total}\nAaron total: {aaron_total}')
#
#     print_pitchers(garrett_5_sp, 5, "\nGarrett Starters: ")
#     print_pitchers(garrett_4_rp, 4, "\nGarrett Relievers: ")
#
#     print_pitchers(aaron_5_sp, 5, "\nAaron Starters: ")
#     print_pitchers(aaron_4_rp, 4, "\nAaron Relievers: ")

if __name__ == "__main__":
    main()

# search for player
# player = statsapi.lookup_player("Pablo López")
# print(player)

# player = statsapi.lookup_player("Kenley Jansen")
# id = player[0].get("id")
# stats = statsapi.player_stats(id)
# print(player[0])
