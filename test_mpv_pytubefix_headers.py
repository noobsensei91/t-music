from pytubefix import YouTube
import mpv
import time

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, client='WEB')
audio_stream = yt.streams.get_audio_only()
stream_url = audio_stream.url

print("Extracted stream URL!")

player = mpv.MPV(video=False)
player.http_header_fields = "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
player.play(stream_url)

for _ in range(5):
    if player.time_pos is None:
        print("Waiting...", player.core_idle)
    else:
        print("Playing at", player.time_pos)
    time.sleep(1)
