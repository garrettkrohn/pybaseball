from enum import Enum
from typing import NotRequired, TypedDict
from pandas import DataFrame
import pybaseball
from loguru import logger as log

class League(Enum):
    COUSIN_LEAGUE = "cousin_league"
    AARON_LEAGUE = "aaron_league"
    ALL_LEAGUES = "all_leagues"

LEAGUE = League.COUSIN_LEAGUE
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

cousin_league_teams: list[Team] = [
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

class LeagueToTeams(TypedDict):
    cousin_league: list[Team]
    aaron_league: list[Team]
    all_leagues: list[Team]

league_to_teams: LeagueToTeams = {
    League.COUSIN_LEAGUE.value: cousin_league_teams,
    League.AARON_LEAGUE.value: [],
    League.ALL_LEAGUES.value: cousin_league_teams # add other leagues here with append
}

def main():

    pitching_stats: DataFrame = pybaseball.pitching_stats(start_season=YEAR, qual=0, stat_columns=Stat.STRIKEOUTS.value)
    pitching_stats_key_value = dataframe_to_key_value_pairs(pitching_stats, Stat.STRIKEOUTS.value)

    batting_stats: DataFrame = pybaseball.batting_stats(start_season=YEAR, qual=0, stat_columns=Stat.HOMERUNS.value)
    batting_stats_key_value = dataframe_to_key_value_pairs(batting_stats, Stat.HOMERUNS.value)

    teams_to_run: list[Team] = league_to_teams.get(LEAGUE.value)
    if teams_to_run == None or len(teams_to_run) == 0:
        log.error("no teams selected")
    teams = add_stats_to_player_objects(pitching_stats_key_value, batting_stats_key_value, teams_to_run)

    sorted_teams = sort_teams(teams)

    calculated_teams = calculate_team_totals(sorted_teams)

    print_team_totals(teams)
    
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


if __name__ == "__main__":
    main()
