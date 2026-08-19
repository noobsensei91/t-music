import mpv
import time
player = mpv.MPV(
    video=False,
    ytdl=True,
    ytdl_format='bestaudio/best',
    ytdl_raw_options='cookies-from-browser=firefox,js-runtimes=node'
)
print("Playing...")
player.play("https://www.youtube.com/watch?v=04mfKJWDSzI")
for _ in range(10):
    time.sleep(1)
    print("core_idle:", player.core_idle, "time_pos:", player.time_pos)
