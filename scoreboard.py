import pygame

class Scoreboard:
    """show scores, highest scores, lives, level"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.stats = ai_game.stats
        self.settings = ai_game.settings

        self.text_color = (240, 240, 240)
        self.font = pygame.font.Font(self.settings.font_path, 16)

        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        score_str = f"Score: {self.stats.score}"
        self.score_image = self.font.render(score_str, False, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.top = 8
        self.score_rect.right = self.screen_rect.right - 10

    def prep_high_score(self):
        high_str = f"High: {self.stats.high_score}"
        self.high_image = self.font.render(high_str, False, self.text_color)
        self.high_rect = self.high_image.get_rect()
        self.high_rect.top = 8
        self.high_rect.centerx = self.screen_rect.centerx

    def prep_level(self):
        lvl_str = f"Lv: {self.stats.level}"
        self.level_image = self.font.render(lvl_str, False, self.text_color)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.top = 8
        self.level_rect.left = 10

    def prep_ships(self):
        lives_str = f"Lives: {self.stats.ships_left}"
        self.lives_image = self.font.render(lives_str, False, self.text_color)
        self.lives_rect = self.lives_image.get_rect()
        self.lives_rect.top = self.level_rect.bottom + 6
        self.lives_rect.left = 10

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def draw(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_image, self.high_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.screen.blit(self.lives_image, self.lives_rect)

    def update_values(self):
        self.prep_score()
        self.prep_level()
        self.prep_ships()
