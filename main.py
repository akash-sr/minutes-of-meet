from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, make_response, jsonify
from werkzeug.utils import secure_filename
import engine

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/record")
def record():
    return render_template("record.html")

@app.route("/upload", methods=['GET','POST'])
def upload():     
    if request.method == 'POST':
        raw_audio = request.files['raw_audio']
        raw_audio.save(secure_filename(raw_audio.filename))
        processed_audio = engine.pre_process_audio(raw_audio.filename)
        transcription = engine.transcribe(processed_audio)
        print(transcription)
        return f"{transcription}"
    return render_template("upload.html")

@app.route("/summary/<result>")
def summary(result):
    return render_template("summary.html",result=result)


if __name__ == "__main__":
    app.run(debug=True)
