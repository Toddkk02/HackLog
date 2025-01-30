import pygame as pg
import os
import random
import time
from config import *

class BootSequence:
    def __init__(self):
        self.messages = [
            ("Initializing boot sequence...", WHITE),
            ("BIOS POST check completed", GREEN),
            ("Loading GRUB bootloader...", WHITE),
            ("Starting kernel initialization...", CYAN),
            ("Loading microcode firmware...", WHITE),
            ("Starting hardware detection...", MAGENTA),
            ("Detecting CPU: AMD Ryzen 9 5950X", WHITE),
            ("Memory check: 32GB DDR4", CYAN),
            ("Checking NVME drives...", WHITE),
            ("Mounting root filesystem...", RED),
            ("Starting system services...", WHITE),
            ("Loading network interfaces...", CYAN),
            ("Starting firewall service...", RED),
            ("Initializing graphics driver...", MAGENTA),
            ("Starting X server...", WHITE),
            ("Loading desktop environment...", GREEN),
            ("Starting system daemons...", WHITE),
            ("Initializing security modules...", RED),
            ("Loading user preferences...", CYAN),
            ("Checking system integrity...", WHITE),
            ("Starting SSH service...", MAGENTA),
            ("Initializing package manager...", WHITE),
            ("Loading system drivers...", CYAN),
            ("Starting audio subsystem...", WHITE),
            ("Initializing USB controllers...", RED),
            ("Loading user interface...", WHITE),
            ("Starting network manager...", MAGENTA),
            ("Checking file permissions...", WHITE),
            ("Loading system updates...", CYAN),
            ("Starting security service...", RED),
            ("System ready.", GREEN)
        ]
        self.tech_messages = [
            "[OK] Starting session {session_id}",
            "[OK] Mounted /dev/nvme0n1p{part}",
            "[OK] Started D-Bus System Message Bus",
            "[OK] Started Network Manager Script Dispatcher Service",
            "Starting Network Manager Wait Online...",
            "Starting Permit User Sessions...",
            "Starting Hold until boot process finishes up...",
            "Starting Network Time Synchronization...",
            "[OK] Reached target Network",
            "[OK] Reached target Host and Network Name Lookups",
            "Starting Authorization Manager...",
            "[OK] Started User Login Management",
            "[OK] Started Authorization Manager",
            "[OK] Created slice system-modprobe.slice",
            "[OK] Started System Logging Service",
            "Starting Accounts Service...",
            "[OK] Started Accounts Service",
            "Starting Modem Manager...",
            "[OK] Started Modem Manager",
            "Starting Privacy Service...",
            "[OK] Mounted FUSE Control File System",
            "[  OK  ] Mounted Kernel Debug File System",
            "[  OK  ] Started Job spooling tools",
            "Loading kernel modules...",
            "Activating swap /swapfile...",
            "Starting Bluetooth service...",
            "Starting WPA supplicant...",
            "Starting Disk Manager...",
            "Starting Power Manager...",
            "Starting Printer service...",
        ]
        self.current_line = 0
        self.lines = []
        self.font = pg.font.SysFont("monospace", 16)
        
    def update(self):
        if self.current_line < len(self.messages):
            message, color = self.messages[self.current_line]
            self.lines.append((message, color))
            self.current_line += 1
            
            for _ in range(random.randint(1, 3)):
                tech_message = random.choice(self.tech_messages)
                tech_message = tech_message.replace("{session_id}", str(random.randint(1000, 9999)))
                tech_message = tech_message.replace("{part}", str(random.randint(1, 5)))
                color = random.choice([WHITE, CYAN, MAGENTA, RED])
                self.lines.append((tech_message, color))
                
        if len(self.lines) > 25:
            self.lines.pop(0)
            
    def draw(self, screen):
        screen.fill(BLACK)
        y = 30
        for message, color in self.lines:
            text = self.font.render(message, True, color)
            screen.blit(text, (30, y))
            y += 20
        pg.display.flip()

def main_menu():
    global player_name
    font_menu = pg.font.SysFont("monospace", 50)
    font_input = pg.font.SysFont("monospace", 30)
    
    player_name = ""
    hostname = ""
    input_active = "player_name"
    player_name_rect = pg.Rect(200, 200, 400, 50)
    hostname_rect = pg.Rect(200, 300, 400, 50)
    
    input_boxes = {
        "player_name": player_name_rect,
        "hostname": hostname_rect
    }

    running = True
    while running:
        screen.fill(BLACK)
        label = font_menu.render("HackLog!", True, GREEN)
        screen.blit(label, (screen_width / 4, 100))

        pg.draw.rect(screen, GREEN if input_active == "player_name" else GRAY, player_name_rect, 2)
        pg.draw.rect(screen, GREEN if input_active == "hostname" else GRAY, hostname_rect, 2)

        player_name_surface = font_input.render(player_name, True, GREEN)
        hostname_surface = font_input.render(hostname, True, GREEN)

        screen.blit(player_name_surface, (player_name_rect.x + 10, player_name_rect.y + 10))
        screen.blit(hostname_surface, (hostname_rect.x + 10, hostname_rect.y + 10))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    exit()
                
                if event.key == pg.K_TAB:
                    input_active = "hostname" if input_active == "player_name" else "player_name"
                elif event.key == pg.K_RETURN:
                    if input_active == "player_name":
                        input_active = "hostname"
                    elif input_active == "hostname" and hostname and player_name:
                        save_config(player_name, hostname)
                        show_boot_sequence()
                        running = False
                elif event.key == pg.K_BACKSPACE:
                    if input_active == "player_name":
                        player_name = player_name[:-1]
                    else:
                        hostname = hostname[:-1]
                else:
                    if input_active == "player_name" and len(player_name) < 20:
                        player_name += event.unicode
                    elif input_active == "hostname" and len(hostname) < 20:
                        hostname += event.unicode

        player_name_label = font_input.render("Player Name:", True, GREEN)
        hostname_label = font_input.render("Hostname:", True, GREEN)

        screen.blit(player_name_label, (player_name_rect.x, player_name_rect.y - 40))
        screen.blit(hostname_label, (hostname_rect.x, hostname_rect.y - 40))

        pg.display.update()

def save_config(player_name, hostname):
    with open("assets/config/config.txt", 'w') as file:
        file.write(f"Player Name: {player_name}\n")
        file.write(f"Hostname: {hostname}\n")

def show_boot_sequence():
    boot = BootSequence()
    clock = pg.time.Clock()
    fade = pg.Surface((screen_width, screen_height))
    fade.fill(BLACK)
    
    for _ in range(100):
        boot.update()
        boot.draw(screen)
        pg.time.delay(50)
        clock.tick(30)
    
    for alpha in range(0, 255, 5):
        fade.set_alpha(alpha)
        screen.blit(fade, (0,0))
        pg.display.flip()
        pg.time.delay(5)