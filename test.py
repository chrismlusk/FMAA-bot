import requests
from bs4 import BeautifulSoup
import csv
from twython import Twython, TwythonError

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

# # Dump game data into a csv.
# file_path = 'csv/test.csv'
# with open(file_path, 'wb') as f:
#     writer = csv.writer(f)
#     writer.writerows(list_of_games)

# Determine winners and write game results.
list_of_winners = []
for row in list_of_games:
    if not row[1]:
        h_team = row[3][0]
        a_team = row[2][0]
        h_score = row[3][1]
        a_score = row[2][1]
        list_of_sentences = []
        if h_score > a_score:
            update = "%s beats %s, %s-%s. %s advances!" % (h_team, a_team, h_score, a_score, h_team)
            list_of_sentences.append(update)
            row[1] = True
        else:
            update = "%s beats %s, %s-%s. %s advances!" % (a_team, h_team, a_score, h_score, a_team)
            list_of_sentences.append(update)
    list_of_winners.append(list_of_sentences)

# print list_of_winners

# Dump sentences into a new csv.
file_path = 'csv/test-results.csv'
with open(file_path, 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(list_of_winners)

# # Authorize Friendship Mad-Bot app under @FriendMadness.
# app_key = '7K0AIkrAiIC5CblaZrAwfsm3e'
# app_secret = 'l52lRFrTDpv2jx02CmGChvm8M6fnybp6kFqwUj20DZpDLdYQ3V'
# oauth_token = '1263138942-YjCL0CXIw48ADkGI9rQ5PuE4ExFldXdrByHc60q'
# oauth_token_secret = '4pWuKAaOYl04qMQwNGvwtjeWhn6ndkcDI5YXNRAwF3kac'

# twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

# while True:
#     try:
#         i = 0
#         if len(list_of_winners) > 0:
#             tweet = list_of_winners[i]
#             # # twitter.update_status(status=tweet)
#             print tweet
#             i += 1
#             list_of_winners.remove(tweet)
#             time.sleep(1)
#         else:
#             print "More FMAA updates soon!"
#             break
#     except TwythonError as e:
#         print e

# print list_of_winners
