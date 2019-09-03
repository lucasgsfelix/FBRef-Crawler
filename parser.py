""" Resposible to parse the tables from FBRef. """
import os


def match_logs_link(player_id, season, player_name):
    """ Return the page with all matches from a season log."""

    link = "https://fbref.com/en/players/" + player_id + '/'
    link += "matchlogs/" + season + '/' + player_name.replace(' ', '-')
    return link + '-Match-Logs'


def get_page(link):
    """ Given a link it return the html page. """
    os.system('wget -O auxiliary.html ' + link + " --quiet")
    with open('auxiliary.html', 'r') as file:
        info = file.read()

    os.system('rm auxiliary.html')
    return info


def soccer_season(season):
    """ Given a season return in soccer format season"""
    return str(season) + '-' + str(season+1)
