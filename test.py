import pygame
import pygame.gfxdraw
import sys
from random import *
from hPyT import *
import ctypes

from resources import *

def draw_scrolling_grid(surface, bg_grid_offset_x, bg_grid_offset_y, block_size):
    for x in range(-2*block_size, width + block_size, block_size):
        for y in range(-2*block_size, height + block_size, block_size):
            rect = pygame.Rect(x + bg_grid_offset_x, y + bg_grid_offset_y, block_size, block_size)
            pygame.draw.rect(surface, GREY, rect, 1)

def make_balls(amount):
    global balls
    for i in range(0, amount):
        angle = randint(0, 360)
        velocities = angle_to_velocities(angle)

        x = width * uniform(0.05, 0.95)
        y = height * uniform(0.05, 0.95)

        for ball in balls:
            while ball.occupying(x, y):
                x = width * uniform(0.05, 0.95)
                y = height * uniform(0.05, 0.95)

        ball = Ball(x=x, y=y, radius=25, speeds=velocities)
        balls.append(ball)

class Ball:
    def __init__(self, x, y, radius, speeds, mass=20, filled=False, width=2):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = speeds[0] * 60  # Adjust speed factor as needed
        self.y_speed = speeds[1] * 60  # Adjust speed factor as needed
        self.colour = get_random_item(colours)

        self.mass = mass
        self.filled = filled
        self.width = width
        self.counter = 0
    
    def move(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        
        xout, yout = False, False

        if self.x - self.radius < 0:
            self.x = self.radius
            self.x_speed = -self.x_speed
            bounce_sound.play()
            self.counter += 1
            xout = True
        elif self.x + self.radius > width:
            self.x = width - self.radius
            self.x_speed = -self.x_speed
            bounce_sound.play()
            self.counter += 1
            xout = True

        if self.y - self.radius < 0:
            self.y = self.radius
            self.y_speed = -self.y_speed
            bounce_sound.play()
            self.counter += 1
            yout = True
        elif self.y + self.radius > height:
            self.y = height - self.radius
            self.y_speed = -self.y_speed
            bounce_sound.play()
            self.counter += 1
            yout = True

        if xout and yout:
            self.counter = 0

        if self.counter > 120:
            print("counter > 120")

    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        
        if distance < self.radius + other.radius:
            hit_sound.play()

            angle = math.atan2(dy, dx)
            sin_angle = math.sin(angle)
            cos_angle = math.cos(angle)
            
            v1 = (self.x_speed * cos_angle + self.y_speed * sin_angle,
                  self.y_speed * cos_angle - self.x_speed * sin_angle)
            v2 = (other.x_speed * cos_angle + other.y_speed * sin_angle,
                  other.y_speed * cos_angle - other.x_speed * sin_angle)
            
            self.x_speed, other.x_speed = v2[0] * cos_angle - v1[1] * sin_angle, v1[0] * cos_angle - v2[1] * sin_angle
            self.y_speed, other.y_speed = v2[0] * sin_angle + v1[1] * cos_angle, v1[0] * sin_angle + v2[1] * cos_angle

            overlap = 0.5 * (self.radius + other.radius - distance + 1)
            self.x += overlap * cos_angle
            self.y += overlap * sin_angle
            other.x -= overlap * cos_angle
            other.y -= overlap * sin_angle

    def occupying(self, x, y):
        saferad = self.radius + self.radius * 1.5
        if self.x - saferad < x < self.x + saferad and self.y - saferad < y < self.y + saferad:
            return True
        else:
            return False

    def draw(self, surface):
        pygame.gfxdraw.aacircle(surface, int(self.x), int(self.y), self.radius - 1, self.colour)
        pygame.gfxdraw.filled_ellipse(surface, int(self.x), int(self.y), self.radius - 1, self.radius - 1, self.colour)
        temp = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        if not self.filled:
            pygame.gfxdraw.filled_ellipse(temp, self.radius, self.radius, self.radius - self.width, self.radius - self.width, BG)
            pygame.gfxdraw.aacircle(temp, self.radius, self.radius, self.radius - self.width, BG)
        
        surface.blit(temp, (int(self.x) - self.radius, int(self.y) - self.radius), None, pygame.BLEND_ADD)

pygame.init()

width, height = 1280, 720
window = pygame.display.set_mode((width, height))
programIcon = pygame.image.load('icon.png')
pygame.display.set_icon(programIcon)

caption = "Gelatinous Kludge | " + str(motds[randint(0,len(motds)-1)])
pygame.display.set_caption(caption)

hpyt_window = ctypes.windll.user32.GetActiveWindow()
maximize_minimize_button.hide(hpyt_window)
border_color.set(hpyt_window, (24, 24, 37))

hwnd = ctypes.windll.user32.GetActiveWindow()
title_bar_color.set(hwnd, '#181825')

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
    sound.set_volume(0.5)

balls = []
make_balls(7)

clock = pygame.time.Clock()

while True:
    dt = clock.tick() / 1000.0  # Delta time in seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for ball in balls:
        for other_ball in balls:
            if ball != other_ball:
                ball.check_collision(other_ball)
        ball.move(dt)
    
    bg_grid_offset_x = (bg_grid_offset_x + scroll_speed_x * dt * 60) % 107
    bg_grid_offset_y = (bg_grid_offset_y + scroll_speed_y * dt * 60) % 107
    
    window.fill(BG)
    draw_scrolling_grid(window, bg_grid_offset_x, bg_grid_offset_y, 106)

    for ball in balls:
        ball.draw(window)

    pygame.display.flip()
