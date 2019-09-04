""" Return a player statistics from FBRef. """
from collections import OrderedDict
import parser


def get_player(player_id, player_name, season):
    """ Return all statistics of a player. """

    link = parser.match_logs_link(player_id, parser.soccer_season(season),
                                  player_name)

    player_page = parser.get_page(link)

    player_pages = parser.retrieve_in_tags("<tbody>", "</tbody>",
                                           player_page)

    # return unparsed matches that a player played
    start = '<tr ><th scope="row"'
    end = '</td></tr>'
    matches = list(map(lambda x: parser.retrieve_in_tags(start, end, x),
                       player_pages))

    # Now I want to return the values between the tags
    plays = []
    for match in matches:
        plays += match

    for index, play in enumerate(plays):

        plays[index] = parser.retrieve_in_tags('>', '<', play, parse=True)

        plays[index] = list(map(lambda x: x.replace('&ndash;', '-'),
                                plays[index]))

        plays[index] = list(filter(lambda x: x not in ['', ' '], plays[index]))

        plays[index] = list(OrderedDict.fromkeys((plays[index])))

    return plays
