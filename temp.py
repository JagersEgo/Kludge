import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Bouncing Ball")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Ball class
class Ball:
    def __init__(self, x, y, radius, x_speed, y_speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = x_speed
        self.y_speed = y_speed
    
    def move(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        
        # Bounce off the edges
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.x_speed = -self.x_speed
        if self.y - self.radius < 0 or self.y + self.radius > height:
            self.y_speed = -self.y_speed
    
    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)

# Create a ball instance
ball = Ball(x=width//2, y=height//2, radius=20, x_speed=300, y_speed=300)

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Calculate delta time
    dt = clock.tick() / 1000.0  # Convert milliseconds to seconds
    
    # Move the ball
    ball.move(dt)
    
    # Clear the screen
    window.fill(BLACK)
    
    # Draw the ball
    ball.draw(window)
    
    # Update the display
    pygame.display.flip()
