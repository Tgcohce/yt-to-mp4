import streamlit as st
import os
import yt_dlp
from imageio_ffmpeg import get_ffmpeg_exe
import tempfile

def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Prefer MP4 format
        'ffmpeg_location': get_ffmpeg_exe(),  # Path to ffmpeg from imageio-ffmpeg
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'logtostderr': False,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'  # Convert to MP4 if needed
        }],
    }

    try:
        # Use a temporary directory to store the downloaded video
        with tempfile.TemporaryDirectory() as tmpdir:
            ydl_opts['outtmpl'] = os.path.join(tmpdir, '%(title)s.%(ext)s')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                video_title = info_dict.get('title', 'video')
                video_filename = ydl.prepare_filename(info_dict)

            # Read the video file
            with open(video_filename, 'rb') as f:
                video_bytes = f.read()

        return video_title, video_bytes

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None, None

def main():
    st.title("YouTube Video Downloader")
    st.write("Enter a YouTube link to download the video in MP4 format directly to your device.")

    # Input for the YouTube URL
    youtube_url = st.text_input("YouTube URL")

    # Button to trigger download
    if st.button("Download Video"):
        if youtube_url:
            with st.spinner("Downloading..."):
                video_title, video_bytes = download_video(youtube_url)
            if video_bytes:
                st.success("Download completed!")
                st.download_button(
                    label="Click here to download the video",
                    data=video_bytes,
                    file_name=f"{video_title}.mp4",
                    mime="video/mp4"
                )
            else:
                st.error("Failed to download video. Please check the URL or try again later.")
        else:
            st.warning("Please enter a valid YouTube URL.")

if __name__ == "__main__":
    main()
