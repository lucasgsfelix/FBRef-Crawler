""" Return a player statistics from FBRef. """
import re
import parser
from collections import OrderedDict


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
    player_info['Position'] = parse_position(player_info['Position'])

    player_info['Position'] = player_info['Position'].replace('\n', '')

    token = 'Footed:</strong>'
    player_info['Foot'] = parser.retrieve_in_tags(token, '<', player_page,
                                                  parse=True)
    player_info['Foot'] = player_info['Foot']

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

    player_info = replace_none(player_info)

    player_page = parser.retrieve_in_tags("<tbody>", "</tbody>", player_page)

    matches_info = player_matches(player_page)

    player_info['Matches'] = matches_info

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

    token_match = 'On matchday squad, but did not play'
    invalid_tokens = ['', ' ', 'Match Report', 'Away', 'Home']
    matches = []

    for index, play in enumerate(plays):

        match_info = {}
        token = r'href="/en/matches/.*?">'
        match_info['Date'] = parser.retrieve_in_tags(token, '<', play)[0]
        token = r'data-stat="dayofweek".*?>'
        match_info['Day'] = parser.retrieve_in_tags(token, '<', play)[0]

        # That is the competition
        token = r'href="/en/comps/.*?>'
        results = parser.retrieve_in_tags(token, '<', play)
        if len(results) == 1:
            match_info['Comp.'] = None
            match_info['Round'] = results[0]
        else:
            match_info['Comp.'] = results[0]
            match_info['Round'] = results[1]


        #print([(a.end()) for a in list(re.finditer(token, play))])
        if token_match in play:
            continue

        token = r'data-stat="result".*?>'
        match_info['Result'] = parser.retrieve_in_tags(token, '<', play)
        match_info['Result'] = match_info['Result'][0].replace('&ndash;', '-')

        token = r'href="/en/squads/.*?>'
        results = parser.retrieve_in_tags(token, '<', play)
        match_info['Squad'] = results[0]
        match_info['Oponent'] = results[1]

        token = r'data-stat="game_started".*?>'
        match_info['Start'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="minutes".*?>'
        match_info['Min. Played'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="goals".*?>'
        match_info['Goals'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="assists".*?>'
        match_info['Assist.'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="shots_total".*?>'
        match_info['Shots'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="shots_on_target".*?>'
        match_info['Sh. On Target.'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="crosses".*?>'
        match_info['Crosses'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="fouled".*?>'
        match_info['Fouls Drawn'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="pens_made".*?>'
        match_info['Pen. Kicks'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="pens_att".*?>'
        match_info['PK attempt'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="tackles_won".*?>'
        match_info['Tackles Won'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="interceptions".*?>'
        match_info['Interceptions'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="fouls".*?>'
        match_info['Fouls Commited'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="cards_yellow".*?>'
        match_info['Yellow C.'] = parser.retrieve_in_tags(token, '<', play)[0]

        token = r'data-stat="cards_red".*?>'
        match_info['Red C.'] = parser.retrieve_in_tags(token, '<', play)[0]

        for key in match_info.keys():
            if match_info[key] is not None and '<' in match_info[key]:
                match_info[key] = 0

        matches.append(match_info)

    return matches


def parse_position(position):
    """ Parse position feature of a player"""

    position = position.replace('&nbsp;&#9642;&nbsp;', '')
    if ')' in position:
        position = position.split(')')[0] + ')'
        if ' &amp; ' in position:
            position = position.replace(' &amp; ', '')
    else:
        position = re.sub(r'^[A-Z] ', '', position)

    return position


def replace_none(player_info):
    """ Replace None values in the players information"""

    for key in player_info:
        if player_info[key] is None:
            player_info[key] = "None"

    return player_info
