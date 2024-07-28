import pygame

class SoundEffects:
    def __init__(self, shoot_sound_file, collision_sound_file):
        # Load sound effects as WAV files
        self.shoot_sound = pygame.mixer.Sound(shoot_sound_file)
        self.collision_sound = pygame.mixer.Sound(collision_sound_file)

    def play_shoot_sound(self):
        self.shoot_sound.play()

    def play_collision_sound(self):
        self.collision_sound.play()
