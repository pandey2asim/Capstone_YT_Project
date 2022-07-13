import os
from googleapiclient.discovery import build
from googleapiclient import errors
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from dotenv import load_dotenv

load_dotenv()

#five tech channels I love
"""
        Channel Name     Channel ID   
    1.	TechnicalGuruji: UCOhHO2ICt0ti9KAh-QHvttQ
    2.	Unbox Therapy:   UCsTcErHg8oDvUnTzoqsYeNw
    3.	Mkbhd (Mar) :    UCBJycsmduvYEL83R_U4JriQ
    4.	Linus Tech Tips: UCXuqSBlHAE6Xw-yeJA0Tunw
    5.	Coisa de Nerd:   UCuxfOdbKQy0tgGXcm9sjHiw
"""

# Youtube API key and service.
api_key = os.getenv("api_key")
api_version = "v3"
api_service = "youtube"
api_key = f"{api_key}"
# credential and API client
youtube = build(api_service, api_version, developerKey=api_key)

channel_ids = ["UCOhHO2ICt0ti9KAh-QHvttQ",
                 "UCsTcErHg8oDvUnTzoqsYeNw",
                 "UCBJycsmduvYEL83R_U4JriQ",
                 "UCXuqSBlHAE6Xw-yeJA0Tunw",
                 "UCuxfOdbKQy0tgGXcm9sjHiw"
             ]  
# function to plot and save barplots
#function for channel stats
def get_channel_stats(youtube, channel_ids):
    all_channel_stats = []

    try:
        request = youtube.channels().list(
            part="snippet,contentDetails,statistics",
            # if multiple id concatenate ids separated by comma.
            id=",".join(channel_ids)
        )
        response = request.execute()
        print(f'API call successful.')
    except errors.HttpError as err:
        raise Exception(err)

    #iterate through items of interestfor every channel. 
    for item in range(len(response['items'])):
        channel_data_dict = {
            "channel_name": response['items'][item]['snippet']['title'],
            "subscribers": response['items'][item]['statistics']['subscriberCount'],
            "views": response['items'][item]['statistics']['viewCount'],
            "number_of_videos": response['items'][item]['statistics']['videoCount'],
            "playlist_id": response['items'][item]['contentDetails']['relatedPlaylists']['uploads']
        }

        all_channel_stats.append(channel_data_dict)
    print(all_channel_stats)
    # return  all_channel_stats



#function for video details
#visualize data with pandas and seaborn libraries
