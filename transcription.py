import os
import math
from pydub import AudioSegment

FILE_NAME = "Ratan Tata Speech - India's Car Industry.mp3"
AUDIO_FILE = "transcript.wav"

# convert mp3 file to wav
sound = AudioSegment.from_mp3(os.path.join(FILE_NAME))
sound.export(AUDIO_FILE, format="wav")
print("WAV file generated from the MP3 file successfully")
print()

#breaking WAV file to chunks for better analysis
from pydub import AudioSegment
from pydub.silence import split_on_silence

DBFS_OFFSET = -40
sound_file = AudioSegment.from_wav(AUDIO_FILE)
audio_chunks = split_on_silence(sound_file, min_silence_len=2000, silence_thresh=sound_file.max_dBFS + DBFS_OFFSET )

try:
    os.mkdir("CHUNKS")
except:
    print("Please delete the folder CHUNKS from current working directory.")

print("Folder 'CHUNKS' made to store the small chunks of complete audio file")
print()
for i, chunk in enumerate(audio_chunks):
    out_file = "chunk{0}.wav".format(i)
    print("Exporting", out_file)
    output_path = os.path.join("CHUNKS", out_file)
    chunk.export(output_path, format="wav")


#data visualization
import librosa
import librosa.display
import matplotlib.pyplot as plt


data, sampling_rate = librosa.load(os.path.join(AUDIO_FILE))
plt.figure(figsize=(40, 10))
librosa.display.waveplot(data,sampling_rate)
plt.title(AUDIO_FILE)
plt.show()

# transcribe audio file                                       
import speech_recognition as sr

r = sr.Recognizer()

i=0
for name in os.listdir("CHUNKS"):
    i+=1

text_file = open("transcript.txt", "w")

print("Transcribing audio chunks ---> ")
print()
for j in range(i):
    filename = "chunk{0}.wav".format(j)
    with sr.AudioFile(os.path.join("CHUNKS",filename)) as source:
        r.adjust_for_ambient_noise(source, duration=0.1)
        audio = r.record(source)  # read the entire audio file
        try:
            text_file.write(filename+": " + r.recognize_google(audio, language="en-in"))
            text_file.write("\n")
            print(filename+": " + r.recognize_google(audio, language="en-in"))
        except:
            text_file.write(filename+": ...Audio unclear...")
            text_file.write("\n")
            print(filename+": ...Audio unclear...")
text_file.close()