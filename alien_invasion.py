import sys
import pygame
from pygame.sprite import Group
from ship import Ship
from alien import Alien
import game_functions as gf
import settings as st
from game_stats import GameStats


def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = st.Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)

    # Make ship, a group of bullets, and a fleet of aliens.
    ship = Ship(ai_settings, screen)
    blaster_rays = Group()
    aliens = Group()

    # Create a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # start the main loop for the game
    while True:
        gf.check_events(ai_settings, screen, ship, blaster_rays)

        if stats.game_active:
            ship.update()
            blaster_rays.update()
            gf.update_rays(ai_settings, screen, ship, aliens, blaster_rays)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, blaster_rays)

        gf.update_screen(ai_settings, screen, ship, aliens, blaster_rays)

run_game()
