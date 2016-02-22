import requests
from bs4 import BeautifulSoup
import json
import os


def get_data():
    url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
    return soup.find(id='scoreboard')


def get_date():
    return get_data().find('h2').text.split(',')[1].replace(' ', '')


def parse_row(row):
    team = row.find_all('td', {'class': ['school']})[0].find('a').text.strip()
    score = row.find_all('td', {'class': ['final']})[0].text.strip()
    return team, score


def write_data(web_data):
    file_path = 'data/' + get_date() + '.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            local_data = json.load(f)
    else:
        local_data = {}

    for k, v in web_data.items():
        if k not in local_data:
            local_data[k] = web_data[k]

    with open(file_path, 'w') as f:
        json.dump(local_data, f, indent=4, separators=(',', ': '))


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

    write_data(results)


if __name__ == '__main__':
    main()
