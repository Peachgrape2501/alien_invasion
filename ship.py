import pygame

class Ship:
    """ship"""
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = self.screen.get_rect()

        # own PNG
        img = pygame.image.load("images/player.png").convert_alpha()
        # zoom in/out
        img = pygame.transform.smoothscale(img, (60, 48))
        self.image = img
        self.rect = self.image.get_rect()

        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

        # moving
        self.moving_right = False
        self.moving_left = False

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        self.rect.x = int(self.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
