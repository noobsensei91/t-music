from unittest.mock import MagicMock
from src.mpris import TMusicAdapter

def test_mpris_adapter():
    engine_mock = MagicMock()
    adapter = TMusicAdapter(engine_mock)
    
    # Simulate pressing play on keyboard
    adapter.play()
    engine_mock.resume.assert_called_once()
    
    # Simulate pressing pause on keyboard
    adapter.pause()
    engine_mock.pause.assert_called_once()
    
    # Simulate PlayPause toggle
    engine_mock.is_playing.return_value = True
    adapter.play_pause()
    assert engine_mock.pause.call_count == 2
    
    engine_mock.is_playing.return_value = False
    adapter.play_pause()
    assert engine_mock.resume.call_count == 2
