import os

def play_sound():
    os.system("aplay -D default ~/sdk/unitree_sdk2_python/samohlasky.m4a")

if __name__ == "__main__":
    play_sound()
