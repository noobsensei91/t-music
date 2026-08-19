import yt_dlp
ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
    print("URL:", info.get('url', 'None')[:100], "...")
    print("Headers:", info.get('http_headers', {}))
