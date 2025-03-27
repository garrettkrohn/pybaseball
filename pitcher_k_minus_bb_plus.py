from pybaseball import pitching_stats, cache
from tabulate import tabulate

QUALIFYING_MARK = 30
YEAR = 2024
ORDER_BY_STAT = 'Stuff+'

def main():

    cache.enable()

    all_pitching_stats = get_all_pitching_stats()
    league_k_minus_bb_average = calculate_league_average_k_minus_bb_percentage(all_pitching_stats)
    all_pitching_stats_sorted = sort_pitching_stats(all_pitching_stats,
                                                    ORDER_BY_STAT,
                                                    descending=True)

    twins_pitching_stats = get_twins_pitching_stats()

    twins_pitching_stats_sorted = sort_pitching_stats(twins_pitching_stats,
                                                      ORDER_BY_STAT,
                                                      descending=True)

    print_pitching_stats_table(twins_pitching_stats_sorted, league_k_minus_bb_average)

def print_pitching_stats_table(pitching_stats, league_k_minus_bb_average):
    table = []
    for pitcher in pitching_stats:
        raw_k = pitcher.get('K%', 0)
        raw_bb = pitcher.get('BB%', 0)
        raw_k_minus_bb = raw_k - raw_bb
        k_percentage = format_percentage(raw_k)
        bb_percentage = format_percentage(raw_bb)
        k_minus_bb_percentage = format_percentage(raw_k_minus_bb)
        k_minus_bb_percentage_plus = format_plus_stat((raw_k_minus_bb / league_k_minus_bb_average))

        table.append({
            'Name': pitcher.get('Name'),
            'IP': pitcher.get('IP'),
            'K%': k_percentage,
            'BB%': bb_percentage,
            'K-BB%': k_minus_bb_percentage,
            'K-BB%+': k_minus_bb_percentage_plus,
            'Stuff+': pitcher.get('Stuff+'),
            'Loc+': pitcher.get('Location+'),
            'Pitch+': pitcher.get('Pitching+'),
            'xFIP': pitcher.get('xFIP')
        })

    headers = table[0].keys()
    rows = [x.values() for x in table]
    print(tabulate(rows, headers=headers, tablefmt='grid'))


def sort_pitching_stats(pitching_stats, attribute, descending=False):
    return sorted(pitching_stats, key=lambda x: x.get(attribute, 0), reverse=descending)

def format_plus_stat(stat):
    return round(int(stat * 100), 0)

def get_all_pitching_stats():
    all_pitching_stats = pitching_stats(start_season=YEAR, 
                                 qual=QUALIFYING_MARK, 
                                 stat_columns='all')
    
    return all_pitching_stats.to_dict(orient='records')

def get_twins_pitching_stats():
    all_pitching_stats = pitching_stats(start_season=YEAR, 
                                 qual=QUALIFYING_MARK, 
                                 stat_columns='all',
                                 team=8)
    
    return all_pitching_stats.to_dict(orient='records')


def format_percentage(number):
    return f"{round((number * 100), 2)}%"

def calculate_league_average_k_minus_bb_percentage(pitcher_stats):
    number_of_pitchers = len(pitcher_stats)
    stat_sum = 0
    for pitcher_stat in pitcher_stats:
        k_per = pitcher_stat.get('K%')
        bb_per = pitcher_stat.get('BB%')
        stat_sum += k_per - bb_per
    return stat_sum / number_of_pitchers

def calculate_league_average_stat(pitcher_stats, stat_name: str):
    number_of_pitchers = len(pitcher_stats)
    stat_sum = 0
    for pitcher_stat in pitcher_stats:
        k_per = pitcher_stat.get(stat_name)
    return stat_sum / number_of_pitchers

if __name__ == "__main__":
    main()
