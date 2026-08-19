from src.audio import AudioEngine
import time

engine = AudioEngine()
engine.play("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

for _ in range(5):
    print("time_pos:", getattr(engine.player, 'time_pos', None))
    print("core_idle:", getattr(engine.player, 'core_idle', None))
    print("idle_active:", getattr(engine.player, 'idle_active', None))
    print("eof_reached:", getattr(engine.player, 'eof_reached', None))
    print("------------------")
    time.sleep(1)
