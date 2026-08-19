from pytubefix import YouTube

url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
yt = YouTube(url, client='WEB')
audio_stream = yt.streams.get_audio_only()
print("Downloading first chunk...")
resp = audio_stream.stream_to_buffer()
chunk = next(resp)
print(f"Downloaded chunk of size {len(chunk)}")
