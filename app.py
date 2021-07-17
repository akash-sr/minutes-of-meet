from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, make_response, jsonify
from pydub.audio_segment import read_wav_audio
from werkzeug.utils import secure_filename
import engine
import os
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/process", methods= ['GET','POST'])
def process():
    if request.method == 'POST':
        raw_audio = request.files['raw_audio']
        raw_audio.save(secure_filename(raw_audio.filename))
        # processed_audio = engine.pre_process_audio(raw_audio.filename)
        # transcription = engine.transcribe(processed_audio)
        transcription = engine.transcribeIBM(raw_audio.filename)
        f = open("transcription.txt","w")
        f.write(transcription)
        f.close()
        return jsonify({
            "status" : "works"
        })
    return redirect(url_for("/"))

@app.route("/upload", methods= ['GET','POST'])
def upload():   
    if request.method == 'POST': 
        raw_audio = request.files['raw_audio']
        raw_audio.save(secure_filename(raw_audio.filename))
        # processed_audio = engine.pre_process_audio(raw_audio.filename)
        # transcription = engine.transcribe(processed_audio)
        transcription = engine.transcribeIBM(raw_audio.filename)
        f = open("transcription.txt","w")
        f.write(transcription)
        f.close()
        return redirect(url_for("summarize"))
    else:
        return render_template("upload.html")

@app.route("/summarize")
def summarize():
    f = open("transcription.txt", "r")
    transcription = f.read()
    summary = engine.generate_summary(transcription)
    f.close()
    f = open("summary.txt","w")
    f.write(summary)
    f.close()
    return redirect(url_for("result"))

@app.route("/result")
def result():
    f = open("summary.txt","r")
    summary = f.read()
    f.close()
    return render_template("result.html",result=summary)

if __name__ == "__main__":
    app.run(debug=True)
