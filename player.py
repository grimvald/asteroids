import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
    """Represents the player's ship, handling its geometry, rendering, rotation, and input controls."""
    
    def __init__(self, x: float, y: float) -> None:
        # Initialize the base CircleShape with coordinates and player radius
        super().__init__(x, y, PLAYER_RADIUS)
        # Initialize the ship's rotation angle to 0 degrees (pointing straight up/forward)
        self.rotation = 0.0
        #Cooldown timer for firing
        self.shoot_timer = 0.0

    def triangle(self) -> list[pygame.Vector2]:
        """Calculates and returns the 3 vertex coordinates of the player's triangular ship based on its position and rotation."""
        # Create a vector pointing forward from the ship, rotated by the current angle
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Create a vector pointing right, scaled to shape the base width of the triangle
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        
        # Calculate the three vertex points: tip (a), bottom-left (b), and bottom-right (c)
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen: pygame.Surface) -> None:
        """Renders the player ship's wireframe polygon onto the game display surface."""
        pygame.draw.polygon(screen, "White", self.triangle(), LINE_WIDTH)

    def rotate(self, dt: float) -> None:
        """Adjusts the player's rotation angle using turn speed and delta time (dt) for smooth movement."""
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        """Calculates direction and updates player position based on speed and delta"""
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        """Fires a new shot from the player's position if the cooldown timer has expired."""
        if self.shoot_timer > 0:
            return

        self.shoot_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt: float) -> None:
        """Polls keyboard input each frame to handle rotation, motion, firingm cooldown timer  controls."""
        if self.shoot_timer > 0:
            self.shoot_timer -= dt    

        keys = pygame.key.get_pressed()

        # Handle rotation inputs (A and D keys)
        if keys[pygame.K_a]:
            self.rotate(-dt)

        if keys[pygame.K_d]:
            self.rotate(dt)

        # Handle movement inputs (W and S keys)
        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move(-dt)
        
        # Handle firing input (spacebar)
        if keys[pygame.K_SPACE]:
            self.shoot()
