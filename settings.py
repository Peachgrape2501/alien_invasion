class Settings:
    """settings for all"""
    def __init__(self):
        # fonts
        self.font_path = "fonts/Pixeled.ttf"
        
        # screen
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 30)

        # ship
        self.ship_speed = 5.0
        self.ship_limit = 3  # lives

        # ship's bullet
        self.bullet_speed = 7.0
        self.bullets_allowed = 3
        self.bullet_width = 4
        self.bullet_height = 16

        # enemy's bullet
        self.enemy_bullet_speed = 4.0
        self.enemy_fire_chance_per_sec = 0.25  # green alien fire per seconds
        self.enemy_fire_min_interval_ms = 600  # single alien interval

        # alien
        self.alien_speed = 1.0          # moving speed
        self.fleet_drop_speed = 20      # drop speed
        self.fleet_direction = 1        # 1→right，-1→left

        # level
        self.speedup_scale = 1.1
        self.score_scale = 1.15

        # stats
        self.alien_score_green = 10
        self.alien_score_yellow = 20
        self.alien_score_red = 30

        # volume
        self.music_volume = 0.4
        self.sfx_volume = 0.8

    def initialize_dynamic(self):
        """parameters for levels"""
        self.alien_speed = 1.0
        self.fleet_direction = 1

        # stats; use also in stats.reset_stats()
        self.alien_score_green = 10
        self.alien_score_yellow = 20
        self.alien_score_red = 30

    def increase_difficulty(self):
        """level up, speed up"""
        self.alien_speed *= self.speedup_scale
        self.alien_score_green = int(self.alien_score_green * self.score_scale)
        self.alien_score_yellow = int(self.alien_score_yellow * self.score_scale)
        self.alien_score_red = int(self.alien_score_red * self.score_scale)




