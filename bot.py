# # # --- experimenting with twitter bots --- # # #

from twython import Twython, TwythonError
import time
import csv

# Authorize Friendship Mad-Bot app under @FriendMadness.
app_key = '7K0AIkrAiIC5CblaZrAwfsm3e'
app_secret = 'l52lRFrTDpv2jx02CmGChvm8M6fnybp6kFqwUj20DZpDLdYQ3V'
oauth_token = '1263138942-YjCL0CXIw48ADkGI9rQ5PuE4ExFldXdrByHc60q'
oauth_token_secret = '4pWuKAaOYl04qMQwNGvwtjeWhn6ndkcDI5YXNRAwF3kac'

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret)

# # # --- BASIC STATUS
# line = "This is an automated message from the friendliest organization in sports."
# twitter.update_status(status=line)

# # --- SEARCH QUERIES
# search_results = twitter.search(q='sooners', count=5)
# try:
#     for tweet in search_results["statuses"]:
#         twitter.retweet(id=tweet["id_str"])
# except TwythonError as e:
#     print e

# # # --- FILTERING SEARCH QUERIES
# exclude = ["Jayhawks", "Boomer", "LOL"]
# include = ["sooners", "OU"]
# search_for = " OR ".join(include)
# blacklist = " -".join(exclude)
# keywords = search_for + blacklist
# results = twitter.search(q=keywords, count=1)
# try:
#     for tweet in results["statuses"]:
#         try:
#             print tweet
#         except TwythonError as e:
#             print e
# except TwythonError as e:
#     print e


# # # --- POSTING FROM TXT FILE
# path = 'csv/test.csv'
# try:
#     with open(path, 'r+') as f:
#         buff = f.readlines()

#     for line in buff[:]:
#         line = line.strip(r'\n')
#         if len(line) <= 140 and len(line) > 0:
#             # twitter.update_status(status=line)
#             print line
#             with open(path, 'w') as f:
#                 buff.remove(line)
#                 f.writelines(buff)
#             time.sleep(10)
#         else:
#             with open(path, 'w') as f:
#                 buff.remove(line)
#                 f.writelines(buff)
#             print ("Skipped! Char length violation.")
#             continue
#         # print ("Next line...")

# except TwythonError as e:
#     print (e)
