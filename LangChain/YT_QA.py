import os
import pytube
from pytube import YouTube
from pympler import asizeof
from urllib.parse import urlparse, parse_qs
from moviepy.editor import *
os.environ["OPENAI_API_KEY"] = "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"

import openai
import time

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.chains import RetrievalQAWithSourcesChain
from langchain import OpenAI
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA

SAVE_PATH = "/Users/chitti.ankith/Desktop/LangChain/audios/"

start_time = time.time()

link=open('Yt_video_ids', 'r')
d_counter = 0

# for id in link:
#   yt_url = "https://www.youtube.com/watch?v=" + id;
#   print("Downloading : ", yt_url)

#   try:
#     yt = YouTube(yt_url)
#     audio_stream = yt.streams.filter(only_audio=True).first()
#     print(yt.streams.filter(only_audio=True).first())
#   except pytube.exceptions.VideoUnavailable:
#     print("Video : ", yt_url, " is unavaialable, skipping.")
#     continue

#   audio_stream.download(SAVE_PATH)
#   d_counter+=1
#   print("Downloaded ", yt_url)
  
# print("Downloaded ", str(d_counter), " streams")

download_end_time = time.time()
print("Downloading streams took ", str(download_end_time - start_time))

files = sorted(os.listdir(SAVE_PATH))

transcripts = []

# Transcribe audio to text
for file in files:
  audio_path = os.path.join(SAVE_PATH, file)
  audio_file= open(audio_path, "rb")
  print(audio_path)
  try :
    transcripts.append(openai.Audio.transcribe("whisper-1", audio_file))
  except:
    continue

transcibe_end_time = time.time()
print("Transcribing text took ", str(transcibe_end_time - download_end_time))
print("Transcripts size : ", asizeof.asizeof(transcripts))

# Splitting the text and creating the docs.
textsplitter = CharacterTextSplitter(chunk_size=512, chunk_overlap=0)
split_end_time = time.time()
print("Splitting text took ", str(split_end_time - transcibe_end_time))

texts = textsplitter.create_documents([transcript.text for transcript in transcripts], metadatas=[{"source" : file} for file in files])
doc_end_time = time.time()
print("Creating docs took ", str(doc_end_time - split_end_time))
print("Docs size : ", asizeof.asizeof(texts))

# Create the vector store index using FAISS.
store = FAISS.from_documents(texts, OpenAIEmbeddings())
store_end_time = time.time()
print("Vector Store Index size : ", asizeof.asizeof(store))
print("Creating vector store took ", str(store_end_time - doc_end_time))

# Create the LLM QA Chain
llm = OpenAI(temperature=0)
chain = RetrievalQAWithSourcesChain.from_chain_type(
    llm=llm, chain_type="refine", retriever=store.as_retriever()
)
chain_end_time = time.time()
print("Creating QA Chain took ", str(chain_end_time - store_end_time))

# Sample list of questions to ask. Generated using OpenAI
questions = [
  "Who was Howard Thurston?",
  "How does the Aero Garden Seed Pod Kit work?",
  "What are the ingredients for making Blueberry Muffins with Crumb Topping?",
  "What is the recipe for Canh Rau Muong (Vietnamese Water Spinach Soup)?",
  "How do you make a DIY Homemade Exfoliating Peppermint Sugar Body Scrub?",
  "What is the process for creating a DIY Mesh Water Ring Sling?",
  "What are the instructions for using the EASY Sleepy Wrap (baby wrap)?",
  "How do you make Ravioli Soup with Zucchini and Spinach?",
  "What are the instructions for using the Eco Cub Baby Wrap Carrier for newborns?",
  "How do you make Fresh Peach Muffins?",
  "What are the steps to seed start German Chamomile indoors for garden flowers?",
  "What are the steps for custom painting a motorcycle?",
  "How do you perform the Card from Thin Air trick in coin and card magic?",
  "What are the tips for growing Basil?",
  "How do you make an origami balloon?",
  "How do you make an origami balloon frog? (Part 2)",
  "What is the process for making an origami glass?",
  "How do you build an outdoor jungle gym?",
  "How do you paint a motorcycle gas tank?",
  "What are the steps for painting a motorcycle?",
  "How do you perform a basecoat prep for painting a motorcycle?",
  "What is the process for Plasti Dipping motorcycle rims?",
  "How do you produce a Half Dollar from a napkin in coin tricks?",
  "How do you recharge the AC system on an AUDI A4 B6?",
  "What are the steps for setting up a primitive slackline?",
  "How do you tie a moby wrap?",
  "How do you wear your baby using a baby wrap or Moby?",
  "What is the tutorial for the Incredible Coin Through Table magic trick?",
  "How do you position a newborn in the JJ Cole Agility Baby Carrier?",
  "What is the technique for maintaining balance in slacklining?",
  "How can you protect a motorcycle tank bag with paint?",
  "How do you create a window herb garden with Burpee Seeds?",
  "What are the folding instructions for an Origami Balloon?",
  "How do you make an Origami Iris (Lily version 2)?",
  "How do you make an Origami Mikan and Kotatsu for display?",
  "What are the beginner tips for setting up a Play Line in slacklining?",
  "How can you create a pop-up poster presentation?",
  "What is the process for recharging a car air conditioner in a Ford Taurus?",
  "How does the Shaffali Pineapple + Peppermint Exfoliant detoxify the skin and spirit?",
  "What are the tips for slacklining in a room?",
  "How do you set up a slackline and what are some helpful tips?"
]

for question in questions:
  print(question)
  st = time.time()
  print(chain({"question": question}))
  print("Time ", str(time.time() - st))

end_time = time.time()

print("Answering all questions took ", str(end_time - chain_end_time))
print("Total time taken ", str(end_time - start_time))
