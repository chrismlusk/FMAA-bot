import csv
import requests
from bs4 import BeautifulSoup

url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
response = requests.get(url)
html = response.content

soup = BeautifulSoup(html, 'lxml')
scoreboard = soup.find(id='scoreboard')
games = scoreboard.find_all('section', class_='game')

# Build a list of final results with teams and scores.
list_of_games = []
for game in games:
    if game.find('div', class_='final') is None:
        continue
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
    list_of_games.append(list_of_rows)

# Determine the winner and create update sentence.
list_of_winners = []
i = 0
tag = list_of_games
for game in tag:
    if tag[i][0][1] > tag[i][1][1]:
        x = ["FINAL: " + tag[i][0][0] + " " + tag[i][0][1] + ", " + tag[i][1][0] + " " + tag[i][1][1] + ". #fmaa16"]
        list_of_winners.append(x)
    else:
        x = ["FINAL: " + tag[i][1][0] + " " + tag[i][1][1] + ", " + tag[i][0][0] + " " + tag[i][0][1] + ". #fmaa16"]
        list_of_winners.append(x)
    i += 1


with open('csv/test.csv', 'wb') as f:
    writer = csv.writer(f)
    # writer.writerow([
    #                     "away_team"
    #                 ])
    writer.writerows(list_of_winners)
