# Google Cloud Speech-To-Text Interview Transcriber
# Please follow the instructions in the README.md first!

#!/usr/bin/env python3

# Set up deps for GC Speech
import sys, os, io, time, configparser
from pathlib import Path, PurePath
from google.oauth2 import service_account
from google.cloud import speech_v1p1beta1 as speech

# Script config
script_config = configparser.ConfigParser()

try:
    script_config.read("config.ini")
except Exception as e:
    print("Error reading config file. Exiting.")
    print(e)
    exit()

# Auth
credentials = service_account.Credentials.from_service_account_file(PurePath(Path(__file__).resolve().parent).joinpath(Path(str(script_config["OPTS"]["Credentials"]))))

# Instantiate GC Speech client
client = speech.SpeechClient(credentials=credentials)

if str(script_config["OPTS"]["Mode"]) == "local":
    # Read-in audio from local file (60s limit, gs is recommended Mode)
    with io.open(PurePath(Path(__file__).resolve().parent).joinpath(str(script_config["OPTS"]["Path"])), "rb") as audio_file:
        content = audio_file.read()
        audio = speech.RecognitionAudio(content=content)
else:
    # Read-in audio from GS
    print(str(script_config["OPTS"]["Path"]))
    audio = speech.RecognitionAudio(uri=str(script_config["OPTS"]["Path"]))

# Config request
req_config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    language_code=str(script_config["OPTS"]["Language"]),
    enable_speaker_diarization=True,
    diarization_speaker_count=int(script_config["OPTS"]["Speakers"]),
    enable_automatic_punctuation=True,
)

# Set GC Operation
try:
    operation = client.long_running_recognize(config=req_config, audio=audio)
except Exception as e:
    print("An error has occurred. Please ensure that you have access permissions to the bucket, and that your GCS account is active!")
    print(e)
    exit()

# Process the audio
print("Waiting for operation to complete...")

def progress(future):
    future.result()

operation.add_done_callback(progress)

while (not operation.done()):
     print(operation.metadata.progress_percent)
     time.sleep(1)

print(operation.metadata.progress_percent)

response = operation.result()

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

# Initiate phrases array
phrases = {}

# Last speaker tag is the 1st one of result
last_speaker_tag = words_info[0].speaker_tag

phrase_idx = 0
phrases[phrase_idx] = str(last_speaker_tag) + ": "

# Prepare the phrases
for word_info in words_info:
    # Different speaker
    if (word_info.speaker_tag != last_speaker_tag):
        # Set to new speaker
        last_speaker_tag = word_info.speaker_tag
        # New phrase
        phrase_idx += 1
        phrases[phrase_idx] = str(last_speaker_tag) + ": "
    # Write word to phrase
    phrases[phrase_idx] += str(word_info.word) + " "

# Format the output, write to file
output = ""
for phrase in phrases:
    # Append phrase and strip trailing spaces
    output += phrases[phrase].strip() + "\n\n"
    print(output)

try:
    f = open(PurePath(Path(__file__).resolve().parent).joinpath(Path(str(script_config["OPTS"]["Path"])).stem + "_transcript.txt"), "w")
    f.write(output)
    f.close()
except Exception as e:
    print("Error writing to transcript file.")
    print(e)
    exit()