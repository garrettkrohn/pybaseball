from pybaseball import statcast_pitcher_pitch_arsenal

# get average pitch speed data for all qualified pitchers in 2019
# all_pitchers_arsenals_velo = statcast_pitcher_pitch_arsenal(2024)
# dict = all_pitchers_arsenals_velo.to_dict(orient='records')
# for pitcher in dict:
#     print(pitcher)

# get average pitch spin data for pitchers with at least 200 pitches in 2019
# all_pitchers_arsenals_spin = statcast_pitcher_pitch_arsenal(2019, minP=200, arsenal_type="avg_spin")
# dict = all_pitchers_arsenals_spin.to_dict(orient='records')
# for pitcher in dict:
#     print(pitcher)

# get percentage shares data for qualified pitchers in 2019
data = statcast_pitcher_pitch_arsenal(2024, arsenal_type="n_")
dict = data.to_dict(orient='records')
for pitcher in dict:
    print(pitcher)
