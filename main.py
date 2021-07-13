from flask import Flask, render_template, flash, request, redirect, url_for, send_from_directory, make_response, jsonify
import os, json, boto3

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
        
@app.route("/sign_s3")
def sign_s3():
    S3_BUCKET = os.environ.get("S3_BUCKET")

    file_name = request.args.get("file_name")
    file_type = request.args.get("file_type")

    s3 = boto3.client("s3")

    presigned_post = s3.generate_presigned_post(
        Bucket = S3_BUCKET,
        Key = file_name,
        Fields = {"acl": "public-read", "Content-Type": file_type},
        Conditions = [
            {"acl": "public-read"},
            {"Content-Type": file_type}
        ],
        ExpiresIn = 3600
    )

    return json.dumps({
        "data"  : presigned_post,
        "url"   : f"https://{S3_BUCKET}.s3.amazonaws.com/{file_name}"  
    })

@app.route("/summary")
def summary():
    return render_template("summary.html")


if __name__ == "__main__":
    app.run(debug=True)
