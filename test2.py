import requests
from bs4 import BeautifulSoup
import csv
import os

# url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
url = 'http://www.ncaa.com/scoreboard/basketball-men/d1/2016/02/14'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'lxml')
scoreboard = soup.find(id='scoreboard')

# Iterate and scrape data for games that are final.
list_of_games = []
add_id = 1
is_posted = False
games = scoreboard.find_all('section', class_='game')
for game in games:
    if game.find('div', class_='final') is None:
        continue
    game_id = game['id'].replace('gamecenter-/game/basketball-men/d1/2016/', '')
    list_of_rows = []
    rows = game.find_all('tr')[1:]
    for row in rows:
        list_of_cells = []
        cells = row.find_all('td', {'class': ['school', 'final']})
        for cell in cells:
            if 'school' in cell.attrs['class']:
                team = cell.find('a').text
                list_of_cells.append(team)
            elif 'final' in cell.attrs['class']:
                score = cell.text
                list_of_cells.append(score)
        list_of_rows.append(list_of_cells)
    list_of_rows.insert(0, add_id)
    list_of_rows.insert(1, is_posted)
    list_of_rows.append(game_id)
    list_of_games.append(list_of_rows)
    add_id += 1
    # print list_of_rows


file_path = 'csv/test2.csv'
try:
    if os.stat(file_path).st_size == 0:
        f = open(file_path, 'wb')
        writer = csv.writer(f)
        writer.writerows(list_of_games)
    else:
        f = open(file_path, 'rb+')
        reader = csv.reader(f)
        for game in list_of_games:
            x = game[-1]
            for line in reader:
                y = line[-1]
                if x == y:
                    print True
                else:
                    continue
                print line
            print game

except OSError as e:
    print e
