import os
from googleapiclient.discovery import build
from googleapiclient import errors
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
from dotenv import load_dotenv

load_dotenv()

def main():
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

#print(api_key)
# credential and API client
youtube = build(api_service, api_version, developerKey=api_key)

channel_ids = ["UCOhHO2ICt0ti9KAh-QHvttQ",
                 "UCsTcErHg8oDvUnTzoqsYeNw",
                 "UCBJycsmduvYEL83R_U4JriQ",
                 "UCXuqSBlHAE6Xw-yeJA0Tunw",
                 "UCuxfOdbKQy0tgGXcm9sjHiw"
             ]  
# function to plot and save barplots
def save_barplot(x_axis, y_axis, data, filename):

    # sns.set(rc={'figure.figsize':(24,10)})
    sns.set(style="whitegrid") 
    fig, ax = plt.subplots(figsize=(20,10))
    rcParams.update({'figure.autolayout': True})
    plt.ticklabel_format(style = 'plain')
    plt.xticks(size=14)
    plt.yticks(size=14)
    sns.barplot(x=x_axis, y=y_axis, data=data)

    plt.savefig(f'{filename}', dpi=360, bbox_inches='tight')
    
    plt.clf()

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
    # print(all_channel_stats)
    return  all_channel_stats

#create pandas dataframe from channel stats data. Returns a dataframe
def channel_stats_to_df(channel_stats):
    df = pd.DataFrame(channel_stats)
    df['subscribers'] = pd.to_numeric(df['subscribers'])
    df['views'] = pd.to_numeric(df['views'])
    df['number_of_videos'] = pd.to_numeric(df['number_of_videos'])
    print(f'DF datatypes: {df.dtypes}')

    return df

## Get video data
def get_video_ids(youtube, playlist_id):
    
    request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId = playlist_id,
                maxResults = 50)
    response = request.execute()
    
    video_ids = []
    
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                        part='contentDetails',
                        playlistId = playlist_id,
                        maxResults = 50,
                        pageToken = next_page_token)
            response = request.execute()
    
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            
            next_page_token = response.get('nextPageToken')
        
    return video_ids

def get_video_details(youtube, video_ids):
    all_video_stats = []
    
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
                    part='snippet,statistics',
                    id=','.join(video_ids[i:i+50]))
        response = request.execute()
        
        for video in response['items']:
            
            Dislikes = 0
            Comments = 0
            Likes = 0 
            Views = 0
            if 'dislikeCount' in video['statistics'].keys():
                Dislikes = video['statistics']['dislikeCount']
            if 'commentCount' in video['statistics'].keys():
                Comments = video['statistics']['commentCount'] 
            if 'likeCount' in video['statistics'].keys():
                Likes = video['statistics']['likeCount']   
            if 'viewCount' in video['statistics'].keys():
                Views = video['statistics']['viewCount'] 


            video_stats = dict(Title = video['snippet']['title'],
                               Published_date = video['snippet']['publishedAt'],
                               Views = Views,
                               Likes = Likes,
                               Dislikes = Dislikes,
                               Comments = Comments
                               )
            all_video_stats.append(video_stats)
    
    return all_video_stats

#function to get all video stats from all channel stats
def get_all_video_stats(channel_stats):

    video_stats_df = pd.DataFrame(columns=['Title', 'Published_date', 'Views', 'Likes', 'Dislikes', 'Comments', 'channel_name', 'playlist_id'])

    for item in channel_stats:
        video_ids = get_video_ids(youtube, item['playlist_id'])
        video_stats = get_video_details(youtube, video_ids)

        df2 = pd.DataFrame(video_stats, columns=['Title', 'Published_date', 'Views', 'Likes', 'Dislikes', 'Comments', 'channel_name', 'playlist_id'])
        df2['channel_name'] = item['channel_name']
        df2['playlist_id'] = item['playlist_id']

        df2['Published_date'] = pd.to_datetime(df2['Published_date']).dt.date
        df2['Views'] = pd.to_numeric(df2['Views'])
        df2['Likes'] = pd.to_numeric(df2['Likes'])
        df2['Dislikes'] = pd.to_numeric(df2['Dislikes'])

        video_stats_df = video_stats_df.append(df2, ignore_index=True)

    return video_stats_df


#Block to fetch and plot channel data.
#Fetch youtube channel data from API.
channel_stats = get_channel_stats(youtube, channel_ids)

# Create a dataframe from the fetched youtube data.
channel_stats_df = channel_stats_to_df(channel_stats) 

# Save barplots as images
save_barplot('channel_name', 'views', channel_stats_df, 'views_by_channe.png')
save_barplot('channel_name', 'subscribers', channel_stats_df, 'subscribers_by_channel.png')
save_barplot('channel_name', 'number_of_videos', channel_stats_df, 'videos_by_channel.png')

# Block to fetch and plot video stats data
all_video_stats = get_all_video_stats(channel_stats)
print(all_video_stats)
top_10_videos = all_video_stats.sort_values(by='Views', ascending=False).head(10)

# bar plot top 10 videos
save_barplot('Views', 'Title', top_10_videos, 'top_10_videos_by_views.png')
#save_barplot('Views', 'channel_name', top_10_videos, 'top_10_videos_by_views_channel.png')

if __name__ == "__main__":
    main()



