from pytubefix import YouTube
import mpv
import time

def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, client='WEB')
stream_url = yt.streams.get_audio_only().url

player = mpv.MPV(video=False, log_handler=my_log)
player.play(stream_url)

for _ in range(5):
    print("core_idle:", player.core_idle, "time_pos:", player.time_pos)
    time.sleep(1)
