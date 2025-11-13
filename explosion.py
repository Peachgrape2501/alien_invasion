import pygame
from pygame.sprite import Sprite

class Explosion(Sprite):
    """simple explosion：short time white flash + fades out rapidly"""
    def __init__(self, ai_game, image, center, duration_ms=180):
        super().__init__()
        self.screen = ai_game.screen
        # highlighted original one and decrese alpha gradually 
        self.base = image.copy()
        self.base.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.image = self.base.copy()
        self.rect = self.image.get_rect(center=center)

        self.start = pygame.time.get_ticks()
        self.duration = duration_ms

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start
        if elapsed >= self.duration:
            self.kill()
            return
        # change transparency
        alpha = max(0, 255 - int(255 * (elapsed / self.duration)))
        self.image.set_alpha(alpha)
