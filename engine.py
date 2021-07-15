from deepspeech import Model
import scipy.io.wavfile as wav
from pydub import AudioSegment
import os

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# set acoustic and language model paths
model_path  = "model/asr-model/deepspeech-0.9.3-models.pbmm"
scorer_path = "model/asr-model/deepspeech-0.9.3-models.scorer"

# asr-model initialization
# instantiate an object of the model using the acoustic model path
ds = Model(model_path)
# set the language model
ds.enableExternalScorer(scorer_path)

# nlp-model initialization
tokenizer        = AutoTokenizer.from_pretrained("model/nlp-model/tokenizer/")
summarizer_model = AutoModelForSeq2SeqLM.from_pretrained("model/nlp-model/model/")

# wrapper function to pre-process the audio the raw audio: converts it to bitrate 16kHz and only one channel (mono)
def pre_process_audio(raw_audio, processed_audio='processed_audio.wav'):
  # extension = raw_audio[-3:]
  # if extension not in allowed_extensions:
  #   return ""
  audio = AudioSegment.from_file(raw_audio)
  # audio = audio.set_frame_rate(16000).set_channels(1)
  # audio.export(processed_audio, format="wav") #exporting to .wav format
  os.system("ffmpeg -i "+ raw_audio+ " -ac 1 -ar 16000"+" " + processed_audio )
  os.remove(raw_audio)
  return processed_audio

# function to transcribe the processed audio
def transcribe(processed_audio):
    fs, audio = wav.read(processed_audio)
    transcription = ds.stt(audio)
    # delete the porcessed audio
    os.remove(processed_audio)
    return transcription

# function to generate the summary
def generate_summary(transcription):
  inputs     = tokenizer(transcription,truncation=True,return_tensors='pt')
  prediction = summarizer_model.generate(**inputs)
  summary    = tokenizer.batch_decode(prediction,skip_special_tokens=True)
  return summary[0]

