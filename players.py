""" Return a player statistics from FBRef. """
from collections import OrderedDict
import parser


def get_player(player_id, player_name, season, header=False):
    """ Return all statistics of a player. """
    print("Evaluating ", player_name, "in season:", season)

    player_info = {}

    link = parser.match_logs_link(player_id, parser.soccer_season(season),
                                  player_name)

    player_page = parser.get_page(link)

    # when a not valid link is returned
    if "<tbody>" not in player_page:
        link = parser.logs_link(player_id, str(season), player_name)
        player_page = parser.get_page(link)

    player_info['Name'] = player_name
    player_info['Id'] = player_id

    token = "Position:</strong>"
    player_info['Position'] = parser.retrieve_in_tags(token, '<', player_page,
                                                      parse=True)

    player_info['Position'] = player_info['Position'].split(')')[0] + ')'

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
    player_info[key] = parser.remove_tokens(player_info[key], ['  ', '\n'])
    player_info[key] = player_info[key].replace('in', '')

    token = 'National Team:</strong>'
    key = 'National Team'
    player_info[key] = parser.retrieve_in_tags(token, '<span', player_page,
                                               parse=True)
    player_info[key] = player_info[key].replace('&nbsp;', '')

    if player_info[key][-1] == ' ':
        player_info[key] = player_info[key][:-1]

    for key in player_info:
        if player_info[key] is None:
            player_info[key] = "None"

    player_page = parser.retrieve_in_tags("<tbody>", "</tbody>", player_page)

    player_info['Matches'] = player_matches(player_page)

    parser.write_file(player_info, header)


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

    token = 'On matchday squad, but did not play'
    invalid_tokens = ['', ' ', 'Match Report']
    matches = []
    for index, play in enumerate(plays):

        plays[index] = parser.retrieve_in_tags('>', '<', play, parse=True)

        plays[index] = list(map(lambda x: x.replace('&ndash;', '-'),
                                plays[index]))

        plays[index] = list(filter(lambda x: x not in invalid_tokens,
                                   plays[index]))

        plays[index] = list(OrderedDict.fromkeys((plays[index])))

        if token not in plays[index]:
            matches.append(plays[index])

    return matches
