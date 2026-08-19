from pytubefix import YouTube
import vlc
import time

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, client='WEB')
stream_url = yt.streams.get_audio_only().url

print("Extracted stream URL! Playing with vlc...")
player = vlc.MediaPlayer(stream_url)
player.play()

for _ in range(5):
    print("VLC State:", player.get_state())
    time.sleep(1)
