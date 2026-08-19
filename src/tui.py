from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, DataTable, Label, Static
from textual.containers import Horizontal, Vertical
from textual import work
from src.audio import AudioEngine
from src.provider import MusicProvider
from src.mpris import MPRISController
import time
import threading

class PlayerBar(Static):
    status_text = ""
    def update_status(self, text: str):
        self.status_text = text
        self.update(text)

class TMusicApp(App):
    CSS_PATH = "tmusic.tcss"
    BINDINGS = [
        ("space", "toggle_play", "Play/Pause"),
        ("m", "toggle_mute", "Mute"),
        ("q", "quit", "Quit"),
        ("p", "prev_track", "Prev"),
        ("n", "next_track", "Next"),
        ("+", "volume_up", "Vol +"),
        ("-", "volume_down", "Vol -"),
        ("a", "add_selected", "Add"),
        ("A", "add_all", "Add All"),
    ]

    def __init__(self, audio_engine: AudioEngine, music_provider: MusicProvider, mpris: MPRISController):
        super().__init__()
        self.engine = audio_engine
        self.provider = music_provider
        self.mpris = mpris
        
        self.playlist = []
        self.current_song_index = -1
        self.current_song_name = "None"
        
        self.update_timer = None

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main-container"):
            with Vertical(id="left-pane"):
                yield Input(placeholder="Search YouTube Music...", id="search-input")
                yield DataTable(id="search-results")
            with Vertical(id="right-pane"):
                yield Label("Queue / Playlist", classes="pane-title")
                yield DataTable(id="playlist-table")
        yield PlayerBar("Idle - Press 'space' to play/pause", id="player-bar")
        yield Footer()

    def on_mount(self) -> None:
        # Initialize search results table
        search_table = self.query_one("#search-results", DataTable)
        search_table.add_columns("Title", "Artist", "ID")
        search_table.cursor_type = "row"

        # Initialize playlist table
        playlist_table = self.query_one("#playlist-table", DataTable)
        playlist_table.add_columns("Playing", "Title", "Artist")
        playlist_table.cursor_type = "row"

        # Start MPRIS
        self.mpris.adapter.on_next = self.action_next_track
        self.mpris.adapter.on_previous = self.action_prev_track
        self.mpris.start()
        
        # Start a UI update loop
        self.set_interval(1.0, self.update_player_status)

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search-input":
            query = event.value
            if query:
                event.input.value = ""
                self.query_one(PlayerBar).update_status(f"Searching for '{query}'...")
                self.perform_search(query)

    @work(thread=True)
    def perform_search(self, query: str):
        if query.startswith("pl: "):
            results = self.provider.search_playlists(query[4:])
            self.call_from_thread(self.update_search_results, results, is_playlist=True)
        elif query == "my_playlists":
            results = self.provider.get_user_playlists()
            self.call_from_thread(self.update_search_results, results, is_playlist=True)
        else:
            results = self.provider.search(query)
            self.call_from_thread(self.update_search_results, results, is_playlist=False)

    def update_search_results(self, results, is_playlist=False):
        table = self.query_one("#search-results", DataTable)
        table.clear()
        for res in results:
            if is_playlist:
                table.add_row(f"📂 {res['title']}", f"{res['author']} ({res['itemCount']})", f"pl:{res['browseId']}")
            else:
                artists_str = ", ".join(res['artists'])
                table.add_row(res['title'], artists_str, res['videoId'])
        self.query_one(PlayerBar).update_status("Search complete. Press Enter to play/load, 'a' to add to queue, 'A' to add all.")

    @work(thread=True)
    def load_playlist_tracks(self, browse_id: str):
        self.call_from_thread(self.query_one(PlayerBar).update_status, "Fetching playlist tracks...")
        tracks = self.provider.get_playlist_tracks(browse_id)
        self.call_from_thread(self.add_tracks_to_queue_and_play, tracks)

    def add_tracks_to_queue_and_play(self, tracks):
        start_index = len(self.playlist)
        for res in tracks:
            artists_str = ", ".join(res['artists'])
            self.playlist.append({"title": res['title'], "artist": artists_str, "id": res['videoId']})
            playlist_table = self.query_one("#playlist-table", DataTable)
            marker = ">>" if len(self.playlist) - 1 == self.current_song_index + 1 else "  "
            playlist_table.add_row(marker, res['title'], artists_str)
            
        self.query_one(PlayerBar).update_status(f"Added {len(tracks)} tracks to queue.")
        if self.current_song_index == -1 or not self.engine.is_playing():
            self.play_track(start_index)

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "search-results":
            row_data = event.data_table.get_row(event.row_key)
            title, artist, item_id = row_data
            
            if item_id.startswith("pl:"):
                browse_id = item_id[3:]
                if browse_id != "ERROR":
                    self.load_playlist_tracks(browse_id)
                return

            self.playlist.append({"title": title, "artist": artist, "id": item_id})
            playlist_table = self.query_one("#playlist-table", DataTable)
            marker = ">>" if len(self.playlist) - 1 == self.current_song_index + 1 else "  "
            playlist_table.add_row(marker, title, artist)
            
            if self.current_song_index == -1 or not self.engine.is_playing():
                self.play_track(len(self.playlist) - 1)
                
        elif event.data_table.id == "playlist-table":
            row_index = event.data_table.get_row_index(event.row_key)
            self.play_track(row_index)

    def action_add_selected(self) -> None:
        table = self.query_one("#search-results", DataTable)
        try:
            row_key = table.coordinate_to_cell_key(table.cursor_coordinate).row_key
            row_data = table.get_row(row_key)
            title, artist, item_id = row_data
            if not item_id.startswith("pl:"):
                self.playlist.append({"title": title, "artist": artist, "id": item_id})
                playlist_table = self.query_one("#playlist-table", DataTable)
                playlist_table.add_row("  ", title, artist)
                self.query_one(PlayerBar).update_status(f"Added '{title}' to queue.")
        except:
            pass

    def action_add_all(self) -> None:
        table = self.query_one("#search-results", DataTable)
        added = 0
        for row_key in table.rows:
            title, artist, item_id = table.get_row(row_key)
            if not item_id.startswith("pl:"):
                self.playlist.append({"title": title, "artist": artist, "id": item_id})
                playlist_table = self.query_one("#playlist-table", DataTable)
                playlist_table.add_row("  ", title, artist)
                added += 1
        if added > 0:
            self.query_one(PlayerBar).update_status(f"Added {added} tracks to queue.")

    def play_track(self, index: int):
        if index < 0 or index >= len(self.playlist):
            return
            
        self.current_song_index = index
        song = self.playlist[index]
        self.current_song_name = f"{song['title']} - {song['artist']}"
        
        # Update MPRIS metadata here
        self.mpris.adapter.update_metadata(song['title'], song['artist'])
        
        self.query_one(PlayerBar).update_status(f"Loading '{self.current_song_name}'...")
        
        # Play in background thread to not block UI
        url = f"https://www.youtube.com/watch?v={song['id']}"
        threading.Thread(target=self.engine.play, args=(url,), daemon=True).start()
        self.update_playlist_ui()

    def update_playlist_ui(self):
        table = self.query_one("#playlist-table", DataTable)
        for i in range(len(self.playlist)):
            marker = "🔊" if i == self.current_song_index else "  "
            table.update_cell_at((i, 0), marker)

    def action_toggle_play(self) -> None:
        self.engine.toggle_pause()
        is_paused = getattr(self.engine.player, 'pause', False)
        state_str = "⏸️ PAUSED" if is_paused else "▶️ PLAYING"
        self.query_one(PlayerBar).update_status(f"{state_str} | {self.current_song_name}")

    def action_toggle_mute(self) -> None:
        is_mute = not getattr(self.engine.player, 'mute', False)
        self.engine.player.mute = is_mute
        self.query_one(PlayerBar).update_status(f"{'🔇 Muted' if is_mute else '🔊 Unmuted'}")

    def action_volume_up(self) -> None:
        vol = getattr(self.engine.player, 'volume', 100)
        new_vol = min(100, vol + 10)
        self.engine.player.volume = new_vol
        self.query_one(PlayerBar).update_status(f"🔊 Volume: {new_vol}%")

    def action_volume_down(self) -> None:
        vol = getattr(self.engine.player, 'volume', 100)
        new_vol = max(0, vol - 10)
        self.engine.player.volume = new_vol
        self.query_one(PlayerBar).update_status(f"🔉 Volume: {new_vol}%")

    def action_next_track(self) -> None:
        if self.current_song_index + 1 < len(self.playlist):
            self.play_track(self.current_song_index + 1)

    def action_prev_track(self) -> None:
        if self.current_song_index > 0:
            self.play_track(self.current_song_index - 1)

    def update_player_status(self):
        # Called every second
        if self.current_song_index == -1:
            return
            
        is_loading = getattr(self.engine.player, 'core_idle', True)
        is_paused = getattr(self.engine.player, 'pause', False)
        
        if is_loading:
            state_str = "⏳ LOADING"
            playstate = "Stopped"
        elif is_paused:
            state_str = "⏸️ PAUSED"
            playstate = "Paused"
        else:
            state_str = "▶️ PLAYING"
            playstate = "Playing"
        
        # Don't overwrite temporary status messages like Volume/Mute if they just appeared
        bar = self.query_one(PlayerBar)
        if hasattr(bar, 'status_text') and "Volume" not in bar.status_text and "Mute" not in bar.status_text:
            bar.update_status(f"{state_str} | {self.current_song_name}")
            
        # Emit MPRIS playstate changes so GNOME knows we can be controlled by media keys
        if not hasattr(self, '_last_playstate') or self._last_playstate != playstate:
            self._last_playstate = playstate
            try:
                self.mpris.adapter.emit_properties_changed({'PlaybackStatus': playstate})
            except Exception:
                pass
