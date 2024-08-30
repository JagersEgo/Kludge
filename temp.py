import pygame
import pygame.gfxdraw
import sys
from random import *
from hPyT import *
import ctypes
import threading  # Import threading module

from resources import *

class Game:
    def __init__(self):
        # Initialize Pygame and set up the display
        pygame.init()
        self.width = 1280
        self.height = 720
        self.window = pygame.display.set_mode((self.width, self.height))
        self.BG = (30, 30, 46)
        self.GREY = (24, 24, 37)
        self.bg_grid_offset_x = 0
        self.bg_grid_offset_y = 0
        self.scroll_speed_x = 0.2
        self.scroll_speed_y = 0.2

        # Load sounds
        self.bounce_sound = pygame.mixer.Sound("saya_cute.ogg")
        self.hit_sound = pygame.mixer.Sound("saya_kick_deeper.ogg")

        # Initialize balls
        self.balls = []

        # Set window properties
        self.programIcon = pygame.image.load('icon.png')
        pygame.display.set_icon(self.programIcon)
        caption = "Gelatinous Kludge | " + str(motds[randint(0,len(motds)-1)])
        pygame.display.set_caption(caption)

        # Custom window modifications
        hpyt_window = ctypes.windll.user32.GetActiveWindow()
        maximize_minimize_button.hide(hpyt_window)
        border_color.set(hpyt_window, (24, 24, 37))
        hwnd = ctypes.windll.user32.GetActiveWindow()
        title_bar_color.set(hwnd, '#181825')

        # Create initial set of balls
        self.make_balls(7)

    def make_balls(self, amount):
        for i in range(amount):
            angle = randint(0, 360)
            velocities = self.angle_to_velocities(angle)
            x = self.width * uniform(0.05, 0.95)
            y = self.height * uniform(0.05, 0.95)

            for ball in self.balls:
                while ball.occupying(x, y):
                    x = self.width * uniform(0.05, 0.95)
                    y = self.height * uniform(0.05, 0.95)

            ball = Ball(x=x, y=y, radius=25, speeds=velocities, game=self)
            self.balls.append(ball)

    def angle_to_velocities(self, angle):
        # Implement the function to convert an angle to velocity components
        return [uniform(-1, 1), uniform(-1, 1)]

    def draw_scrolling_grid(self):
        block_size = 106  # Size of the grid blocks
        for x in range(-2 * block_size, self.width + block_size, block_size):
            for y in range(-2 * block_size, self.height + block_size, block_size):
                rect = pygame.Rect(x + self.bg_grid_offset_x, y + self.bg_grid_offset_y, block_size, block_size)
                pygame.draw.rect(self.window, self.GREY, rect, 1)

    def main_game_loop(self):
        clock = pygame.time.Clock()

        while True:
            self.dt = clock.tick() / 1000.0  # Delta time in seconds
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            for ball in self.balls:
                for other_ball in self.balls:
                    if ball != other_ball:
                        ball.check_collision(other_ball)
                ball.move(self.dt)

            self.bg_grid_offset_x = (self.bg_grid_offset_x + self.scroll_speed_x * self.dt * 60) % 107
            self.bg_grid_offset_y = (self.bg_grid_offset_y + self.scroll_speed_y * self.dt * 60) % 107

            self.window.fill(self.BG)
            self.draw_scrolling_grid()#self.window, self.bg_grid_offset_x, self.bg_grid_offset_y, 106)

            for ball in self.balls:
                ball.draw(self.window)

            pygame.display.flip()
                        

    def second_thread_function(self):
        # Placeholder for the second thread's function
        pass


class Ball:
    def __init__(self, x, y, radius, speeds, game):
        self.x = x
        self.y = y
        self.radius = radius
        self.x_speed = speeds[0] * 60  # Adjust speed factor as needed
        self.y_speed = speeds[1] * 60  # Adjust speed factor as needed
        self.colour = get_random_item(colours)
        self.game = game

        self.mass = 20
        self.filled = True
        self.width = 2
        self.counter = 0
    
    def move(self, dt):
        self.x += self.x_speed * dt
        self.y += self.y_speed * dt
        
        xout, yout = False, False

        if self.x - self.radius < 0:
            self.x = self.radius
            self.x_speed = -self.x_speed
            self.game.bounce_sound.play()
            self.counter += 1
            xout = True
        elif self.x + self.radius > self.game.width:
            self.x = self.game.width - self.radius
            self.x_speed = -self.x_speed
            self.game.bounce_sound.play()
            self.counter += 1
            xout = True

        if self.y - self.radius < 0:
            self.y = self.radius
            self.y_speed = -self.y_speed
            self.game.bounce_sound.play()
            self.counter += 1
            yout = True
        elif self.y + self.radius > self.game.height:
            self.y = self.game.height - self.radius
            self.y_speed = -self.y_speed
            self.game.bounce_sound.play()
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
            self.game.hit_sound.play()

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
if __name__ == "__main__":
    game = Game()

    # Create threads
    thread1 = threading.Thread(target=game.main_game_loop)
    thread2 = threading.Thread(target=game.second_thread_function)

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads to complete
    thread1.join()
    thread2.join()
