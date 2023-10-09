""" Pipeline for generating captions on video """

import os
from extract_audio import extract_audio_from_video
from generate_transcript import generate_transcript
from add_text_to_video import add_captions
from update_server import send_update_to_nodejs


def get_transcript_to_video(video_id):
    video_name = f"{video_id}.mp4"
    return_code = extract_audio_from_video(video_name=video_name)
    # return code is 0 when the process is success
    if return_code == 0:
        # video_path = os.path.join(os.getcwd(), "videos/", video_name)
        audio_path = os.path.join(
            os.getcwd(), "audio/", video_name.split(".")[0] + ".wav"
        )

        send_update_to_nodejs(
            update_data={
                "status": 1,
                "message": "Audio Extracted!",
                "data": {
                    "videoId": video_id,
                },
            }
        )

        # TODO: this transcript has to be stored in db so that user can edit this later
        transcript = generate_transcript(audio_file_path=audio_path)
        print("[LOG]: Transcript Genereated!")
        message = {
            "data": {
                "videoId": video_id,
                "transcript": transcript,
            },
            "status": 2,
            "message": "Transcript Genereated!",
        }
        send_update_to_nodejs(update_data=message)
        return

    send_update_to_nodejs(
        update_data={
            "data": {
                "videoId": video_id,
            },
            "status": -1,
            "message": "Audio extraction failed!",
        }
    )
    return


def render_video_with_captions(transcript, video_id):
    video_name = f"{video_id}.mp4"
    video_path = os.path.join(os.getcwd(), "videos/", video_name)

    caption_words = [
        (word["start"], word["end"] - word["start"], word["word"])
        for word in transcript
    ]

    output_path = add_captions(
        video_name=video_name, video_path=video_path, captions=caption_words
    )

    print("[LOG]: output video generated")
    message = {
        "status": 3,
        "message": "Video Generated!",
        "data": {"videoId": video_name, "outputPath": output_path},
    }
    send_update_to_nodejs(update_data=message)
