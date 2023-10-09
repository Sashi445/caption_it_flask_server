import os
import subprocess


def remove_file_extension(filename):
    """
    Remove the file extension from a filename using string methods.

    Args:
        filename (str): The input filename.

    Returns:
        str: The filename without the file extension.
    """
    # Find the last occurrence of the dot (.) in the filename
    last_dot_index = filename.rfind(".")

    # Check if a dot was found and remove the extension if found
    if last_dot_index != -1:
        filename_without_extension = filename[:last_dot_index]
        return filename_without_extension
    else:
        # If no dot was found, return the original filename
        return filename


def extract_audio_from_video(
    video_name: str, video_dir_path: str = "videos", audio_out_dir: str = "audio"
):
    audio_name = f"{remove_file_extension(video_name)}.wav"
    audio_path = os.path.join(os.getcwd(), audio_out_dir, audio_name)
    video_path = os.path.join(os.getcwd(), video_dir_path, video_name)
    # cmd = [
    #     "ffmpeg",
    #     "-i",
    #     video_path,
    #     "-vn",
    #     "-acodec",
    #     "pcm_s16le",
    #     "-ar",
    #     "44100",
    #     "-ac",
    #     "2",
    #     audio_path,
    # ]
    cmd = [
    "ffmpeg",
    "-i",
    video_path,
    "-vn",               # Disable video stream
    "-acodec", "pcm_s16le",  # Set audio codec to PCM 16-bit little-endian
    "-ar", "44100",      # Set audio sample rate to 44100 Hz
    "-ac", "1",          # Set audio channels to mono (1 channel)
    audio_path
]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode
