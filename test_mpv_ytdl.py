import mpv
import time

def my_log(loglevel, component, message):
    if loglevel in ['error', 'fatal']:
        print('[{}] {}: {}'.format(loglevel, component, message))

player = mpv.MPV(
    video=False,
    ytdl=True,
    ytdl_format='bestaudio/best',
    ytdl_raw_options='cookies-from-browser=firefox,js-runtimes=node',
    log_handler=my_log
)

print("Playing natively with mpv and ytdl_hook...")
player.play("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

for _ in range(15):
    print("core_idle:", player.core_idle, "time_pos:", player.time_pos)
    if player.time_pos is not None:
        print("PLAYING!")
        break
    time.sleep(1)
