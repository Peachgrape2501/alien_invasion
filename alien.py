import pygame, random
from pygame.sprite import Sprite

class Alien(Sprite):
    """single alien:tyoe/HP/score + expliosion + green aliens fire randomly"""

    TYPES = [
        ("green", "images/green.png", 1),   # (name, path, HP)
        ("yellow","images/yellow.png", 2),
        ("red",   "images/red.png", 3),
    ]

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game

        name, path, hp = random.choice(self.TYPES)
        self.kind = name
        base_img = pygame.image.load(path).convert_alpha()
        base_img = pygame.transform.smoothscale(base_img, (48, 48))

        self.normal_image = base_img
        flash_img = base_img.copy()
        flash_img.fill((255, 255, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
        self.flash_image = flash_img

        self.image = self.normal_image
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

        self.hp = hp
        self.max_hp = hp
        self.flash_ms = 80
        self._flash_until = 0

        # green aliens fire cool down a bit
        self._next_fire_ready_at = 0

    # === scores ===
    def score_value(self):
        s = self.settings
        if self.kind == "green":
            return s.alien_score_green
        if self.kind == "yellow":
            return s.alien_score_yellow
        return s.alien_score_red

    def update(self):
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

        # switch image
        if pygame.time.get_ticks() < self._flash_until:
            self.image = self.flash_image
        else:
            self.image = self.normal_image

        # green aliens fire ramdomly
        if self.kind == "green":
            self._try_fire_randomly()

    def _try_fire_randomly(self):
        now = pygame.time.get_ticks()
        if now < self._next_fire_ready_at:
            return
        # ~ estimate with 60FPS :p_frame = p_sec / 60
        p_sec = self.settings.enemy_fire_chance_per_sec
        p_frame = p_sec / 60.0
        if random.random() < p_frame:
            # shot from the bottom
            self.ai_game.spawn_enemy_bullet(self.rect.centerx, self.rect.bottom)
            self._next_fire_ready_at = now + self.settings.enemy_fire_min_interval_ms

    def take_hit(self, dmg=1):
        self.hp -= dmg
        self._flash_until = pygame.time.get_ticks() + self.flash_ms
        return self.hp <= 0

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return self.rect.right >= screen_rect.right or self.rect.left <= 0
