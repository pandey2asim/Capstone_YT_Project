import os
from googleapiclient.discovery import build
from googleapiclient import errors
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams

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
#function for video details
#visualize data with pandas and seaborn libraries
