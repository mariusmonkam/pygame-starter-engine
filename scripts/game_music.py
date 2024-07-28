import pygame

class GameMusic:
    def __init__(self, background_music_file):
        self.background_music_file = background_music_file

    def play_background_music(self):
        pygame.mixer.music.load(self.background_music_file)
        pygame.mixer.music.play(-1)  # Loop indefinitely

    def stop_background_music(self):
        pygame.mixer.music.stop()

class SoundEffects:
    def __init__(self, shoot_sound_file, collision_sound_file):
        self.shoot_sound_file = shoot_sound_file
        self.collision_sound_file = collision_sound_file

    def play_shoot_sound(self):
        pygame.mixer.music.load(self.shoot_sound_file)
        pygame.mixer.music.play()

    def play_collision_sound(self):
        pygame.mixer.music.load(self.collision_sound_file)
        pygame.mixer.music.play()
