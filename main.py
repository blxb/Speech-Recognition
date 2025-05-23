import sounddevice as sd # library for recording sound
import numpy as np # library for working with massives(these things [])
import scipy.io.wavfile as wav # library for working with .wav files
import speech_recognition as sr # library for speech recognition
from googletrans import Translator # library for translating the speech
import sys # for a later purpose

duration = 5  # duration of recording
sample_rate = 44100

# List of supported and popular language codes
supportedLangs = {
    "en-US": "English (United States)",
    "en-GB": "English (United Kingdom)",
    "es-ES": "Spanish (Spain)",
    "es-MX": "Spanish (Mexico)",
    "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese (Portugal)",
    "ru-RU": "Russian",
    "fr-FR": "French",
    "de-DE": "German",
    "it-IT": "Italian",
    "hi-IN": "Hindi",
    "ar-EG": "Arabic (Egypt)",
    "ar-SA": "Arabic (Saudi Arabia)",
    "zh-CN": "Chinese (Simplified)",
    "ja-JP": "Japanese",
    "ko-KR": "Korean",
    "tr-TR": "Turkish",
    "id-ID": "Indonesian",
    "pl-PL": "Polish"
}

# Build the prompt string
prompt = "Pick your langauge for speech\n"
for code, name in supportedLangs.items():
    prompt += f"[{name}]: {code}\n"
    
speechLang = input(prompt + "\nEnter the language code (e.g., en-US): ").strip() # asking user to input the language they would rather to speak

if speechLang in supportedLangs:
    print(f"You selected: {supportedLangs[speechLang]}")
else:
    print("❌ Invalid language code. Please enter a valid one from the list.")    

print("Speak...")
recording = sd.rec(
  int(duration * sample_rate), # recording duration in samples
  samplerate=sample_rate,      # sampling frequency
  channels=1,                  # 1 - is mono
  dtype="int16")               # audio data format
sd.wait()  # Waiting for recording session to finish

wav.write("output.wav", sample_rate, recording)
print("Recording is finished, now recognizing")

recognizer = sr.Recognizer()
with sr.AudioFile("output.wav") as source:
    audio = recognizer.record(source)

try:
    text = recognizer.recognize_google(audio, language=speechLang)
    print("You said:", text)
except sr.UnknownValueError:             # - if Google didn't understand the speech (noise, silence)
    print("Couldn't recognize the speech")
    sys.exit() # make sure that script exits before continuing further
except sr.RequestError as e:             # - if there is no internet or API is unavailable
    print(f"Server's error: {e}")
    sys.exit() # the same here make sure that script exits if fails

possibleLangs = ["ru", "en", "es", "pt", "id", "it", "tr"] #list of all of the possible supported translates
lang = input("\nWhich language do you want your recorder voice to be translated to:\n[Russian]: ru\n[English]: en\n[Espanol]: es\n[Portugal]: pt\n[Indonesian]: id\n[Polish]: pl\n[Italian]: it\n[Turkish]: tr \nEnter the language: ").strip()

# checking if what the user inputed is an actually valid language code(by checking it from possibleLangs listen)
if lang not in possibleLangs:
    print("Enter a valid language.")
    sys.exit()
else:
    print(f"You selected: {lang}")
    
translator = Translator()
translated = translator.translate(text, dest=lang)  # here is the language that user choices
print(f"🌍 Translating to {lang}:", translated.text)    