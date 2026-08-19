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
    def update_status(self, text: str):
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
        results = self.provider.search(query)
        self.call_from_thread(self.update_search_results, results)

    def update_search_results(self, results):
        table = self.query_one("#search-results", DataTable)
        table.clear()
        for res in results:
            artists_str = ", ".join(res['artists'])
            table.add_row(res['title'], artists_str, res['videoId'])
        self.query_one(PlayerBar).update_status("Search complete. Press Enter on a song to play.")

    async def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "search-results":
            row_data = event.data_table.get_row(event.row_key)
            title, artist, video_id = row_data
            
            # Add to playlist
            self.playlist.append({"title": title, "artist": artist, "id": video_id})
            
            playlist_table = self.query_one("#playlist-table", DataTable)
            marker = ">>" if len(self.playlist) - 1 == self.current_song_index + 1 else "  "
            playlist_table.add_row(marker, title, artist)
            
            # If nothing is playing, play it
            if self.current_song_index == -1 or not self.engine.is_playing():
                self.play_track(len(self.playlist) - 1)
                
        elif event.data_table.id == "playlist-table":
            row_index = event.data_table.get_row_index(event.row_key)
            self.play_track(row_index)

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
        self.engine.player.mute = not getattr(self.engine.player, 'mute', False)

    def action_volume_up(self) -> None:
        vol = getattr(self.engine.player, 'volume', 100)
        self.engine.player.volume = min(100, vol + 10)

    def action_volume_down(self) -> None:
        vol = getattr(self.engine.player, 'volume', 100)
        self.engine.player.volume = max(0, vol - 10)

    def action_next_track(self) -> None:
        if self.current_song_index + 1 < len(self.playlist):
            self.play_track(self.current_song_index + 1)
        else:
            self.query_one(PlayerBar).update_status("No next track in queue.")

    def action_prev_track(self) -> None:
        if self.current_song_index > 0:
            self.play_track(self.current_song_index - 1)
        else:
            self.query_one(PlayerBar).update_status("Already at the first track.")

    def update_player_status(self):
        # Called every second
        if self.current_song_index == -1:
            return
            
        is_loading = getattr(self.engine.player, 'core_idle', True)
        is_paused = getattr(self.engine.player, 'pause', False)
        
        if is_loading:
            state_str = "⏳ LOADING"
        elif is_paused:
            state_str = "⏸️ PAUSED"
        else:
            state_str = "▶️ PLAYING"
        
        bar = self.query_one(PlayerBar)
        bar.update_status(f"{state_str} | {self.current_song_name}")
