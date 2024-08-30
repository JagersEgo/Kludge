import tkinter as tk
import pygame
import sys
from threading import Thread

def open_tkinter_window():
    root = tk.Tk()
    root.title("Tkinter Window")
    root.geometry("400x300")
    root.configure(bg='blue')
    root.mainloop()

def open_pygame_window():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Pygame Window")
    screen.fill((255, 0, 0))  # Red color
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
    pygame.quit()
    sys.exit()

# Run both windows in separate threads
if __name__ == "__main__":
    tkinter_thread = Thread(target=open_tkinter_window)
    pygame_thread = Thread(target=open_pygame_window)

    tkinter_thread.start()
    pygame_thread.start()

    tkinter_thread.join()
    pygame_thread.join()
