import os
import pytube
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from moviepy.editor import *

SAVE_PATH = "<insert_save_path>"

link=open('Yt_video_ids', 'r')
d_counter = 0

for id in link:
  yt_url = "https://www.youtube.com/watch?v=" + id;
  print("Downloading : ", yt_url)

  try:
    yt = YouTube(yt_url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    print(yt.streams.filter(only_audio=True).first())
  except pytube.exceptions.VideoUnavailable:
    print("Video : ", yt_url, " is unavaialable, skipping.")
    continue

  # try: 
  # downloading the audio
  audio_stream.download(SAVE_PATH)
  d_counter+=1
  print("Downloaded ", yt_url)
  # Convert to mp3
  # audio_path = os.path.join(SAVE_PATH, audio_stream.default_filename)
  # audio_clip = AudioFileClip(audio_path)
  # audio_clip.write_audiofile(os.path.join(SAVE_PATH, f"{audio_stream.default_filename}.mp3"))
  # break
  # except:
  #   print("Some Error in Downloading: ", yt_url) 
  

print("Downloaded ", str(d_counter), " streams")


# You can find the unprocessed caption file (i.e. with stop words) here: https://www.rocq.inria.fr/cluster-willow/amiech/howto100m/raw_caption.zip
