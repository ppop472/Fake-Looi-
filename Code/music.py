import pygame
import time

def play_mp3(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

def main():
    mp3_file_path = "zene/zene.mp3"  # Update the file path to match your MP3 file
    play_mp3(mp3_file_path)
    print(mp3_file_path, "is playing...")
    # Keep the program running for a while
    while pygame.mixer.music.get_busy():
        time.sleep(1)

if __name__ == "__main__":
    main()
