import requests
from bs4 import BeautifulSoup
import json
import os


def get_data():
    url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
    # url = 'http://www.ncaa.com/scoreboard/basketball-men/d1/2016/02/14'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    return soup.find(id='scoreboard')


def get_date():
    date = get_data().find('h2').text.split(',')[1].replace(' ', '')
    return date


def parse_row(row):
    team = row.find_all('td', {'class': ['school']})[0].find('a').text.strip()
    score = row.find_all('td', {'class': ['final']})[0].text.strip()
    return team, score


def compare_dicts(results):
    file_path = 'results/' \
        + get_date() + '.json'
    if os.path.exists(file_path):
        with open(file_path, 'r+') as f:
            saved_dict = json.load(f)
            for key in saved_dict:
                if key in results:
                    del results[key]
            if results:
                updated_dict = saved_dict.copy()
                updated_dict.update(results)
                f.seek(0)
                json.dump(updated_dict, f)
                print "New results to add."
            else:
                print "Nothing new right now."
    else:
        with open(file_path, 'w') as f:
            json.dump(results, f)
            print "New JSON file started."


def main():
    results = {}
    is_posted = False
    for game in get_data().find_all('section', class_='game'):
        if game.find('div', class_='final') is None:
            continue
        key = game['id'].split('/')[-1]
        away_team, away_score = parse_row(game.find_all('tr')[1])
        home_team, home_score = parse_row(game.find_all('tr')[2])
        results[key] = [away_team, away_score,
                        home_team, home_score,
                        is_posted]

    compare_dicts(results)


if __name__ == '__main__':
    main()
