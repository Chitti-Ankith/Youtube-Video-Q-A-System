import os
import pytube
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
from moviepy.editor import *
from pympler import asizeof

os.environ["OPENAI_API_KEY"] = "<insert_save_path>"
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

  audio_stream.download(SAVE_PATH)
  d_counter+=1
  print("Downloaded ", yt_url)
  
print("Downloaded ", str(d_counter), " streams")

download_end_time = time.time()
print("Downloading streams took ", str(download_end_time - start_time))

files = sorted(os.listdir(SAVE_PATH))
print(files[:11])

transcripts = []

# Transcribe audio to text
for file in files[:11]:
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

texts = textsplitter.create_documents([transcript.text for transcript in transcripts], metadatas=[{"source" : file} for file in files[:11]])
print("Docs size : ", asizeof.asizeof(texts))
doc_end_time = time.time()
print("Creating docs took ", str(doc_end_time - split_end_time))

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
    "How does the Aero Garden Seed Pod Kit work?",
    "What are the ingredients and steps for making Blueberry Muffins with Crumb Topping?",
    "What is the recipe for Canh Rau Muong (Vietnamese Water Spinach Soup)?",
    "How do you make a DIY Homemade Exfoliating Peppermint Sugar Body Scrub?",
    "What are the instructions for creating a DIY Mesh Water Ring Sling?",
    "What are the instructions for using the EASY Sleepy Wrap (baby wrap) in Part 2?",
    "How do you make Ravioli Soup with Zucchini and Spinach?",
    "What are the instructions for using the Eco Cub Baby Wrap Carrier for newborns?",
    "What are the ingredients and steps for making Fresh Peach Muffins?",
    "What are the steps for seed starting German Chamomile indoors for garden flowers?",
    "What are the steps for preparing and painting a motorcycle in BASECOAT PREP (PART 5)?",
    "How do you use the Aero Garden Seed pod kit for hydroponic gardening?",
    "How can you achieve a perfect crumb topping for Blueberry Muffins?",
    "What are the key ingredients and techniques for making Canh Rau Muong (Vietnamese Water Spinach Soup)?",
    "What are the benefits and instructions for making a DIY Homemade Exfoliating Peppermint Sugar Body Scrub?",
]

for question in questions:
  print(question)
  st = time.time()
  print(chain({"question": question}))
  print("Time ", str(time.time() - st))
end_time = time.time()

print("Answering all questions took ", str(end_time - chain_end_time))
print("Total time taken ", str(end_time - start_time))
