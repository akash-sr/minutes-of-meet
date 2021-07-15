from deepspeech import Model
import scipy.io.wavfile as wav
from pydub import AudioSegment
import os

# set acoustic and language model paths
model_path  = "model/deepspeech-0.9.3-models.pbmm"
scorer_path = "model/deepspeech-0.9.3-models.scorer"

# allowed_extensions = ['wav','webm','ogg','mp3']

# instantiate an object of the model using the acoustic model path
ds = Model(model_path)
# set the language model
ds.enableExternalScorer(scorer_path)

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
    return ds.stt(audio)

