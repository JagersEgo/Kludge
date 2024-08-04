from resources import *

# Ball class
class Ball:
    def __init__(self, x, y, radius, speeds, mass=20, filled=True, width=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = speeds[0]
        self.y_speed = speeds[1]
        self.colour = get_random_item(mocha)
        self.mass = mass
        self.filled = filled
        self.width = width
    
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
        # Bounce off the edges
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.x_speed = -self.x_speed
            bounce_sound.play()
        if self.y - self.radius < 0 or self.y + self.radius > height:
            self.y_speed = -self.y_speed
            bounce_sound.play()
            
    def check_collision(self, other):
        # Calculate the distance between the balls
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        
        if distance < self.radius + other.radius:
            hit_sound.play()
            # Calculate the angle of collision
            angle = math.atan2(dy, dx)
            sin_angle = math.sin(angle)
            cos_angle = math.cos(angle)
            
            # Rotate the velocity components to align with the collision axis
            v1 = (self.x_speed * cos_angle + self.y_speed * sin_angle,
                  self.y_speed * cos_angle - self.x_speed * sin_angle)
            v2 = (other.x_speed * cos_angle + other.y_speed * sin_angle,
                  other.y_speed * cos_angle - other.x_speed * sin_angle)
            
            # Swap the velocity components
            self.x_speed, other.x_speed = v2[0] * cos_angle - v1[1] * sin_angle, v1[0] * cos_angle - v2[1] * sin_angle
            self.y_speed, other.y_speed = v2[0] * sin_angle + v1[1] * cos_angle, v1[0] * sin_angle + v2[1] * cos_angle

    def occupying(coords): # Is a point within the bounds of the circle
        x, y = coords
        if self.x-radius<x<self.x+radius and self.y-radius<y<self.y+radius:
            return True
        else:
            return False

    def _draw(self, surface): # Old unaliased draw
        pygame.draw.circle(surface, self.colour, (self.x, self.y), self.radius)

    def draw(self, surface): # shamelessly stoled from https://abarry.org/antialiased-rings-filled-circles-in-pygame/
        # Anti-aliased outer circle
        pygame.gfxdraw.aacircle(surface, int(self.x), int(self.y), self.radius - 1, self.colour)
        
        # Filled outer circle
        pygame.gfxdraw.filled_ellipse(surface, int(self.x), int(self.y), self.radius - 1, self.radius - 1, self.colour)
        
        # Temporary surface for inner circle
        temp = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        if not self.filled:
            # Inner background color circle
            pygame.gfxdraw.filled_ellipse(temp, self.radius, self.radius, self.radius - self.width, self.radius - self.width, BG_ALPHA_COLOR)
            # Anti-aliased inner circle
            pygame.gfxdraw.aacircle(temp, self.radius, self.radius, self.radius - self.width, BG_ALPHA_COLOR)
        
        surface.blit(temp, (int(self.x) - self.radius, int(self.y) - self.radius), None, pygame.BLEND_ADD)

    def hit(x, y):
        bounce_sound.play()