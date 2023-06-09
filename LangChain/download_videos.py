import os
import pytube
from pytube import YouTube
from urllib.parse import urlparse, parse_qs

SAVE_PATH = "/Users/chitti.ankith/Desktop/videos/"

link=open('Yt_video_ids', 'r')
d_counter = 0

for id in link:
  yt_url = "https://www.youtube.com/watch?v=" + id;
  print("Downloading : ", yt_url)

  try:
    yt = YouTube(yt_url)
    mp4file = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[0]
    print(yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[0])
  except pytube.exceptions.VideoUnavailable:
    print("Video : ", yt_url, " is unavaialable, skipping.")
    continue

  try: 
    # downloading the video 
    mp4file.download(SAVE_PATH)
    d_counter+=1
    print("Downloaded ", yt_url)
  except:
    print("Some Error in Downloading: ", yt_url) 
  

print("Downloaded ", str(d_counter), " videos")