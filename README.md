# Youtube-Video-Q-A-System


The system builds a Python app designed to download, extract, transcribe and analyze audio content from a YouTube video.
Utilized OpenAI Whisper API and LangChain frameworks to help with audio transcriptions and answering relevant questions.


The script simply needs an OPEN AI Key to be inputted in order to work.

'Yt_video_ids' contains the list of YouTube videos to download and transcribe. The list has been taken from HowTo100M instructional
video dataset.

'download_videos.py' is a helper script for downloading YouTube videos.
'download_yt_audio.py' is a helper script to download YouTube audios.

'YT_QA.py' is the main application that downloads the videos from ids specified in 'Yt_video_ids', transcribes their audio into text,
splits the text, and builds the vector index using FAISS. Finally, it configures the RetrievalQAWithSourcesChain with the OpenAI LLM in
order to answer the required questions along with source videos for the same. 

'short_qa_script.py' is a shorter version of the above script that only parses a fewer number of videos in order to reduce API cost.

Required libraries : pip install openai faiss-cpu moviepy pytube3 langchain tiktoken 
