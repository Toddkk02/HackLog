import pygame as pg
import os
from config import *
from memory import *

class Terminal:
    def __init__(self, width=500, height=300, x=400, y=200):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = pg.Surface((width, height))
        self.rect = pg.Rect((x, y, width, height))
        self.dragging = False
        self.drag_offset = (0, 0)
        self.font = pg.font.SysFont("Fira Code Medium", 16)
        self.surface.fill((40, 40, 40))
        
        # Input handling
        self.current_input = ""
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_time = 500  # milliseconds
        
        # Command history
        self.command_history = []
        self.history_index = 0
        self.lines = []
        self.scroll_offset = 0
        self.line_height = 20
        
        # CTRL state
        self.ctrl_pressed = False
        
        self._load_config()
        self._create_title_bar()
        self.add_new_prompt()

    def _load_config(self):
        try:
            with open("assets/config/config.txt", "r") as file:
                lines = file.readlines()
                self.player_name = lines[0].split(":")[1].strip()
                self.hostname = lines[1].split(":")[1].strip()
                global current_path
                current_path = update_filesystem(self.player_name)
        except:
            self.player_name = "unknown"
            self.hostname = "localhost"
            current_path = update_filesystem(self.player_name)

    def _create_title_bar(self):
        self.title_bar_height = 30
        title_bar = pg.Surface((self.width, self.title_bar_height))
        title_bar.fill((60,60,60))
        
        self.close_button = pg.Surface((20,20))
        self.close_button.fill((255,95,87))
        self.close_button_rect = pg.Rect(5,5,20,20)
        title_bar.blit(self.close_button, self.close_button_rect)
        
        title_text = self.font.render(f"{self.hostname} - Terminal", True, WHITE)
        title_bar.blit(title_text, (35, 8))
        
        self.surface.blit(title_bar, (0, 0))

    def add_new_prompt(self):
        prompt = f"{self.player_name}@{self.hostname}:~$ "
        self.lines.append(("prompt", prompt))
        # Auto-scroll when adding new prompt
        max_scroll = max(0, len(self.lines) * self.line_height - (self.height - self.title_bar_height))
        self.scroll_offset = max_scroll

    def add_output(self, text, color=WHITE):
        for line in text.split('\n'):
            self.lines.append(("output", line, color))
        # Auto-scroll when adding output
        max_scroll = max(0, len(self.lines) * self.line_height - (self.height - self.title_bar_height))
        self.scroll_offset = max_scroll

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = (event.pos[0] - self.x, event.pos[1] - self.y)
            
            if event.button == 4:  # Mouse wheel up
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.button == 5:  # Mouse wheel down
                max_scroll = max(0, len(self.lines) * self.line_height - (self.height - self.title_bar_height))
                self.scroll_offset = min(self.scroll_offset + 1, max_scroll)
            
            if self.close_button_rect.collidepoint(mouse_pos) and mouse_pos[1] < self.title_bar_height:
                return True
                
            if mouse_pos[1] < self.title_bar_height:
                self.dragging = True
                self.drag_offset = (event.pos[0] - self.x, event.pos[1] - self.y)
        
        elif event.type == pg.MOUSEBUTTONUP:
            self.dragging = False
            
        elif event.type == pg.MOUSEMOTION and self.dragging:
            new_x = event.pos[0] - self.drag_offset[0]
            new_y = event.pos[1] - self.drag_offset[1]
            
            new_x = max(0, min(new_x, screen_width - self.width))
            new_y = max(0, min(new_y, screen_height - self.height))
            
            self.x = new_x
            self.y = new_y
            self.rect.x = new_x
            self.rect.y = new_y
            
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                self.ctrl_pressed = True
            
            elif self.ctrl_pressed and event.key == pg.K_c:
                self.current_input = ""
                self.add_output("^C")
                self.add_new_prompt()
            
            elif event.key == pg.K_RETURN:
                if self.current_input:
                    self.command_history.append(self.current_input)
                    self.history_index = len(self.command_history)
                    self.execute_command(self.current_input)
                self.current_input = ""
                self.add_new_prompt()
            
            elif event.key == pg.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            
            elif event.key == pg.K_UP:
                if self.history_index > 0:
                    self.history_index -= 1
                    self.current_input = self.command_history[self.history_index]
            
            elif event.key == pg.K_DOWN:
                if self.history_index < len(self.command_history):
                    self.history_index += 1
                    self.current_input = self.command_history[self.history_index] if self.history_index < len(self.command_history) else ""
            
            else:
                if not self.ctrl_pressed and event.unicode:
                    self.current_input += event.unicode
        
        elif event.type == pg.KEYUP:
            if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                self.ctrl_pressed = False
        
        return False

    def execute_command(self, command):
        global current_path
        self.lines.append(("input", command))
        
        # Calculate the maximum possible scroll offset based on content
        max_scroll = max(0, len(self.lines) * self.line_height - (self.height - self.title_bar_height))
        # Set scroll to maximum to show latest content
        self.scroll_offset = max_scroll
        
        if command == "clear":
            self.lines = []
        elif command.startswith("cd"):
            parts = command.split()
            if len(parts) > 1:
                new_dir = parts[1].strip()
                # Handle special case for home directory
                if new_dir == "~":
                    new_dir = f"/home/{self.player_name}"
                # Handle special case for parent directory
                elif new_dir == "..":
                    current_parts = current_path.split("/")
                    if len(current_parts) > 1:  # Make sure we're not at root
                        new_dir = "/".join(current_parts[:-1])
                        if new_dir == "":  # Handle case when we reach root
                            new_dir = "/"
                else:
                    # Normalize the path
                    if not new_dir.startswith("/"):
                        new_dir = f"{current_path}/{new_dir}"
                    # Clean up any double slashes
                    new_dir = new_dir.replace('//', '/')
                    
                if new_dir in linux_file_system:
                    current_path = new_dir
                    self.add_output(f"Changed directory to '{current_path}'", GREEN)
                else:
                    self.add_output(f"cd: {new_dir}: No such file or directory", RED)
            else:
                # cd without arguments goes to user's home directory
                home_dir = f"/home/{self.player_name}"
                if home_dir in linux_file_system:
                    current_path = home_dir
                    self.add_output(f"Changed directory to '{current_path}'", GREEN)
                else:
                    self.add_output(f"cd: Home directory not found", RED)
        
        elif command.startswith("mkdir "):
            parts = command.split()
            if len(parts) > 1:
                new_dir = parts[1].strip()
                if not new_dir.startswith("/"):
                    new_dir = f"{current_path}/{new_dir}"
                # Clean up any double slashes
                new_dir = new_dir.replace('//', '/')
                
                if new_dir in linux_file_system:
                    self.add_output(f"mkdir: cannot create directory '{new_dir}': File exists", RED)
                else:
                    parent_dir = "/".join(new_dir.split("/")[:-1])
                    if parent_dir in linux_file_system:
                        linux_file_system[new_dir] = []
                        # Add the new directory name to its parent's listing
                        dir_name = new_dir.split("/")[-1]
                        if dir_name not in linux_file_system[parent_dir]:
                            linux_file_system[parent_dir].append(dir_name)
                        self.add_output(f"Directory '{new_dir}' created successfully", GREEN)
                    else:
                        self.add_output(f"mkdir: cannot create directory '{new_dir}': No such file or directory", RED)
            else:
                self.add_output("mkdir: missing operand", RED)
        
        elif command.startswith("ls"):
            parts = command.split()
            path = current_path  # Default to current path if no path specified
            
            if len(parts) > 1:
                path_arg = parts[1].strip()
                # Handle home directory shortcut
                if path_arg == "~":
                    path = f"/home/{self.player_name}"
                # Handle parent directory
                elif path_arg == "..":
                    path_parts = current_path.split("/")
                    if len(path_parts) > 1:
                        path = "/".join(path_parts[:-1])
                        if path == "":
                            path = "/"
                else:
                    # Normalize the path
                    if not path_arg.startswith('/'):
                        path = f"{current_path}/{path_arg}"
                    path = path.replace('//', '/')
            
            if path in linux_file_system:
                files = linux_file_system[path]
                if files:
                    self.add_output("  ".join(files), GREEN)
                else:
                    self.add_output("Directory is empty", WHITE)
            else:
                self.add_output(f"ls: cannot access '{path}': No such file or directory", RED)
        
        elif command == "help":
            self.add_output("Available commands:", CYAN)
            self.add_output("  clear - Clear the terminal")
            self.add_output("  help - Show this help message")
            self.add_output("  echo [text] - Display text")
            self.add_output("  ls [path] - List directory contents")
            self.add_output("  mkdir [dir] - Create a new directory")
            self.add_output("  cd [dir] - Change directory")
            self.add_output("  exit - Close the terminal")
        
        elif command.startswith("echo "):
            self.add_output(command[5:])
        
        elif command == "exit":
            return True
        
        else:
            self.add_output(f"Command not found: {command}", RED)
        
        # Update scroll offset again after adding all output
        max_scroll = max(0, len(self.lines) * self.line_height - (self.height - self.title_bar_height))
        self.scroll_offset = max_scroll

    def draw(self, screen):
        self.surface.fill((40, 40, 40))
        self._create_title_bar()
        
        y = self.title_bar_height - self.scroll_offset
        
        for i, (line_type, *line_content) in enumerate(self.lines[:-1]):
            if line_type == "prompt":
                text = self.font.render(line_content[0], True, CYAN)
            elif line_type == "input":
                text = self.font.render(line_content[0], True, WHITE)
            else:  # output
                text = self.font.render(line_content[0], True, line_content[1])
            
            if self.title_bar_height <= y < self.height:
                self.surface.blit(text, (10, y))
            y += self.line_height
        
        if self.lines:
            last_line = self.lines[-1]
            if last_line[0] == "prompt":
                prompt = last_line[1]
                prompt_text = self.font.render(prompt, True, CYAN)
                if self.title_bar_height <= y < self.height:
                    self.surface.blit(prompt_text, (10, y))
                
                if self.current_input:
                    input_text = self.font.render(self.current_input, True, WHITE)
                    input_x = 10 + self.font.size(prompt)[0]
                    self.surface.blit(input_text, (input_x, y))
                
                if self.cursor_visible:
                    cursor_x = 10 + self.font.size(prompt + self.current_input)[0]
                    if self.title_bar_height <= y < self.height:
                        pg.draw.line(self.surface, WHITE, 
                                   (cursor_x, y), 
                                   (cursor_x, y + self.line_height - 2))
        
        current_time = pg.time.get_ticks()
        if current_time - self.cursor_timer > self.cursor_blink_time:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = current_time
        
        screen.blit(self.surface, (self.x, self.y))
        pg.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height), 2)