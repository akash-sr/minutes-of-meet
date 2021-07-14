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
        
# @app.route("/sign_s3")
# def sign_s3():
#     S3_BUCKET = os.environ["S3_BUCKET_NAME"]

#     file_name = request.args.get("file_name")
#     file_type = request.args.get("file_type")

#     s3 = boto3.client("s3")

#     presigned_post = s3.generate_presigned_post(
#         Bucket = S3_BUCKET,
#         Key = file_name,
#         Fields = {"acl": "public-read", "Content-Type": file_type},
#         Conditions = [
#             {"acl": "public-read"},
#             {"Content-Type": file_type}
#         ],
#         ExpiresIn = 3600
#     )

#     return json.dumps({
#         "data"  : presigned_post,
#         "url"   : f"https://{S3_BUCKET}.s3.amazonaws.com/{file_name}"  
#     })


@app.route("/summary/<result>")
def summary(result):
    return render_template("summary.html",result=result)


if __name__ == "__main__":
    app.run(debug=True)
