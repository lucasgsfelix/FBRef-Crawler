""" Return a player statistics from FBRef. """
from collections import OrderedDict
import parser


def get_player(player_id, player_name, season):
    """ Return all statistics of a player. """

    player_info = {}

    link = parser.match_logs_link(player_id, parser.soccer_season(season),
                                  player_name)

    player_page = parser.get_page(link)

    player_info['Name'] = player_name
    player_info['Id'] = player_id

    token = "Position:</strong>"
    player_info['Position'] = parser.retrieve_in_tags(token, '<', player_page,
                                                      parse=True)

    token = 'Footed:</strong>'
    player_info['Foot'] = parser.retrieve_in_tags(token, '<', player_page,
                                                  parse=True)

    token = 'itemprop="height">'
    player_info['Height'] = parser.retrieve_in_tags(token, '<', player_page,
                                                    parse=True)

    token = 'itemprop="weight">'
    player_info['Weight'] = parser.retrieve_in_tags(token, '<', player_page,
                                                    parse=True)

    player_info['Season'] = parser.soccer_season(season)

    token = 'data-birth="'
    end = '">'
    key = 'Birth Date'
    player_info[key] = parser.retrieve_in_tags(token, end, player_page,
                                               parse=True)

    token = 'itemprop="birthPlace">'
    end = '</span>'
    key = 'Birth Place'
    player_info[key] = parser.retrieve_in_tags(token, end, player_page,
                                               parse=True)

    token = 'National Team:</strong>'
    key = 'National Team'
    player_info[key] = parser.retrieve_in_tags(token, '<span', player_page,
                                               parse=True)

    player_page = parser.retrieve_in_tags("<tbody>", "</tbody>", player_page)

    player_info['Matches'] = player_matches(player_page)

    return player_info


def player_matches(player_page):
    ''' Get all the matches that a player has played in a season.'''

    # return unparsed matches that a player played
    start = '<tr ><th scope="row"'
    end = '</td></tr>'
    matches = list(map(lambda x: parser.retrieve_in_tags(start, end, x),
                       player_page))

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
