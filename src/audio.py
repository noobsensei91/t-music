import os
import sys
import mpv

class AudioEngine:
    def __init__(self):
        # Locate bundled yt-dlp if running from PyInstaller executable
        meipass = getattr(sys, '_MEIPASS', None)
        if meipass:
            ytdl_path = os.path.join(meipass, 'yt-dlp.exe' if os.name == 'nt' else 'yt-dlp')
            self.player = mpv.MPV(
                video=False,
                ytdl=True,
                ytdl_format='bestaudio/best',
                script_opts=f'ytdl_hook-ytdl_path={ytdl_path}'
            )
        else:
            self.player = mpv.MPV(
                video=False,
                ytdl=True,
                ytdl_format='bestaudio/best'
            )

    def is_playing(self) -> bool:
        if self.player.core_idle:
            return False
        if self.player.pause:
            return False
        return True

    def play(self, url: str):
        # Explicitly unpause before starting a new track
        self.player.pause = False
        # Pass the URL directly to mpv; the native ytdl_hook handles the rest
        self.player.play(url)

    def pause(self):
        self.player.pause = True

    def resume(self):
        self.player.pause = False

    def stop(self):
        self.player.stop()

    def set_volume(self, volume: int):
        self.player.volume = volume

    def toggle_pause(self):
        self.player.pause = not self.player.pause
