import pygame as pg
import random
from config import *
from terminal import Terminal

class Desktop:
    def __init__(self):
        self.terminals = []
        self.background = None
        self.dash_to_dock = None
        # Initialize button rects
        self.app_button_rect = pg.Rect(0, 0, 0, 0)
        self.terminal_button_rect = pg.Rect(0, 0, 0, 0)
        self.load_images()
        # Do initial draw to set up button positions
        self.setup_buttons()
        
    def load_images(self):
        self.background = pg.image.load("assets/images/pc_background.png")
        self.background = pg.transform.scale(self.background, (screen_width, screen_height))
        
        original_dock = pg.image.load("assets/images/dash_to_dock.png")
        dock_height = int(screen_height * 0.08)
        dock_width = int(dock_height * (original_dock.get_width() / original_dock.get_height()))
        self.dash_to_dock = pg.transform.scale(original_dock, (dock_width, dock_height))

    def setup_buttons(self):
        dock_width, dock_height = self.dash_to_dock.get_size()
        dock_x = (screen_width - dock_width) // 2
        dock_y = screen_height - dock_height - 10
        
        button_size = int(dock_height * 0.8)
        
        # Terminal button at fixed position (750, 850)
        self.terminal_button_rect = pg.Rect(740, 820, button_size, button_size)
        
        # App button
        app_x = dock_x + dock_width - (dock_width * 0.1) - button_size
        app_y = dock_y + (dock_height - button_size) // 2
        self.app_button_rect = pg.Rect(app_x, app_y, button_size, button_size)
    
    def create_terminal(self):
        x = 400 + len(self.terminals) * 30
        y = 200 + len(self.terminals) * 30
        if len(self.terminals) > 5:
            x = random.randint(0, screen_width - 500)
            y = random.randint(0, screen_height - 300)
        self.terminals.append(Terminal(x=x, y=y))
    
    def handle_events(self, event):
        for terminal in self.terminals[:]:
            if terminal.handle_event(event):
                self.terminals.remove(terminal)
    
    def draw(self, screen):
        screen.blit(self.background, (0, 0))
        
        dock_width, dock_height = self.dash_to_dock.get_size()
        dock_x = (screen_width - dock_width) // 2
        dock_y = screen_height - dock_height - 10
        
        screen.blit(self.dash_to_dock, (dock_x, dock_y))
        self.draw_buttons(screen, dock_x, dock_y, dock_width, dock_height)
        
        for terminal in self.terminals:
            terminal.draw(screen)
    
    def draw_buttons(self, screen, dock_x, dock_y, dock_width, dock_height):
        button_size = int(dock_height * 0.8)
        
        # Draw debug rectangles
        #pg.draw.rect(screen, (255, 0, 0, 128), self.terminal_button_rect, 2)
        # pg.draw.rect(screen, (0, 255, 0, 128), self.app_button_rect, 2)