from pytubefix import YouTube
import mpv
import time

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, use_oauth=True, allow_oauth_cache=True)
audio_stream = yt.streams.get_audio_only()
stream_url = audio_stream.url

print("Extracted stream URL from pytubefix!")

player = mpv.MPV(video=False)
player.play(stream_url)

for _ in range(5):
    print("time_pos:", getattr(player, 'time_pos', None))
    print("core_idle:", getattr(player, 'core_idle', None))
    time.sleep(1)
