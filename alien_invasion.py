import sys
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from enemy_bullet import EnemyBullet
from alien import Alien
from explosion import Explosion
from button import Button



class AlienInvasion:
    """manage resources, start/win/gameover"""

    def __init__(self):
        pygame.init()

        # -------- basic settings and win --------
        self.settings = Settings()
        self.settings.initialize_dynamic()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        pygame.display.set_caption("Alien Invasion")

        self.clock = pygame.time.Clock()

        # -------- stats and UI --------
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self)

        # -------- game object --------
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()         # ship's bullet
        self.enemy_bullets = pygame.sprite.Group()   # enemy's bullet（only green aliens）
        self.aliens = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()      # explosion

        # -------- sound --------
        self._load_sounds()
        self._start_music()

        # -------- UI resources --------
        self._load_ui_assets()

        # -------- button --------
        cx = self.settings.screen_width // 2

        # Start position
        start_y = self.settings.screen_height // 2 + 190
        self.btn_start  = Button(self, "START", (cx, start_y),
                                 bg=(0,0,0), bg_hover=(30,30,30), fg=(255,255,255))

        # Replay / Exit keep the same position
        gameover_y = self.settings.screen_height // 2 + 40
        self.btn_replay = Button(self, "REPLAY", (cx-120, gameover_y + 80),
                                 bg=(0,0,0), bg_hover=(0,40,60), fg=(255,255,255))
        self.btn_exit   = Button(self, "EXIT",   (cx+120, gameover_y + 80),
                                 bg=(0,0,0), bg_hover=(60,0,0), fg=(255,80,80))



    # ================= main loop =================
    def run_game(self):
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_enemy_bullets()
                self._update_aliens()
                self.explosions.update()

            self._update_screen()
            self.clock.tick(60)

    # ================= events =================
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._on_keydown(event)
            elif event.type == pygame.KEYUP:
                self._on_keyup(event)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._on_click(event)  

    def _on_click(self, event):
        """click mouse left"""
        if self.stats.game_active:
            return  # 游戏中不响应按钮

        # win/game over: REPLAY / EXIT
        if self.stats.game_won or self.stats.ships_left <= 0:
            if self.btn_replay.clicked(event):
                self._start_new_game()
                return
            if self.btn_exit.clicked(event):
                pygame.quit(); sys.exit()
            return

        # start UI: START
        if self.btn_start.clicked(event):
            self._start_new_game()


    def _on_keydown(self, event):
        if event.key == pygame.K_ESCAPE:
            pygame.quit(); sys.exit()

        if not self.stats.game_active:
            if event.key == pygame.K_RETURN:
                self._start_new_game()
            return

    # Game started: left/right/A/D
        if event.key in (pygame.K_RIGHT,):
            self.ship.moving_right = True
        if event.key in (pygame.K_LEFT,):
            self.ship.moving_left = True
        if event.key in (pygame.K_d,):
            self.ship.moving_right = True
        if event.key in (pygame.K_a,):
            self.ship.moving_left = True
        if event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _on_keyup(self, event):
    # turn off A/D while release left/right or vice versa
        if event.key in (pygame.K_RIGHT, pygame.K_d):
            self.ship.moving_right = False
        if event.key in (pygame.K_LEFT, pygame.K_a):
            self.ship.moving_left = False


    # ================= sound/background music =================
    def _load_sounds(self):
        try:
            pygame.mixer.init()
        except Exception:
            pass
        self.snd_shoot = self._load_sound("sounds/laser.wav")
        self.snd_hit = self._load_sound("sounds/hit.wav")
        self.snd_explosion = self._load_sound("sounds/explosion.wav")

    def _load_sound(self, path):
        try:
            s = pygame.mixer.Sound(path)
            s.set_volume(self.settings.sfx_volume)
            return s
        except Exception:
            return None

    def _start_music(self):
        try:
            pygame.mixer.music.load("sounds/music.wav")
            pygame.mixer.music.set_volume(self.settings.music_volume)
            pygame.mixer.music.play(-1)  # playing again
        except Exception:
            pass

    # ================= UI resources & fonts =================
    def _load_ui_assets(self):
        # nightsky background for start/gameover/win UI
        try:
            bg = pygame.image.load("images/nightsky.png").convert()
            self.start_bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
        except Exception:
            self.start_bg = None

    def _font(self, size):
        # set fonts from settings.font_path; otherwise go back to the default fonts
        try:
            return pygame.font.Font(self.settings.font_path, size)
        except Exception:
            return pygame.font.SysFont(None, size)

    # ================= ship's bullet =================
    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            self.bullets.add(Bullet(self))
            if self.snd_shoot:
                self.snd_shoot.play()

    def _update_bullets(self):
        self.bullets.update()

        for b in self.bullets.copy():
            if b.rect.bottom <= 0:
                self.bullets.remove(b)

        # collide: ship's bullet vs alien (delete bullet but not necessary aliens)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        if collisions:
            for _, aliens_hit in collisions.items():
                for alien in aliens_hit:
                    died = alien.take_hit(1)          # delete lives and hit effects
                    if self.snd_hit:
                        self.snd_hit.play()
                    if died:
                        # stats and explosion
                        self.stats.score += alien.score_value()
                        self.sb.check_high_score()
                        self.sb.update_values()
                        if self.snd_explosion:
                            self.snd_explosion.play()
                        self.explosions.add(Explosion(self, alien.image, alien.rect.center))
                        alien.kill()

        # condition to win: >= 1000 scores
        if self.stats.score >= 1000 and self.stats.game_active:
            self._win_game()

        # clean win
        if self.stats.game_active and not self.aliens:
            self._new_wave()

    # ================= alien's bullet =================
    def spawn_enemy_bullet(self, x, y):
        """green aliens shot from (x,y)"""
        self.enemy_bullets.add(EnemyBullet(self, x, y))

    def _update_enemy_bullets(self):
        self.enemy_bullets.update()

        for eb in self.enemy_bullets.copy():
            if eb.rect.top >= self.settings.screen_height:
                self.enemy_bullets.remove(eb)

        # enemy's bullet shot ships
        if self.stats.game_active and pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
            self._ship_hit()

    # ================= alien =================
    def _create_fleet(self):
        """multiple lines of aliens"""
        sample = Alien(self)
        w, h = sample.rect.size

        available_space_x = self.settings.screen_width - 2 * w
        number_aliens_x = max(1, available_space_x // (2 * w))

        available_space_y = self.settings.screen_height - (3 * h) - 100
        number_rows = max(2, available_space_y // (2 * h))

        self.aliens.empty()
        for row in range(number_rows):
            for col in range(number_aliens_x):
                self._create_alien(col, row)

    def _create_alien(self, col, row):
        alien = Alien(self)
        w, h = alien.rect.size
        alien.x = w + 2 * w * col
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * h * row
        self.aliens.add(alien)

    def _update_aliens(self):
        # go down if touch the edge 
        if any(a.check_edges() for a in self.aliens.sprites()):
            for a in self.aliens.sprites():
                a.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

        self.aliens.update()

        # lives deducted if aliens touch the end
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

        # lives deducted if aliens touch player
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    # ================= life/replay/new wave/win =================
    def _ship_hit(self):
        """player got shot or aliens touch the end: lives deducted/game over"""
        if not self.stats.game_active:
            return

        self.stats.ships_left -= 1
        self.sb.update_values()

        if self.stats.ships_left <= 0:
            # game over
            self.stats.game_active = False
            self.stats.game_won = False
            return

        # clean the win and new wave
        self.aliens.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.explosions.empty()
        self.ship.center_ship()
        self._create_fleet()

    def _new_wave(self):
        """clean the win and new wave with higher level"""
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.explosions.empty()
        self.settings.increase_difficulty()
        self.stats.level += 1
        self.sb.update_values()
        self._create_fleet()

    def _win_game(self):
        """reach the 1000 scores and win"""
        self.stats.game_active = False
        self.stats.game_won = True

    def _start_new_game(self):
        """restart the game"""
        # reset the speed and stats
        self.settings.initialize_dynamic()
        # reset the stats
        self.stats.reset_stats()
        self.sb.update_values()
        self.sb.check_high_score()
        # clean win and objects
        self.aliens.empty()
        self.bullets.empty()
        self.enemy_bullets.empty()
        self.explosions.empty()
        self.ship.center_ship()
        # new wave and restart
        self._create_fleet()
        self.stats.game_active = True

    # ================= draw =================
    def _update_screen(self):
        if self.stats.game_active:
            # playing the game, draw as usual
            self.screen.fill(self.settings.bg_color)

            for b in self.bullets.sprites():
                b.draw_bullet()
            for eb in self.enemy_bullets.sprites():
                eb.draw_bullet()

            self.ship.blitme()
            self.aliens.draw(self.screen)
            self.explosions.draw(self.screen)

            self.sb.draw()
        else:
            # start/win/game over：night sky + titles
            if self.start_bg:
                self.screen.blit(self.start_bg, (0, 0))
            else:
                self.screen.fill((10, 10, 25))

            if self.stats.game_won:
                self._draw_victory()
            elif self.stats.ships_left <= 0:
                self._draw_game_over()
            else:
                self._draw_start_screen()

        pygame.display.flip()

    # ---- Start Screen ----
    def _draw_start_screen(self):
        title_font = self._font(56)
        tip_font = self._font(11)

        title = title_font.render("ALIEN INVASION", False, (0, 255, 100))
        tip2 = tip_font.render("Move: Left/Right  Fire: SPACE   Exit: ESC", False, (150, 255, 255))

        # semi-transparent black backgound
        padding = 18
        wrap_rect = title.get_rect(center=(self.settings.screen_width//2, self.settings.screen_height//2 - 40))
        box_rect = wrap_rect.unionall([tip2.get_rect(center=(wrap_rect.centerx, wrap_rect.bottom + 80))])
        box_rect.inflate_ip(padding*2, padding*2)

        overlay = pygame.Surface(box_rect.size)
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, box_rect)

        self.screen.blit(title, title.get_rect(center=(box_rect.centerx, wrap_rect.centery)))
        self.screen.blit(tip2, tip2.get_rect(center=(box_rect.centerx, wrap_rect.bottom + 80)))

        # highest score at up right screen
        hs_font = self._font(20)
        hs = hs_font.render(f"HIGHEST: {self.stats.high_score}", False, (230, 230, 230))
        self.screen.blit(hs, hs.get_rect(top=10, right=self.settings.screen_width - 10))
    
        self.btn_start.draw(self.screen)


    # ---- Game Over ----
    def _draw_game_over(self):
        font = self._font(24)
        text_color = (255, 80, 80)
        msg = "GAME OVER"
        msg_img = font.render(msg, False, text_color)

        padding = 16
        bg_rect = msg_img.get_rect(center=self.screen.get_rect().center)
        bg_rect.inflate_ip(padding * 2, padding)

        overlay = pygame.Surface(bg_rect.size)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, bg_rect)

        self.screen.blit(msg_img, msg_img.get_rect(center=bg_rect.center))

        self.btn_replay.draw(self.screen)
        self.btn_exit.draw(self.screen)


    # ---- Victory ----
    def _draw_victory(self):
        lines = [
            "YOU WON! THE STARS ARE YOURS"
        ]
        text = lines[0]  # random.choice(lines) maybe...

        font = self._font(12)
        msg_img = font.render(f"{text} 🌟", False, (255, 255, 0))  # yellow and stars

        padding = 16
        bg_rect = msg_img.get_rect(center=self.screen.get_rect().center)
        bg_rect.inflate_ip(padding * 2, padding)

        overlay = pygame.Surface(bg_rect.size)
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, bg_rect)

        self.screen.blit(msg_img, msg_img.get_rect(center=bg_rect.center))

        # hints
        tip_font = self._font(10)
        tip = tip_font.render("Press ENTER to Play Again", False, (230, 230, 230))
        tip_rect = tip.get_rect(center=(bg_rect.centerx, bg_rect.bottom + 40))
        self.screen.blit(tip, tip_rect)

        self.btn_replay.draw(self.screen)
        self.btn_exit.draw(self.screen)


if __name__ == "__main__":
    AlienInvasion().run_game()

