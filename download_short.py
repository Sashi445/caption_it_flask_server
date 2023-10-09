from pytube import YouTube


def download_yt_short(yt_short_id, out_dir="videos"):
    # Define the URL of the YouTube short video
    youtube_url = f"https://www.youtube.com/shorts/{yt_short_id}"

    try:
        # Create a YouTube object
        yt = YouTube(youtube_url)

        # Get the highest resolution stream (video and audio combined)
        stream = yt.streams.get_highest_resolution()

        # Specify the path where you want to save the video
        download_path = out_dir

        # Download the video
        stream.download(output_path=download_path)

        print("Video downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


download_yt_short("gw-qzSA33wA")
download_yt_short('mL_6ZrF9vkU')
download_yt_short('34ERpdSI0hg')
download_yt_short('q8Us9fK8e4A')
download_yt_short('0DkvRA6v3CM')
