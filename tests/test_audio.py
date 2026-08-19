import pytest
import time
from src.audio import AudioEngine

def test_audio_engine():
    engine = AudioEngine()
    assert not engine.is_playing()
    
    # Give it a test video ID
    # This might take a few seconds to resolve via yt-dlp
    engine.play("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    # Wait up to 15 seconds for buffering
    started = False
    for _ in range(15):
        if engine.is_playing():
            started = True
            break
        time.sleep(1)
    
    assert started
    
    # Test pause
    engine.pause()
    time.sleep(0.5)
    assert not engine.is_playing()
    
    # Test resume
    engine.resume()
    time.sleep(0.5)
    assert engine.is_playing()
    
    # Test stop
    engine.stop()
    time.sleep(0.5)
    assert not engine.is_playing()
