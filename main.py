import sys
import pygame
from asteroid import Asteroid
from asteroidfield import AsteroidField
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from shot import Shot


def main():
    # Print startup version info and screen configuration details
    print(f"Starting Asteroids with pygame version {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    # Initialize all imported pygame modules
    pygame.init()

    # Initialize the game clock and delta time (dt) variable for smooth movement
    clock = pygame.time.Clock()
    dt = 0.0
    
    # Instantiate the player object in the center of the screen window
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    # Create the main game display window using width and height constants
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    #Create sprite groups for updatable drawable objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    #Asign the groups to the Player class containers attribute
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # Instantiate the player (automatically added to containers due to group assignment)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    # Main game loop running continuously until the window is closed
    while True:
        # Log the state of the game for debugging and history tracking
        log_state()
        
        # Iterate through and process user events from the pygame event queue
        for event in pygame.event.get():
            # Check if the user clicked the window close button
            if event.type == pygame.QUIT:
                return  # Exit the game loop and shut down

        # Update all objects in the updatable group
        updatable.update(dt)        
        
        #Check for collision between player and any asteroid
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game over!")
                sys.exit()

        # Check fro collision between shots and asteroids
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()
                    asteroid.split()
                
        # Clear the frame by filling the screen surface with solid black
        screen.fill("black")

        # Draw all objects in the drawable group
        for sprite in drawable:
            sprite.draw(screen)       

        # Refresh the display to show everything drawn during this frame
        pygame.display.flip()
    
        # Limit the frame rate to 60 FPS and calculate delta time (dt) in seconds
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
