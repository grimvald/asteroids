import pygame

from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS

class Shot (CircleShape):
    """Represents a bullet fired by the player."""
    def __init__(self, x: float, y: float) -> None:
        super().__init__(x,y, SHOT_RADIUS)
    

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
        """Moves the bullet in a straight line based on its velocity and delta time."""
        self.position += self.velocity * dt
        
