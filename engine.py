from deepspeech import Model
import scipy.io.wavfile as wav
from pydub import AudioSegment
import os

# set acoustic and language model paths
model_path  = "model/deepspeech-0.9.3-models.pbmm"
scorer_path = "model/deepspeech-0.9.3-models.scorer"


# instantiate an object of the model using the acoustic model path
ds = Model(model_path)
# set the language model
ds.enableExternalScorer(scorer_path)

# wrapper function to pre-process the audio the raw audio: converts it to bitrate 16kHz and only one channel (mono)
def pre_process_audio(raw_audio, audio_path, processed_audio='processed_audio.wav'):
  extension = raw_audio[-3:]
  if extension != 'wav':
      print("Invalid File Format!")
      quit()
  audio = AudioSegment.from_file(os.path.join(audio_path,raw_audio))
  audio = audio.set_frame_rate(16000).set_channels(1)
  audio.export(os.path.join(audio_path,processed_audio), format="wav") #exporting to .wav format
  return os.path.join(audio_path,processed_audio)

# function to transcribe the processed audio
def transcribe(processed_audio):
    fs, audio = wav.read(processed_audio)
    transcription = ds.stt(audio)
    # delete the porcessed audio
    os.remove(processed_audio)
    return ds.stt(audio)

