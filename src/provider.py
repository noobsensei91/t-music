from ytmusicapi import YTMusic

class MusicProvider:
    def __init__(self):
        # We don't need authentication for simple search
        self.ytmusic = YTMusic()

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
