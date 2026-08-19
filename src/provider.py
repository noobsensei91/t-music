import os
import json
import requests
from ytmusicapi import YTMusic

class MusicProvider:
    def __init__(self):
        # ytmusicapi OAuth is currently completely broken by Google backend changes, 
        # so we strictly use an unauthenticated client for public scraping.
        self.ytmusic = YTMusic()
        
        self.access_token = None
        if os.path.exists('oauth.json'):
            try:
                with open('oauth.json') as f:
                    self.access_token = json.load(f)['access_token']
            except:
                pass

    def get_user_playlists(self) -> list:
        if not self.access_token:
            return [{"title": "⚠️ Requires Auth. Run 'ytmusicapi oauth' in terminal.", "browseId": "ERROR"}]
        
        try:
            # Use official YouTube Data API v3 for authenticated requests
            url = "https://www.googleapis.com/youtube/v3/playlists"
            params = {"part": "snippet,contentDetails", "mine": True, "maxResults": 50}
            headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}
            
            r = requests.get(url, headers=headers, params=params)
            if r.status_code == 200:
                parsed = []
                for p in r.json().get("items", []):
                    parsed.append({
                        "browseId": p["id"],
                        "title": p["snippet"]["title"],
                        "author": p["snippet"]["channelTitle"],
                        "itemCount": p["contentDetails"]["itemCount"]
                    })
                return parsed
            else:
                return [{"title": f"⚠️ API Error: {r.status_code}", "browseId": "ERROR"}]
        except Exception as e:
            return [{"title": f"⚠️ Error: {str(e)}", "browseId": "ERROR"}]

    def search(self, query: str, limit: int = 10) -> list:
        """
        Searches for a track on YouTube Music and returns a standardized list of results.
        """
        raw_results = self.ytmusic.search(query, filter="songs", limit=limit)
        
        parsed_results = []
        for item in raw_results:
            if item["resultType"] == "song":
                parsed_results.append({
                    "videoId": item["videoId"],
                    "title": item["title"],
                    "artists": [artist["name"] for artist in item.get("artists", [])],
                    "duration": item.get("duration"),
                })
                
        return parsed_results

    def search_playlists(self, query: str, limit: int = 10) -> list:
        raw_results = self.ytmusic.search(query, filter="playlists", limit=limit)
        parsed_results = []
        for item in raw_results:
            if item["resultType"] == "playlist":
                parsed_results.append({
                    "browseId": item["browseId"],
                    "title": item["title"],
                    "author": item.get("author", ""),
                    "itemCount": item.get("itemCount", "?")
                })
        return parsed_results

    def get_playlist_tracks(self, browse_id: str) -> list:
        # First try ytmusicapi (fast, works for public playlists, doesn't consume API quota)
        try:
            raw_playlist = self.ytmusic.get_playlist(browse_id)
            parsed_results = []
            for item in raw_playlist.get("tracks", []):
                if item.get("videoId"):
                    parsed_results.append({
                        "videoId": item["videoId"],
                        "title": item["title"],
                        "artists": [artist["name"] for artist in item.get("artists", [])],
                        "duration": item.get("duration"),
                    })
            if parsed_results:
                return parsed_results
        except Exception:
            pass
            
        # If it failed (private playlist), fallback to official YouTube Data API v3
        if not self.access_token:
            return []
            
        # YouTube Data API requires raw playlist IDs (remove VL prefix if present)
        if browse_id.startswith("VL"):
            browse_id = browse_id[2:]
            
        url = "https://www.googleapis.com/youtube/v3/playlistItems"
        params = {"part": "snippet,contentDetails", "playlistId": browse_id, "maxResults": 50}
        headers = {"Authorization": f"Bearer {self.access_token}", "Accept": "application/json"}
        
        try:
            r = requests.get(url, headers=headers, params=params)
            if r.status_code == 200:
                parsed_results = []
                for item in r.json().get("items", []):
                    video_id = item["contentDetails"].get("videoId")
                    if video_id:
                        parsed_results.append({
                            "videoId": video_id,
                            "title": item["snippet"]["title"],
                            "artists": ["YouTube"],
                            "duration": "?:??",
                        })
                return parsed_results
        except Exception:
            pass
            
        return []
