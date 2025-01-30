import pygame as pg
import random
from config import *
from terminal import Terminal
from browser import Browser

class Desktop:
    def __init__(self):
        self.terminals = []
        self.browsers = []
        self.screen = screen
        self.background = None
        self.dash_to_dock = None
        # Initialize button rects
        self.app_button_rect = pg.Rect(0, 0, 0, 0)
        self.terminal_button_rect = pg.Rect(0, 0, 0, 0)
        self.browser_button_rect = pg.Rect(0, 0, 0, 0)
        self.load_images()
        # Do initial draw to set up button positions
        self.setup_buttons()

    def load_images(self):
        try:
            self.background = pg.image.load("assets/images/pc_background.png")
            self.background = pg.transform.scale(self.background, (screen_width, screen_height))
            
            original_dock = pg.image.load("assets/images/dash_to_dock.png")
            dock_height = int(screen_height * 0.08)
            dock_width = int(dock_height * (original_dock.get_width() / original_dock.get_height()))
            self.dash_to_dock = pg.transform.scale(original_dock, (dock_width, dock_height))
        except pg.error as e:
            print(f"Errore nel caricamento delle immagini: {e}")
            # Fallback a superfici colorate in caso di errore
            self.background = pg.Surface((screen_width, screen_height))
            self.background.fill(LIGHT_GRAY)
            self.dash_to_dock = pg.Surface((int(screen_width * 0.8), int(screen_height * 0.08)))
            self.dash_to_dock.fill(GRAY)

    def setup_buttons(self):
        dock_width, dock_height = self.dash_to_dock.get_size()
        dock_x = (screen_width - dock_width) // 2
        dock_y = screen_height - dock_height - 10
        button_size = int(dock_height * 0.8)
        
        # Terminal button at fixed position (750, 850)
        self.terminal_button_rect = pg.Rect(740, 820, button_size, button_size)
        # Browser button at fixed position (570, 850)
        self.browser_button_rect = pg.Rect(570, 820, button_size, button_size)
        
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
        terminal = Terminal(x=x, y=y)
        self.terminals.append(terminal)
        return terminal

    def create_browser(self):
        x = 300 + len(self.browsers) * 30
        y = 150 + len(self.browsers) * 30
        if len(self.browsers) > 5:
            x = random.randint(0, screen_width - 600)
            y = random.randint(0, screen_height - 400)
        browser = Browser(self, x=x, y=y)
        self.browsers.append(browser)
        return browser

    def handle_events(self, event):
        # Handle terminal events
        for terminal in self.terminals[:]:
            if terminal.handle_event(event):
                self.terminals.remove(terminal)
                
        # Handle browser events
        for browser in self.browsers[:]:
            browser.handle_event(event)
            # Qui puoi aggiungere la logica per rimuovere i browser se necessario
            # similar to terminals if you implement a close functionality

    def draw(self, screen):
        # Draw background
        screen.blit(self.background, (0, 0))
        
        # Draw dock
        dock_width, dock_height = self.dash_to_dock.get_size()
        dock_x = (screen_width - dock_width) // 2
        dock_y = screen_height - dock_height - 10
        screen.blit(self.dash_to_dock, (dock_x, dock_y))
        
        # Draw buttons
        self.draw_buttons(screen, dock_x, dock_y, dock_width, dock_height)
        
        # Draw all windows
        for terminal in self.terminals:
            terminal.draw(screen)
        for browser in self.browsers:
            browser.draw()

    def draw_buttons(self, screen, dock_x, dock_y, dock_width, dock_height):
        button_size = int(dock_height * 0.8)
        # Uncomment for debugging button positions
        pg.draw.rect(screen, (255, 0, 0), self.browser_button_rect, 2)
        #pg.draw.rect(screen, (255, 0, 0, 128), self.terminal_button_rect, 2)
        #pg.draw.rect(screen, (0, 255, 0, 128), self.app_button_rect, 2)