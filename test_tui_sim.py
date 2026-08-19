import asyncio
from src.audio import AudioEngine
from src.provider import MusicProvider
from src.mpris import MPRISController
from src.tui import TMusicApp
import traceback

async def run_sim():
    engine = AudioEngine()
    provider = MusicProvider()
    mpris = MPRISController(engine)
    app = TMusicApp(audio_engine=engine, music_provider=provider, mpris=mpris)
    
    async with app.run_test() as pilot:
        try:
            await pilot.click("#search-input")
            await pilot.press("o", "n", " ", "m", "e", "l", "a", "n", "enter")
            await asyncio.sleep(2)
            
            await pilot.click("#search-results")
            await pilot.press("down", "enter")
            await asyncio.sleep(1)
            
            # Click the first row in the playlist
            await pilot.click("#playlist-table")
            await pilot.press("enter")
            await asyncio.sleep(1)
        except Exception as e:
            traceback.print_exc()

asyncio.run(run_sim())
