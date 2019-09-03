""" Return a player statistics from FBRef. """
import parser


def get_player(player_id, player_name, season):
    """ Return all statistics of a player. """

    link = parser.match_logs_link(player_id, parser.soccer_season(season),
                                  player_name)

    player_page = parser.get_page(link)
