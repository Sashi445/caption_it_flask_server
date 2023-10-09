from flask import Flask, request, jsonify, render_template
from concurrent.futures import ThreadPoolExecutor
import os
import uuid
from script import get_transcript_to_video, render_video_with_captions
from update_server import send_update_to_nodejs
from dotenv import load_dotenv
from utils import run_dir_checks

load_dotenv()

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "videos"
app.config["ALLOWED_EXTENSIONS"] = {"mp4", "avi", "mov"}

executor = ThreadPoolExecutor(max_workers=1)


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/check-server", methods=["GET"])
def check_server():
    return jsonify({"message": "Server is running!", "status": 200}), 200


@app.route("/render-video/<video_id>", methods=["POST"])
def render_video(video_id):
    # TODO: genereate transcript and post the update to NodeJS server
    body = request.get_json()
    transcript = body["transcript"]
    executor.submit(render_video_with_captions, transcript, video_id)
    return jsonify({"message": "Video rendering started!", "status": 200}), 200


@app.route("/", methods=["POST", "GET"])
def generate_transcript_to_video():
    try:
        if request.method == "POST":
            if "video" not in request.files:
                return "No file part", 400

            file = request.files["video"]

            if file.filename == "":
                return "No selected file", 400

            # Check if the file has an allowed extension
            if file and allowed_file(file.filename):
                # Create an uploads folder if it doesn't exist
                if not os.path.exists(app.config["UPLOAD_FOLDER"]):
                    os.makedirs(app.config["UPLOAD_FOLDER"])

                video_id = str(uuid.uuid4())

                file_name = f"{video_id}.mp4"
                # Save the uploaded file to the uploads folder
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], file_name))

                send_update_to_nodejs(
                    update_data={
                        "status": 0,
                        "message": "Video uploaded!",
                        "data": {
                            "videoId": video_id,
                            "name": file.filename,
                        },
                    }
                )

                # start video processing after video gets uploaded
                executor.submit(get_transcript_to_video, video_id)

                # Redirect to a success page or perform additional processing
                return jsonify({"message": "Video uploaded!", "status": 201}), 201

        return render_template("index.html")

    except Exception as e:
        return str(e), 500


if __name__ == "__main__":
    debug_mode = True if os.getenv("mode") == "DEV" else False
    port_number = os.getenv("PORT") or 5000
    run_dir_checks()
    app.run(debug=debug_mode, port=port_number)
