import yt_dlp
import mpv
import time

def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

ydl_opts = {
    'format': 'bestaudio/best', 
    'quiet': True,
    'extractor_args': {'youtube': ['player_client=ios']}
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
    url = info.get('url', 'None')
    headers = info.get('http_headers', {})

player = mpv.MPV(video=False, log_handler=my_log)
if 'http_headers' in info:
    player.http_header_fields = ",".join([f"{k}: {v}" for k, v in headers.items()])
player.play(url)

for _ in range(5):
    print("time_pos:", getattr(player, 'time_pos', None))
    time.sleep(1)
