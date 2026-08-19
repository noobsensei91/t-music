from mpris_server.server import Server
from mpris_server.adapters import MprisAdapter
from mpris_server import PlayState
from mpris_server.base import dbus_emit_changes
from gi.repository import GLib
import threading

class TMusicAdapter(MprisAdapter):
    def __init__(self, audio_engine):
        super().__init__()
        self.engine = audio_engine
        self.current_title = "T-Music"
        self.current_artist = "Unknown"
        self.on_next = None
        self.on_previous = None
        self.server = None

    def emit_properties_changed(self, changed_props):
        if getattr(self, 'server', None) and getattr(self.server, 'player', None):
            try:
                # changed_props can be a list of strings, or a dict. 
                # If dict, we just extract keys to let mpris_server fetch the property.
                props = list(changed_props.keys()) if isinstance(changed_props, dict) else changed_props
                dbus_emit_changes(self.server.player, props)
            except Exception:
                pass

    def update_metadata(self, title, artist):
        self.current_title = title
        self.current_artist = artist
        self.emit_properties_changed({'Metadata': self.metadata()})

    def play(self):
        self.engine.resume()

    def pause(self):
        self.engine.pause()

    def play_pause(self):
        self.engine.toggle_pause()

    def next(self):
        if self.on_next:
            self.on_next()

    def previous(self):
        if self.on_previous:
            self.on_previous()

    def get_current_position(self):
        time_pos = getattr(self.engine.player, 'time_pos', 0)
        return int(time_pos * 1000000) if time_pos else 0

    def get_volume(self):
        return 1.0

    def get_shuffle(self):
        return False

    def get_rate(self):
        return 1.0

    def can_control(self):
        return True

    def can_pause(self):
        return True

    def can_play(self):
        return True

    def can_go_next(self):
        return True

    def can_go_previous(self):
        return True

    def can_seek(self):
        return False

    def get_playstate(self):
        if getattr(self.engine.player, 'core_idle', True):
            return PlayState.STOPPED
        if self.engine.is_playing():
            return PlayState.PLAYING
        return PlayState.PAUSED

    def get_stream_title(self):
        return self.current_title

    def get_current_track(self):
        from mpris_server.types import Track
        return Track(track_id="/org/mpris/MediaPlayer2/TrackList/0")

    def metadata(self):
        return {
            'mpris:trackid': '/org/mpris/MediaPlayer2/TrackList/0',
            'xesam:title': self.current_title,
            'xesam:artist': [self.current_artist]
        }

class MPRISController:
    def __init__(self, audio_engine):
        self.adapter = TMusicAdapter(audio_engine)
        self.server = Server('tmusic', adapter=self.adapter)
        self.adapter.server = self.server

    def start(self):
        self.server.publish()
        self.loop = GLib.MainLoop()
        threading.Thread(target=self.loop.run, daemon=True).start()
