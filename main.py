from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, make_response, jsonify

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
        print(request.files['audio_file'].filename)
        return redirect(url_for("summary"))
    return render_template("upload.html")
        

@app.route("/summary")
def summary():
    return render_template("summary.html")


if __name__ == "__main__":
    app.run(debug=True)
