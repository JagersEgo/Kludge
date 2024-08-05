import pygame
import pygame.gfxdraw
import sys
from random import *
from hPyT import *
import ctypes

from resources import *
#from kludges import *

#print (title)

def draw_scrolling_grid(surface, bg_grid_offset_x, bg_grid_offset_y):
    block_size = 107  # Size of the grid blocks
    for x in range(-block_size, width + block_size, block_size):
        for y in range(-block_size, height + block_size, block_size):
            rect = pygame.Rect(x + bg_grid_offset_x, y + bg_grid_offset_y, block_size, block_size)
            pygame.draw.rect(surface, GREY, rect, 1)

def make_balls(amount):
    # Make this more robust later by taking a dictionary input of balls

    global balls

    for i in range(0,amount):
        angle = randint(0,360)
        velocities = angle_to_velocities(angle)

        x=width*uniform(0.05,0.95)
        y=height*uniform(0.05,0.95)

        for ball in balls:
            while ball.occupying(x,y):
                x=width*uniform(0.05,0.95)
                y=height*uniform(0.05,0.95)

        ball = Ball(x=x, y=y, radius=25, speeds=velocities)
        balls.append(ball)

# Ball class
class Ball:
    def __init__(self, x, y, radius, speeds, mass=20, filled=False, width=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = speeds[0]
        self.y_speed = speeds[1]
        self.colour = get_random_item(mocha)
        #mocha.remove(self.colour) ### temp

        self.mass = mass
        self.filled = filled
        self.width = width

        self.counter = 0
    
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
        xout, yout = False, False

        # Bounce off the edges
        if self.x - self.radius < 0 or self.x + self.radius > width:
            self.x_speed = -self.x_speed
            bounce_sound.play()
            self.counter += 1
            self.xout = True
        if self.y - self.radius < 0 or self.y + self.radius > height:
            self.y_speed = -self.y_speed
            bounce_sound.play()
            self.counter += 1
            self.yout = True

        if xout == True and yout == True:
            self.counter = 0

        if self.counter > 120:
            print ("Kludge stuck oob")
            #add check to see if middle is occupied
            self.x = 40
            self.y = 40
            self.counter = 0


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

    def occupying(self,x,y): # Is a point within the bounds of the circle
        saferad = self.radius+self.radius*1.5

        if self.x-saferad<x<self.x+saferad and self.y-saferad<y<self.y+saferad:
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
            pygame.gfxdraw.filled_ellipse(temp, self.radius, self.radius, self.radius - self.width, self.radius - self.width, BG)
            # Anti-aliased inner circle
            pygame.gfxdraw.aacircle(temp, self.radius, self.radius, self.radius - self.width, BG)
        
        surface.blit(temp, (int(self.x) - self.radius, int(self.y) - self.radius), None, pygame.BLEND_ADD)

    def hit(x, y):
        bounce_sound.play()

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1280,720 

window = pygame.display.set_mode((width, height))
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

caption = "Gelatinous Kludge | " + str(motds[randint(0,len(motds)-1)])
pygame.display.set_caption(caption)

hpyt_window = ctypes.windll.user32.GetActiveWindow()
maximize_minimize_button.hide(hpyt_window) # hides both maximize and minimize button
border_color.set(hpyt_window, (24, 24, 37))

hwnd = ctypes.windll.user32.GetActiveWindow()
title_bar_color.set(hwnd, '#181825')
#title_text_color.set(window, '#ff00ff')

# Define common vars
BG = (30, 30, 46)
WHITE = (255, 255, 255)
GREY = (24, 24, 37)

bg_grid_offset_x = 0
bg_grid_offset_y = 0
scroll_speed_x = 0.2
scroll_speed_y = 0.2

sounds = []
bounce_sound = pygame.mixer.Sound("saya_cute.ogg")
sounds.append(bounce_sound)
hit_sound = pygame.mixer.Sound("saya_kick_deeper.ogg")
sounds.append(hit_sound)
misc_sound = pygame.mixer.Sound("tok10.ogg")
sounds.append(misc_sound)
for sound in sounds:
    sound.set_volume(0.5) ######################################################################################################################################################

# Ball vars
balls = []

make_balls(7)

# Main game loop
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # Move the ball
    for ball in balls:
        
        for other_ball in balls:
        
            if ball != other_ball:
                ball.check_collision(other_ball)
        ball.move()
    
    # Clear the screen
    bg_grid_offset_x = (bg_grid_offset_x + scroll_speed_x) % 107
    bg_grid_offset_y = (bg_grid_offset_y + scroll_speed_y) % 107
    
    # Clear the screen
    window.fill(BG)
    
    # Draw the scrolling grid
    draw_scrolling_grid(window, bg_grid_offset_x, bg_grid_offset_y)

    # Draw the ball
    for ball in balls:
        ball.draw(window)
    

    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)
