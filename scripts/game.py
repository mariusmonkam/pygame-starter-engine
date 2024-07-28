import pygame
import sys
from fighter import Fighter
from alien import Alien
from ball import Ball
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_FILL_COLOR, GAME_CAPTION
from game_music import GameMusic, SoundEffects
from generate_midi import generate_sound_files

class Game:
    def __init__(self):
        pygame.display.set_caption(GAME_CAPTION)
        self.screen_width, self.screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        self.screen_fill_color = SCREEN_FILL_COLOR
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.game_font = pygame.font.Font(None, 30)
        self.game_score = 0

        self.fighter = Fighter()
        self.alien = Alien()
        self.ball = Ball(self.fighter)

        self.clock = pygame.time.Clock()
        self.game_is_running = True

        # Ensure sound files are created
        generate_sound_files()

        # Initialize game music with the provided background music file
        self.music = GameMusic('music/children_music_pretty.mid')
        self.music.play_background_music()

        # Initialize sound effects
        self.sound_effects = SoundEffects('effects/shoot_sound.mid', 'effects/collision_sound.mid')

    def run(self):
        while self.game_is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.music.stop_background_music()
                    sys.exit()
                self.handle_key_events(event)

            self.update_game_state()
            self.draw_screen()
            self.clock.tick(60)  # Limit the frame rate to 60 FPS

        self.show_game_over()
        self.music.stop_background_music()  # Stop music when the game is over

    def handle_key_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.fighter.move_left()
            if event.key == pygame.K_RIGHT:
                self.fighter.move_right()
            if event.key == pygame.K_SPACE:
                self.ball.fire()
                self.sound_effects.play_shoot_sound()  # Play shoot sound

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.fighter.stop_moving()

    def update_game_state(self):
        self.fighter.update_position()
        self.alien.update_position()
        self.ball.update_position()

        if self.ball.is_out_of_screen():
            self.ball.reset()

        if self.ball.is_collision(self.alien):
            self.ball.reset()
            self.alien.reset()
            self.game_score += 1
            self.sound_effects.play_collision_sound()  # Play collision sound

        if self.alien.has_reached_fighter(self.fighter):
            self.game_is_running = False

    def draw_screen(self):
        self.screen.fill(self.screen_fill_color)
        self.screen.blit(self.fighter.image, (self.fighter.x, self.fighter.y))
        self.screen.blit(self.alien.image, (self.alien.x, self.alien.y))
        if self.ball.was_fired:
            self.screen.blit(self.ball.image, (self.ball.x, self.ball.y))
        self.show_game_score()
        self.show_info_box()
        pygame.display.update()

    def show_game_score(self):
        game_score_text = self.game_font.render(f"Your Score is: {self.game_score}", True, 'white')
        self.screen.blit(game_score_text, (20, 20))

    def show_info_box(self):
        info_box_text = self.game_font.render(f"Fighter Position: ({self.fighter.x}, {self.fighter.y})", True, 'white')
        self.screen.blit(info_box_text, (20, 50))

    def show_game_over(self):
        game_over_text = self.game_font.render("Game Over", True, 'white')
        game_over_rectangle = game_over_text.get_rect()
        game_over_rectangle.center = (self.screen_width / 2, self.screen_height / 2)
        self.screen.blit(game_over_text, game_over_rectangle)
        pygame.display.update()
        pygame.time.wait(5000)

# Entry point
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    game = Game()
    game.run()
    pygame.quit()
