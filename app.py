from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, make_response, jsonify
from pydub.audio_segment import read_wav_audio
from werkzeug.utils import secure_filename
import engine

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/process", methods= ['GET','POST'])
def process():
    if request == 'POST':
        raw_audio = request.files['raw_audio']
        raw_audio.save(secure_filename(raw_audio.filename))
        print(raw_audio.filename)
        # processed_audio = engine.pre_process_audio(raw_audio.filename)
        # transcription = engine.transcribe(processed_audio)
        return redirect(url_for("summary", result = raw_audio.filename))
    return redirect(url_for("summary", result = "transcription failed")) 

@app.route("/upload", methods= ['GET','POST'])
def upload():   
    if request == 'POST': 
        raw_audio = request.files['raw_audio']
        raw_audio.save(secure_filename(raw_audio.filename))
        print(raw_audio.filename)
        processed_audio = engine.pre_process_audio(raw_audio.filename)
        transcription = engine.transcribe(processed_audio)
        return redirect(url_for("summary", result = transcription))  
    else:
        return render_template("upload.html")

@app.route("/summary/<result>")
def summary(result):
    return render_template("summary.html",result=result)

if __name__ == "__main__":
    app.run(debug=True)
