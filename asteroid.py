import random
import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    """Represents an asteroid obstacle that moves across the screen and damages the player."""

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the asteroid circle onto the game screen."""
        pygame.draw.circle(
            screen,
            "white",
            (int(self.position.x), int(self.position.y)),
            self.radius,
            LINE_WIDTH,
        )

    def update(self, dt: float) -> None:
        """Moves the asteroid in a straight line based on its velocity and delta time."""
        self.position += self.velocity * dt

    def split(self) -> None:
        """Destroys the current asteroid and spawns two smaller ones if above minimum size."""
        self.kill()
        
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        log_event("asteroid_split")

        angle = random.uniform(20, 50)
        
        vel1 = self.velocity.rotate(angle) * 1.2
        vel2 = self.velocity.rotate(-angle) * 1.2

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = vel1

        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2.velocity = vel2

        
