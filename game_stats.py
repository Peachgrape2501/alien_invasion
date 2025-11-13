class GameStats:
    """monitor stats(score, lives, level, whether playing/game over）"""
    def __init__(self, settings):
        self.settings = settings
        self.reset_stats()
        self.game_active = False   # 🚦 start screen
        self.game_won = False      # whether win
        self.high_score = 0

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.game_won = False

