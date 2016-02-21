import requests
from bs4 import BeautifulSoup
import json
import os
# from twython import Twython, TwythonError
# import time

# url = 'http://www.ncaa.com/scoreboards/basketball-men/d1'
url = 'http://www.ncaa.com/scoreboard/basketball-men/d1/2016/02/14'
response = requests.get(url)
html = response.content
soup = BeautifulSoup(html, 'lxml')
scoreboard = soup.find(id='scoreboard')

dict_of_games = {}
is_posted = False

# --- Iterate and scrape data for games that are final.
for game in scoreboard.find_all('section', class_='game'):
    if game.find('div', class_='final') is None:
        continue
    game_id = game['id']
    key = game_id.split('/')[-1]  # --- Split at the last slash.
    # --- Each dict has a key of the id scraped from the table.
    dict_of_games[key] = {
        'away': {
            'team': None,
            'score': None
        },
        'home': {
            'team': None,
            'score': None
        },
        'is_posted': False
    }
    rows = game.find_all('tr')
    for row in rows:
        cells = row.find_all('td', {'class': ['school', 'final']})
        if rows.index(row) == 1:  # --- Index 1 is away team.
            for cell in cells:
                if 'school' in cell.attrs['class']:
                    team = cell.find('a').text.strip()
                    dict_of_games[key]['away']['team'] = team
                elif 'final' in cell.attrs['class']:
                    score = cell.text.strip()
                    dict_of_games[key]['away']['score'] = score
        elif rows.index(row) == 2:  # --- Index 2 is home team.
            for cell in cells:
                if 'school' in cell.attrs['class']:
                    team = cell.find('a').text.strip()
                    dict_of_games[key]['home']['team'] = team
                elif 'final' in cell.attrs['class']:
                    score = cell.text.strip()
                    dict_of_games[key]['home']['score'] = score

file_path = 'data/data.json'
# --- If there is no data in the JSON file, create a new one.
if os.stat(file_path).st_size == 0:
    with open(file_path, 'wb') as f:
        json.dump(dict_of_games, f, indent=4, separators=(',', ': '))
        print "New JSON file started."
else:
    with open(file_path, 'rb+') as f:
        saved_dict = json.load(f)
        for item in dict_of_games.keys():
            if item in saved_dict:
                dict_of_games.pop(item, None)
        # --- If there are new game results, add them to the file.
        if dict_of_games:
            new_items = json.dumps(dict_of_games).replace('{', ',', 1)
            f.seek(-2, 2)  # --- Move backward to add items inside {}
            f.write(new_items)
            print "New results added to JSON file."
        # --- Otherwise, don't change the file.
        else:
            print "Nothing new right now."

# # # --- Authorize Friendship Mad-Bot app under @FriendMadness.
# # app_key = '7K0AIkrAiIC5CblaZrAwfsm3e'
# # app_secret = 'l52lRFrTDpv2jx02CmGChvm8M6fnybp6kFqwUj20DZpDLdYQ3V'
# # oauth_token = '1263138942-YjCL0CXIw48ADkGI9rQ5PuE4ExFldXdrByHc60q'
# # oauth_token_secret = '4pWuKAaOYl04qMQwNGvwtjeWhn6ndkcDI5YXNRAwF3kac'

# # twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

# # while True:
# #     try:
# #         i = 0
# #         if len(list_of_winners) > 0:
# #             tweet = list_of_winners[i]
# #             # # twitter.update_status(status=tweet)
# #             print tweet
# #             i += 1
# #             list_of_winners.remove(tweet)
# #             time.sleep(1)
# #         else:
# #             print "More FMAA updates soon!"
# #             break
# #     except TwythonError as e:
# #         print e

# # print list_of_winners
