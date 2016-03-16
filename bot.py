import requests
from bs4 import BeautifulSoup
import json
import os
from tokens import tokens
from twython import Twython
import time


def get_data():
    # url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
    url = 'http://www.ncaa.com/scoreboard/basketball-men/d1/2016/03/13'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    return soup.find(id='scoreboard')


def get_date():
    return get_data().find('h2').text.split(',')[1].replace(' ', '')


def parse_row(row):
    team = row.find_all('td', {'class': ['school']})[0].find('a').text.strip()
    score = row.find_all('td', {'class': ['final']})[0].text.strip()
    return team, score


def set_daily_file_path():
    path = 'data/' + get_date() + '.json'
    return os.path.abspath(path)


def read_data(file):
    file_path = file
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            local_data = json.load(f)
    else:
        local_data = {}
    return local_data


def compare_web_and_local_data(web_data, local_data):
    for k, v in web_data.items():
        if k not in local_data:
            local_data[k] = web_data[k]
    return local_data


def get_tokens():
    app_key = tokens['app_key']
    app_secret = tokens['app_secret']
    oauth_token = tokens['oauth_token']
    oauth_token_secret = tokens['oauth_token_secret']
    return Twython(app_key, app_secret, oauth_token, oauth_token_secret)


def pair_teams_with_friends(data):
    path = os.path.abspath('data/_friends.json')
    friend_data = read_data(path)
    for k, v in friend_data.items():
        if k == data:
            if not friend_data[k][2]:
                friend = friend_data[k][0] + ' ' + friend_data[k][1]
                name_first = friend_data[k][0]
                conference = friend_data[k][3]
            else:
                friend = friend_data[k][2]
                name_first = friend_data[k][0]
                conference = friend_data[k][3]
            return friend, name_first, conference


def post_result_sentences(updated_data):
    twitter = get_tokens()
    for k, v in updated_data.items():
        away_team = updated_data[k][0]
        away_score = updated_data[k][1]
        home_team = updated_data[k][2]
        home_score = updated_data[k][3]
        is_posted = updated_data[k][4]
        home_friend = pair_teams_with_friends(home_team)
        away_friend = pair_teams_with_friends(away_team)

        if not is_posted:
            if away_score > home_score:
                if away_friend and home_friend:
                    result = "FINAL: %s (%s) beats %s (%s), %s-%s. %s advances. #FMAA16" % (away_friend[0], away_team, home_friend[0], home_team, away_score, home_score, away_friend[1])
                    # twitter.update_status(status=result)
                    print result
                    time.sleep(2)
                    updated_data[k][4] = True
            else:
                if away_friend and home_friend:
                    result = "FINAL: %s (%s) beats %s (%s), %s-%s. %s advances. #FMAA16" % (home_friend[0], home_team, away_friend[0], away_team, home_score, away_score, home_friend[1])
                    # twitter.update_status(status=result)
                    print result
                    time.sleep(2)
                    updated_data[k][4] = True
    return updated_data


def write_data(final_data):
    file_path = set_daily_file_path()
    with open(file_path, 'w') as f:
        json.dump(final_data, f, indent=4, separators=(',', ': '))


def main():
    web_data = {}
    is_posted = False
    for game in get_data().find_all('section', class_='game'):
        if game.find('div', class_='final') is None:
            continue
        key = game['id'].split('/')[-1]
        away_team, away_score = parse_row(game.find_all('tr')[1])
        home_team, home_score = parse_row(game.find_all('tr')[2])
        web_data[key] = [away_team, away_score, home_team, home_score, is_posted]

    local_data = read_data(set_daily_file_path())
    updated_data = compare_web_and_local_data(web_data, local_data)
    final_data = post_result_sentences(updated_data)
    write_data(final_data)


if __name__ == '__main__':
    main()
