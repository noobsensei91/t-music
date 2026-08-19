import pytest
from src.provider import MusicProvider

def test_search_track():
    provider = MusicProvider()
    results = provider.search("Chainsaw Man Kick Back", limit=1)
    
    assert isinstance(results, list)
    assert len(results) > 0
    
    first_result = results[0]
    assert "videoId" in first_result
    assert "title" in first_result
    assert "artists" in first_result
    
    # Check if we got the expected song
    assert "kick back" in first_result["title"].lower()
