from pytubefix import YouTube
import subprocess

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, client='WEB')
stream_url = yt.streams.get_audio_only().url

print("Extracted stream URL! Playing with mpv CLI...")
subprocess.run(["mpv", "--no-video", stream_url])
