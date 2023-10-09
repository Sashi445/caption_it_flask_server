import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import secrets

def get_random_video_name():
    # Generate a random string of a specified length
    random_string_length = 10  # You can adjust the length as needed
    random_string = secrets.token_hex(random_string_length)
    return random_string


def add_captions(video_name, video_path, captions):
    # Load the video
    video = VideoFileClip(video_path)

    # Create a list to store text clips
    text_clips = []

    # Create text clips for each caption
    for timestamp, duration, caption in captions:
        # Create a TextClip for the caption
        text_clip = TextClip(
            caption,
            fontsize=30,
            color="white",
            bg_color="black",
            font="Arial-Bold",
            kerning=5,
        )

        # # Add a shadow to the text
        # shadow = text_clip.margin(10, color=(0, 0, 0, 0.5))

        # Set the duration and position of the text clip
        text_clip = text_clip.set_duration(
            duration
        )  # Set the duration (1 second in this case)
        text_clip = text_clip.set_position(("center"))  # Set the position

        # Add the text clip to the list
        text_clips.append(text_clip.set_start(timestamp))

    # Create a CompositeVideoClip from the text clips and set its duration
    captioned_video = CompositeVideoClip(
        [video.set_duration(video.duration)] + text_clips
    )

    output_path = os.path.join("output/", f"{video_name}.mp4")

    # Write the final video with captions to a file
    captioned_video.write_videofile(output_path, codec="libx264")

    # Close video clips
    video.close()
    captioned_video.close()
