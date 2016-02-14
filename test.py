import requests
from bs4 import BeautifulSoup
# import csv
from twython import Twython, TwythonError
import time

# url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
url = 'http://www.ncaa.com/scoreboard/basketball-men/d1/2016/02/12'
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

list_of_winners = []
for row in list_of_games:
    h_team = row[1][0]
    a_team = row[0][0]
    h_score = row[1][1]
    a_score = row[0][1]
    if h_score > a_score:
        update = "%s beats %s, %s-%s. %s advances!" % (h_team, a_team, h_score, a_score, h_team)
    else:
        update = "%s beats %s, %s-%s. %s advances!" % (a_team, h_team, a_score, h_score, a_team)
    list_of_winners.append(update)

# Authorize Friendship Madness app.
app_key = 'bfzIzp6FRmUChOFfujhvLwISE'
app_secret = 'VoSkGgcJD29QlOCQmVyFtv7KxgwYYunuUSqUEh1zqB7IgnAj4Z'
oauth_token = '21734466-gy5DbrVqB5V8H7pImfdMS17UIj3EHQkdRDDysO2Pq'
oauth_token_secret = 'KOcMn6Zw9vrKTqoLG9SMUkocmENDlQybW4VYULqHEgl0B'

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

while True:
    try:
        i = 0
        if len(list_of_winners) > 0:
            tweet = list_of_winners[i]
            # twitter.update_status(status=tweet)
            print tweet
            i += 1
            list_of_winners.remove(tweet)
            time.sleep(1)
        else:
            print "More FMAA updates soon!"
            break
    except TwythonError as e:
        print e

print list_of_winners
