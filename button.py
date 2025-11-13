import pygame

class Button:
    def __init__(self, ai_game, text, center, size=(220, 64), 
                 bg=(0,0,0), bg_hover=(30,30,30), fg=(255,255,255), font_size=28):
        self.ai_game = ai_game
        self.text = text
        self.center = center
        self.size = size
        self.bg = bg
        self.bg_hover = bg_hover
        self.fg = fg
        self.font_size = font_size

        self.font = self._font(font_size)
        self.image = self.font.render(self.text, False, self.fg)
        self.rect = pygame.Rect(0,0,*self.size)
        self.rect.center = self.center

    def _font(self, size):
        try:
            return pygame.font.Font(self.ai_game.settings.font_path, size)
        except Exception:
            return pygame.font.SysFont(None, size)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hover = self.rect.collidepoint(mouse_pos)
        color = self.bg_hover if is_hover else self.bg

        # semi-transparent black background + border
        pad = 10
        base = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        base.fill((*color, 210))
        pygame.draw.rect(base, (200,200,200), base.get_rect(), width=2, border_radius=10)
        surface.blit(base, self.rect)

        # text
        self.image = self.font.render(self.text, False, self.fg)
        surface.blit(self.image, self.image.get_rect(center=self.rect.center))

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False
