from src.audio import AudioEngine
from src.provider import MusicProvider
from src.mpris import get_mpris_controller
from src.tui import TMusicApp
import sys

def main():
    try:
        engine = AudioEngine()
        provider = MusicProvider()
        mpris = get_mpris_controller(engine)
        
        app = TMusicApp(audio_engine=engine, music_provider=provider, mpris=mpris)
        app.run()
    except Exception as e:
        print(f"Failed to start T-Music: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
