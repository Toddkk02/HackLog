import pygame as pg
from pygame import *
from config import *
from terminal import Terminal
from Desktop import Desktop
from menu import *
from browser import *
import time
import random
import os

def main():
    pg.init()
    screen = pg.display.set_mode((screen_width, screen_height))
    pg.display.set_caption("Linux Desktop")
    
    if os.path.exists("assets/config/config.txt"):
        show_boot_sequence()
    else:
        main_menu()
    
    # Add this line to start the desktop after boot sequence
    start_desktop()

def start_desktop():
    desktop = Desktop()
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    toggle_applications(desktop)
            if event.type == MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                if desktop.app_button_rect.collidepoint(pos):
                    toggle_applications(desktop)
                elif desktop.terminal_button_rect.collidepoint(pos):
                    desktop.create_terminal()
                elif desktop.browser_button_rect.collidepoint(pos):
                    # Modifica questa parte
                    desktop.create_browser()  # Usa il metodo della classe Desktop
            
            # Gestisci gli eventi per tutte le finestre
            desktop.handle_events(event)
            
            if event.type == MOUSEMOTION:
                pos = pg.mouse.get_pos()
                #print(pos)
                
        desktop.draw(screen)
        pg.display.flip()
        clock.tick(60)
def toggle_applications(desktop):
    global app_image_menu
    try:
        app_image_menu = pg.image.load("assets/images/application.png")
        app_image_menu = pg.transform.scale(app_image_menu, (screen_width, screen_height))
    except pg.error as e:
        print(f"Error loading application.png: {e}")
        app_image_menu = pg.Surface((screen_width, screen_height))
        app_image_menu.fill((50, 50, 50))

    # Fade in animation
    time_to_open = 0.2
    while time_to_open > 0:
        screen.blit(desktop.background, (0, 0))
        app_image_menu.set_alpha(int((1 - time_to_open / 0.2) * 255))
        screen.blit(app_image_menu, (0, 0))
        pg.display.flip()
        time_to_open -= 0.01
        pg.time.Clock().tick(60)

    # Applications menu loop
    running = True
    while running:
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        screen.blit(desktop.background, (0, 0))
        screen.blit(app_image_menu, (0, 0))
        pg.display.flip()

if __name__ == "__main__":
    main()