# task.py
import pygame as pg
from config import *

class Task:
    def __init__(self, title, description, xp_reward, detailed_explanation, required_commands=None):
        self.title = title
        self.description = description
        self.xp_reward = xp_reward
        self.detailed_explanation = detailed_explanation
        self.completed = False
        self.button_rect = pg.Rect(20, 20, 200, 50)
        self.visible = True
        self.required_commands = required_commands or []

class TaskManager:
    def __init__(self, desktop):
        self.desktop = desktop
        self.tasks = []
        self.total_xp = 0
        self.font = pg.font.SysFont("Arial", 16)
        self.font_large = pg.font.SysFont("Arial", 24)
        self.font_title = pg.font.SysFont("Arial", 32, bold=True)
        
        # Task tracking
        self.command_history = set()
        self.current_task_progress = {}
        
        # Menu states
        self.show_menu = False
        self.show_explanation = False
        self.selected_task_index = None
        
        # Surfaces
        self.menu_surface = pg.Surface((screen_width, screen_height))
        self.explanation_surface = pg.Surface((screen_width, screen_height))
        self.menu_alpha = 0
        self.fade_speed = 15
        
        # Notification system
        self.show_notification = False
        self.notification_text = ""
        self.notification_timer = 0
        
        self._init_tasks()
        
    def _init_tasks(self):
        self.tasks = [
            Task("Terminal Mastery", 
                "Learn essential terminal commands", 
                150,
                [
                    "To complete this task, you need to:",
                    "1. Use the 'ls' command to list directory contents",
                    "2. Use 'cd' to change directories",
                    "3. Create a new directory with 'mkdir'",
                    "4. Use 'clear' to clean the terminal",
                    "",
                    "Tips:",
                    "- Try 'ls' to see what's in your current directory",
                    "- Use 'cd ..' to go up one directory",
                    "- Create a new directory with 'mkdir mynewdir'",
                    "- Type 'help' to see all available commands"
                ],
                required_commands=['ls', 'cd', 'mkdir', 'help']),

            Task("File System Navigation", 
                "Master directory navigation", 
                200,
                [
                    "Navigate through the file system:",
                    "1. Go to your home directory using 'cd ~'",
                    "2. List contents with 'ls'",
                    "3. Create a new directory called 'mynewdir'",
                    "4. Navigate into it",
                    "5. Go back to parent directory",
                    "",
                    "Required commands:",
                    "- cd ~",
                    "- cd ..",
                    "- ls",
                    "- mkdir"
                ],
                required_commands=['cd ~',"cd ..", 'ls', 'mkdir mynewdir']),

            Task("Directory Structure", 
                "Create a project directory structure", 
                250,
                [
                    "Create a complete project structure:",
                    "1. Create a 'projects' directory",
                    "2. Inside it, create:",
                    "   - 'src' directory",
                    "   - 'docs' directory",
                    "   - 'tests' directory",
                    "",
                    "Commands needed:",
                    "- mkdir projects",
                    "- cd projects",
                    "- mkdir src"
                ],
                required_commands=['mkdir projects', 'cd projects', 'mkdir src'])
        ]
        
        # Initialize progress for each task
        for task in self.tasks:
            self.current_task_progress[task.title] = set()

    def check_terminal_command(self, command):
        # Add the full command to history
        self.command_history.add(command)
        
        completed_tasks = []
        
        for task in self.tasks:
            if not task.completed and task.required_commands:
                # Check both full commands and base commands
                completed_commands = set()
                for req_command in task.required_commands:
                    # Check if the required command matches exactly or as a base command
                    if req_command in self.command_history or command.startswith(req_command.split()[0]):
                        completed_commands.add(req_command)
                
                self.current_task_progress[task.title] = completed_commands
                
                if len(completed_commands) == len(task.required_commands):
                    task.completed = True
                    self.total_xp += task.xp_reward
                    completed_tasks.append(task.title)
        
        if completed_tasks:
            self.show_task_completion(f"Completed: {', '.join(completed_tasks)}!")
            return True
        
        return False

    def show_task_completion(self, text):
        self.show_notification = True
        self.notification_text = text
        self.notification_timer = 180  # 3 seconds at 60 FPS

    def handle_terminal_input(self, terminal, command):
        if command:
            self.check_terminal_command(command)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            
            if not self.show_menu:
                task_button = pg.Rect(20, 20, 200, 50)
                if task_button.collidepoint(mouse_pos):
                    self.show_menu = True
                    self.show_explanation = False
                    return True
            else:
                task_area_width = screen_width/2
                task_area_x = screen_width/4
                
                if self.show_explanation:
                    if event.button == 1:
                        self.show_explanation = False
                        return True
                else:
                    for i, task in enumerate(self.tasks):
                        task_rect = pg.Rect(task_area_x, 120 + (i * 100), task_area_width, 80)
                        if task_rect.collidepoint(mouse_pos):
                            if event.button == 3:  # Right click
                                self.show_explanation = True
                                self.selected_task_index = i
                                return True
                    
                    task_area = pg.Rect(screen_width/4, 100, screen_width/2, screen_height-200)
                    if not task_area.collidepoint(mouse_pos):
                        self.show_menu = False
                        self.show_explanation = False
                        return True
        
        return False

    def draw(self, screen):
        if not self.show_menu:
            self._draw_task_button(screen)
        else:
            self._draw_menu(screen)
        
        if self.show_notification:
            self._draw_notification(screen)
            self.notification_timer -= 1
            if self.notification_timer <= 0:
                self.show_notification = False

    def _draw_task_button(self, screen):
        button_rect = pg.Rect(20, 20, 200, 50)
        pg.draw.rect(screen, (40, 40, 40), button_rect)
        pg.draw.rect(screen, GREEN, button_rect, 2)
        text = self.font.render("Tasks Menu", True, GREEN)
        screen.blit(text, (button_rect.x + 10, button_rect.y + 15))
        xp_display = self.font_large.render(f"Total XP: {self.total_xp}", True, GREEN)
        screen.blit(xp_display, (20, screen_height - 40))

    def _draw_menu(self, screen):
        # Draw menu background
        self.menu_surface.fill((0, 0, 0))
        if self.menu_alpha < 200:
            self.menu_alpha += self.fade_speed
        self.menu_surface.set_alpha(self.menu_alpha)
        screen.blit(self.menu_surface, (0, 0))
        
        if self.show_explanation and self.selected_task_index is not None:
            self._draw_task_explanation(screen)
        else:
            self._draw_task_list(screen)

    def _draw_task_explanation(self, screen):
        task = self.tasks[self.selected_task_index]
        explanation_bg = pg.Rect(screen_width/4, 100, screen_width/2, screen_height-200)
        pg.draw.rect(screen, (30, 30, 30), explanation_bg)
        pg.draw.rect(screen, GREEN, explanation_bg, 2)
        
        # Draw title
        title = self.font_title.render(task.title, True, GREEN)
        title_rect = title.get_rect(center=(screen_width/2, 140))
        screen.blit(title, title_rect)
        
        # Draw progress if applicable
        if task.title in self.current_task_progress:
            progress = self.current_task_progress[task.title]
            if progress:
                progress_text = f"Progress: {len(progress)}/4 commands completed"
                prog_text = self.font.render(progress_text, True, GREEN)
                screen.blit(prog_text, (screen_width/4 + 20, 170))
        
        # Draw detailed explanation
        y_offset = 200
        for line in task.detailed_explanation:
            text = self.font.render(line, True, GREEN)
            text_rect = text.get_rect(x=screen_width/4 + 20, y=y_offset)
            screen.blit(text, text_rect)
            y_offset += 30
        
        # Draw close instruction
        close_text = self.font.render("Click to close explanation", True, GREEN)
        close_rect = close_text.get_rect(center=(screen_width/2, screen_height - 60))
        screen.blit(close_text, close_rect)

    def _draw_notification(self, screen):
        notification_height = 50
        notification_rect = pg.Rect(
            (screen_width - 300) // 2,
            50,
            300,
            notification_height
        )
        pg.draw.rect(screen, (40, 40, 40), notification_rect)
        pg.draw.rect(screen, GREEN, notification_rect, 2)
        
        text = self.font.render(self.notification_text, True, GREEN)
        text_rect = text.get_rect(center=notification_rect.center)
        screen.blit(text, text_rect)

    def _draw_task_list(self, screen):
        # Draw title
        title = self.font_title.render("Available Tasks", True, GREEN)
        title_rect = title.get_rect(center=(screen_width/2, 60))
        screen.blit(title, title_rect)
        
        # Draw tasks
        task_area_width = screen_width/2
        task_area_x = screen_width/4
        
        for i, task in enumerate(self.tasks):
            task_rect = pg.Rect(task_area_x, 120 + (i * 100), task_area_width, 80)
            pg.draw.rect(screen, (40, 40, 40), task_rect)
            pg.draw.rect(screen, GREEN, task_rect, 2)
            
            title_text = self.font_large.render(task.title, True, GREEN)
            screen.blit(title_text, (task_rect.x + 20, task_rect.y + 10))
            
            desc_text = self.font.render(task.description, True, GREEN)
            screen.blit(desc_text, (task_rect.x + 20, task_rect.y + 40))
            
            xp_text = self.font.render(f"Reward: {task.xp_reward} XP", True, GREEN)
            xp_rect = xp_text.get_rect(right=task_rect.right - 20, centery=task_rect.y + 20)
            screen.blit(xp_text, xp_rect)
            
            # Show progress or completion status
            if task.completed:
                status_text = "Completed"
                status_color = (0, 200, 0)
            elif task.title in self.current_task_progress:
                progress = len(self.current_task_progress[task.title])
                status_text = f"Progress: {progress}/4"
                status_color = (200, 200, 0)
            else:
                status_text = "Right click for details"
                status_color = (200, 200, 0)
            
            status_render = self.font.render(status_text, True, status_color)
            status_rect = status_render.get_rect(
                right=task_rect.right - 20, 
                centery=task_rect.y + 60
            )
            screen.blit(status_render, status_rect)
        
        instruction = self.font.render("Click outside to close", True, GREEN)
        instruction_rect = instruction.get_rect(center=(screen_width/2, screen_height - 40))
        screen.blit(instruction, instruction_rect)