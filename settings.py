class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize Game Settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # Ship settings
        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        # Blaster settings
        self.blaster_speed_factor = 4
        self.blaster_width = 3
        self.blaster_height = 15
        self.blaster_color = 100, 10, 5
        self.blaster_rays_allowed = 6

        # Alien settings
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10
        # fleet_direction of 1 represents right; -1 represents left
        self.fleet_direction = 1
