class GameStats:
    """Tracks statistics for Invasion."""

    def reset_stats(self):
        """Initialize the statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit

    def __init__(self, ai_settings):
        """Initialize statistics."""
        self.ai_settings = ai_settings
        self.reset_stats()

        # Start alien invasion in an active state.
        self.game_active = False

