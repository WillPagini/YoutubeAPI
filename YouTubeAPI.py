#import libraries
import requests
import pandas
import time
import numpy

#Set Auth keys provided by youtube
API_key = 'xxx'
Channel_ID = 'xxx'
pageToken= ""

def getStats(video_id):
  url_stats = 'https://www.googleapis.com/youtube/v3/videos?key='+API_key+"&id="+video_id+"&part=statistics&maxResults=10000"+pageToken
  response_stats = requests.get(url_stats).json()
  viewCount = response_stats['items'][0]['statistics']['viewCount']
  likeCount = response_stats['items'][0]['statistics']['likeCount']
  commentCount = response_stats['items'][0]['statistics']['commentCount']

  return viewCount, likeCount, commentCount

def get_videos(df):

  #Make API Channel Call

  url = 'https://www.googleapis.com/youtube/v3/search?key='+API_key+"&channelId="+Channel_ID+"&part=snippet,id&order=date&maxResults=10000"+pageToken
  response = requests.get(url).json()

  time.sleep(1)

  # Iterates over json from API
  for video in response['items']:
    if video['id']['kind'] == 'youtube#video':
      video_id = video['id']['videoId']
      video_title = video['snippet']['title']
      video_title = str(video_title).replace("&amp;", "")
      upload_date = video['snippet']['publishedAt']
      upload_date = str(upload_date). split("T")[0]

      view_count, like_count, comment_count = getStats(video_id)

      df =df.append({'video_id':video_id, 'video_title':video_title,
                    'upload_date':upload_date, 'view_count': view_count,
                    'like_count':like_count, 'comment_count': comment_count}, ignore_index=True)
  return df

df = pandas.DataFrame(columns=['video_id', 'video_title', 'upload_date', 'view_count', 'like_count', 'comment_count'])
df = get_videos(df)

df.info()
#Formating datatype fields
df['video_id'] = df['video_id'].astype(str)
df['video_title'] = df['video_title'].astype(str)
df['upload_date'] = df['upload_date'].astype('datetime64[D]')
df['view_count'] = df['view_count'].astype(numpy.int64)
df['like_count'] = df['like_count'].astype(numpy.int64)
df['comment_count'] = df['comment_count'].astype(numpy.int64)

#Exports to CSV extention
df.to_csv('youtube_vids_stats.csv')