# Youtube-Video-Q-A-System


The system builds a python app designed to download, extract, transcribe and analyize audio content from a YouTube video.
Utilized OpenAI Whisper API and LangChain frameworks to help with audio transcriptions and answering relevant questions.


The script simply needs an OPEN AI Key to be inputted in order to work.

'Yt_video_ids' contains the list of youtube videos to download and transcribe.

'download_videos.py' is a helper script to download the youtube videos.
'download_yt_audio.py' is a helper script to download youtube audios.

'YT_QA.py' is the main application which downloads the videos from ids specified in 'Yt_video_ids', transcribes their audio into text,
split text and build vector index using FAISS. Initilalize OpenAI LLM and configure the RetrievalQAWithSourcesChain in order to answer
the required questions along with source videos for the same. 

'short_qa_script.py' is a shorted version of the above script that only parses a fewer number of videos in order to reduce API cost.
