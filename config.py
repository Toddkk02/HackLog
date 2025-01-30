import pygame as pg
import os

# Screen settings
screen_width = 1600
screen_height = 900
quarter_of_screen = screen_width / 4

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (83, 83, 83)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize pygame and screen
pg.init()
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("HackLog")

# Global variables
is_desktop = True
menu_background = None
app_image_menu = None
internet_connections = False

# Create assets directory if it doesn't exist
if not os.path.exists("assets/config"):
    os.makedirs("assets/config")