import yt_dlp
import mpv
import time

ydl_opts = {
    'format': 'bestaudio/best', 
    'quiet': True,
    'cookiefile': 'cookies.txt',
    'extractor_args': {'youtube': ['player_client=ios']},
}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
    url = info.get('url', 'None')
    headers = info.get('http_headers', {})

player = mpv.MPV(video=False, cookies='cookies.txt')
if 'http_headers' in info:
    player.http_header_fields = ",".join([f"{k}: {v}" for k, v in headers.items()])
player.play(url)

for _ in range(5):
    print("time_pos:", getattr(player, 'time_pos', None))
    print("core_idle:", getattr(player, 'core_idle', None))
    time.sleep(1)
