import os
import sys

# On Windows Python 3.8+, ctypes ignores the PATH env var.
# We must explicitly add the PyInstaller _MEIPASS folder so mpv-2.dll can be found.
if os.name == 'nt' and hasattr(sys, '_MEIPASS'):
    os.add_dll_directory(sys._MEIPASS)

from src.audio import AudioEngine
from src.provider import MusicProvider
from src.mpris import get_mpris_controller
from src.tui import TMusicApp

def main():
    try:
        engine = AudioEngine()
        provider = MusicProvider()
        mpris = get_mpris_controller(engine)
        
        app = TMusicApp(audio_engine=engine, music_provider=provider, mpris=mpris)
        app.run()
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\nFailed to start T-Music: {e}")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
