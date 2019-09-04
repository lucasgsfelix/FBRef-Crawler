""" Crawler players logs from fbref.com"""
import players


if __name__ == '__main__':

    SEASON_START, SEASON_END = 2015, 2019

    with open("Input/players_info.txt", 'r') as file:

        PLAYERS_INFO = file.read().split('\n')

        PLAYERS_INFO = list(map(lambda x: x.split('\t'), PLAYERS_INFO))

        # making a dict with player_id : player_name
        PLAYERS_INFO.pop(0)  # removing header
        PLAYERS_INFO = {player[1]: player[0] for player in PLAYERS_INFO}

    HEADER = True
    for season in range(SEASON_START, SEASON_END):

        for player in PLAYERS_INFO:
            players.get_player(player, PLAYERS_INFO[player], season,
                               header=HEADER)
            HEADER = False
