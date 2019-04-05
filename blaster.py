import pygame
from pygame.sprite import Sprite

class Blaster(Sprite):
    """A class to manage blaster rays fired from the ship"""

    def __init__(self, ai_settings, screen, ship):
        """Create a blaster object at the ship's current positions"""
        super().__init__()
        self.screen = screen

        # Create blaster ray rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, ai_settings.blaster_width, ai_settings.blaster_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Store blaster ray's position as a decimal value
        self.y = float(self.rect.y)

        self.color = ai_settings.blaster_color
        self.speed_factor = ai_settings.blaster_speed_factor

    def update(self):
        """Move the blaster ray up the screen."""
        # Update the decimal position of the bullet.
        self.y -= self.speed_factor
        # Update the rect position.
        self.rect.y = self.y

    def draw_blaster(self):
        """Draw the blaster ray to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)
