from pytubefix import YouTube
import mpv
import time

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, client='WEB')
audio_stream = yt.streams.get_audio_only()
stream_url = audio_stream.url

print("Extracted stream URL from pytubefix!")
