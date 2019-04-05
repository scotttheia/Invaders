import sys
import pygame
from blaster import Blaster
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, ship, blaster_rays):
    """Respond to key presses and mouse events."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_key_down(event, ai_settings, screen, ship, blaster_rays)
        elif event.type == pygame.KEYUP:
            check_key_up(event, ship)


def update_screen(ai_settings, screen, ship, aliens, blaster_rays):
    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    # Redraw all blaster rays behind ship and aliens.
    for ray in blaster_rays.sprites():
        ray.draw_blaster()

    ship.blitme()
    aliens.draw(screen)

    # Make the most recently drawn screen visible
    pygame.display.flip()


def check_key_down(event, ai_settings, screen, ship, blaster_rays):
    """Respond to key presses."""
    if event.key == pygame.K_RIGHT:
        # Move the ship to the right.
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # Move the ship to the right.
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a new blaster ray and add it to the blaster group
        fire_blaster(ai_settings, screen, ship, blaster_rays)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_blaster(ai_settings, screen, ship, blaster_rays):
    if len(blaster_rays) < ai_settings.blaster_rays_allowed:
        new_ray = Blaster(ai_settings, screen, ship)
        blaster_rays.add(new_ray)


def check_key_up(event, ship):
    """Respond to key releases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_rays(ai_settings, screen, ship, aliens, rays):
    # Get rid of bullets that have disappeared.
    for ray in rays:
        if ray.rect.bottom <= 0:
            rays.remove(ray)

    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, rays)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, rays):
    """Respond to bullet collisions."""
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(rays, aliens, True, True)

    if len(aliens) == 0:
        # Destroy existing bullets
        rays.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_of_aliens(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in a row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width

    alien = Alien(ai_settings, screen)
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a fleet full of aliens."""
    alien = Alien(ai_settings, screen)
    number_of_aliens_x = get_number_of_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row_number in range(number_rows):
        for alien_number in range(number_of_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def update_aliens(ai_settings, stats, screen, ship, aliens, blaster_rays):
    """Update the positions of all aliens in the fleet."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions.

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, blaster_rays)

    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, blaster_rays)


def ship_hit(ai_settings, stats, screen, ship, aliens, blaster_rays):
    """Respond to ship being hit by alien."""
    if stats.ships_left > 0:
        # Decrement ships_left.
        stats.ships_left -= 1

        # Empty the list of aliens and bullets.
        aliens.empty()
        blaster_rays.empty()

        # Create new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause.
        sleep(0.5)

    else:
        stats.game_active = False


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, blaster_rays):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if a ship got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, blaster_rays)
            break

