import yt_dlp
from imageio_ffmpeg import get_ffmpeg_exe


def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Prefer MP4 format
        'ffmpeg_location': get_ffmpeg_exe(),  # Path to ffmpeg from imageio-ffmpeg
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'  # Convert to mp4 if needed
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading in MP4 format...")
            ydl.download([url])
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")


youtube_link = input("Enter the YouTube URL: ")
download_video(youtube_link)
