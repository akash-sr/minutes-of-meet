from deepspeech import Model
import scipy.io.wavfile as wav
from pydub import AudioSegment

import os
from dotenv import load_dotenv

# import NLP's Libraries
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

"""
# import IBM watson's STT libraries
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()
API_KEY = os.getenv("API_KEY")
URL = os.getenv("URL")

mimeTypes = {
  'mp3' : 'audio/mp3',
  'ebm': 'audio/webm',
  'wav' : 'audio/wav',
  'ogg' : 'audio/ogg'
}

"""

# set acoustic and language model paths
model_path  = "model/asr-model/deepspeech-0.9.3-models.pbmm"
scorer_path = "model/asr-model/deepspeech-0.9.3-models.scorer"

# asr-deepspeech-model initialization
# instantiate an object of the model using the acoustic model path
ds = Model(model_path)
# set the language model
ds.enableExternalScorer(scorer_path)

"""
# asr-IBM-model initialization
authenticator = IAMAuthenticator(API_KEY) 
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(URL)

"""

# nlp-model initialization
tokenizer        = AutoTokenizer.from_pretrained("model/nlp-model/tokenizer/",local_files_only=True)
summarizer_model = AutoModelForSeq2SeqLM.from_pretrained("model/nlp-model/model/",local_files_only=True)

# function to transcribe the processed audio
def transcribe(processed_audio):
    fs, audio = wav.read(processed_audio)
    transcription = ds.stt(audio)
    # delete the porcessed audio
    os.remove(processed_audio)
    return transcription

"""
def transcribeIBM(audio_clip):
  ext = audio_clip[-3:]
  content_type = mimeTypes[ext]
  with open(audio_clip,'rb') as f:
    result = stt.recognize(audio=f, content_type=content_type, model='en-US_NarrowbandModel', continuous = True).get_result()
  raw_transcripts = result['results']
  final_transcript = ""
  for transcripts in raw_transcripts:
    final_transcript = final_transcript + transcripts['alternatives'][0]['transcript']
  return final_transcript
"""


# wrapper function to pre-process the audio the raw audio: converts it to bitrate 16kHz and only one channel (mono)
def pre_process_audio(raw_audio, processed_audio='processed_audio.wav'):
  os.system("ffmpeg -i "+ raw_audio+ " -ac 1 -ar 16000"+" " + processed_audio )
  os.remove(raw_audio)
  return processed_audio

# function to generate the summary
# def generate_summary(transcription):
#   inputs     = tokenizer(transcription,truncation=True,return_tensors='pt')
#   prediction = summarizer_model.generate(**inputs)
#   summary    = tokenizer.batch_decode(prediction,skip_special_tokens=True)
#   return summary[0]

# function to generate the summary considering the small inputs
def generate_summary(transcription):
  number_of_words = len(transcription.split())
  if (number_of_words < 50):
    summary = [transcription]
  else:
    inputs             = tokenizer(transcription,truncation=True,return_tensors='pt')
    prediction         = summarizer_model.generate(**inputs)
    summary            = tokenizer.batch_decode(prediction,skip_special_tokens=True)
  return(summary[0])



