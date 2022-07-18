from project import get_channel_stats
from project import save_barplot
import os
from googleapiclient.discovery import build
from googleapiclient import errors
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from dotenv import load_dotenv

load_dotenv()


api_version = "v3"
api_service = "youtube"
api_key = os.getenv("api_key")
api_key = f"{api_key}"
# credential and API client
youtube = build(api_service, api_version, developerKey=api_key)

channel_ids = ["UCOhHO2ICt0ti9KAh-QHvttQ",
               "UCsTcErHg8oDvUnTzoqsYeNw",
               "UCBJycsmduvYEL83R_U4JriQ",
               "UCXuqSBlHAE6Xw-yeJA0Tunw",
               "UCuxfOdbKQy0tgGXcm9sjHiw"
               ]


answer = [{'channel_name': 'Technical Guruji', 'subscribers': '22200000', 'views': '3042392178', 
'number_of_videos': '4574', 'playlist_id': 'UUOhHO2ICt0ti9KAh-QHvttQ'}, 
{'channel_name': 'Linus Tech Tips', 'subscribers': '14700000', 'views': '5975361049', 
'number_of_videos': '5833', 'playlist_id': 'UUXuqSBlHAE6Xw-yeJA0Tunw'}, 
{'channel_name': 'Marques Brownlee', 'subscribers': '15800000', 'views': '3052148676', 'number_of_videos': '1448', 'playlist_id': 'UUBJycsmduvYEL83R_U4JriQ'}, 
{'channel_name': 'Coisa de Nerd', 'subscribers': '11000000', 'views': '3413411728', 'number_of_videos': '1961', 'playlist_id': 'UUuxfOdbKQy0tgGXcm9sjHiw'},
 {'channel_name': 'Unbox Therapy', 'subscribers': '18200000', 'views': '4320359100', 'number_of_videos': '2047', 'playlist_id': 'UUsTcErHg8oDvUnTzoqsYeNw'}]

def test_get_channel_stats():
    try:
        assert get_channel_stats(youtube, channel_ids) == answer
    except AssertionError:
        print('error')

def test_save_barplot():
    try:
        assert save_barplot(plt.x_axis, plt.y_axis, plt.data, plt.filename) == True
    except AttributeError:
        print('error')


