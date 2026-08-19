from src.audio import AudioEngine
import time

def my_log(loglevel, component, message):
    print('[{}] {}: {}'.format(loglevel, component, message))

engine = AudioEngine()
engine.player.log_handler = my_log
print("Extracting and playing...")
engine.play("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

for _ in range(5):
    print("Is playing?", engine.is_playing())
    time.sleep(1)
