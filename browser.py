import pygame as pg
from config import *
import random
import time

class Browser:
    def __init__(self, desktop, width=800, height=600, x=50, y=50):
        self.desktop = desktop
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.surface = pg.Surface((width, height))
        self.rect = pg.Rect(x, y, width, height)
        self.font = pg.font.SysFont("Arial", 16)
        self.font_large = pg.font.SysFont("Arial", 24)
        self.font_title = pg.font.SysFont("Arial", 20, bold=True)
        
        # Input boxes
        self.url_box = pg.Rect(80, 40, width - 160, 30)  # URL bar in top area
        self.search_box = pg.Rect(width//4, 250, width//2, 40)  # Search box for homepage
        self.active_input = None
        self.input_text = ""
        
        self.scroll_y = 0
        self.max_scroll = 0
        self.cursor_visible = True
        self.cursor_timer = time.time()
        
        # Navigation buttons
        self.back_button = pg.Rect(20, 40, 30, 30)
        self.forward_button = pg.Rect(50, 40, 30, 30)
        self.refresh_button = pg.Rect(width - 50, 40, 30, 30)
        
        # Browser state
        self.history = []
        self.current_page = "home"
        self.history_index = -1
        self.interactive_elements = []
        
        # Website database
        self.websites = {
            "home": {
                "title": "DarkSeeker",
                "type": "search",
                "content": [
                    ("title", "DarkSeeker - Anonymous Search"),
                    ("image", "logo", width//4, 120, width//2, 100),
                    ("text", "Your Gateway to Private Browsing"),
                    ("search", "Search the dark web..."),
                    ("links", [
                        ("Popular", "categories.onion"),
                        ("Markets", "markets.onion"),
                        ("Forums", "forums.onion"),
                        ("News", "news.onion")
                    ])
                ]
            },
            "categories.onion": {
                "title": "Categories",
                "type": "list",
                "content": [
                    ("title", "Browse Categories"),
                    ("category", "Security Tools", [
                        ("Encryption", "encryption.onion"),
                        ("VPN Services", "vpn.onion"),
                        ("Password Managers", "passwords.onion")
                    ]),
                    ("category", "Communication", [
                        ("Secure Email", "email.onion"),
                        ("Chat Services", "chat.onion"),
                        ("Forums", "forums.onion")
                    ]),
                    ("category", "Information", [
                        ("Tech News", "technews.onion"),
                        ("Security Blogs", "secblogs.onion"),
                        ("Tutorials", "tutorials.onion")
                    ])
                ]
            },
            "markets.onion": {
                "title": "Digital Markets",
                "type": "marketplace",
                "content": [
                    ("title", "Digital Marketplace"),
                    ("warning", "Warning: Access legitimate services only"),
                    ("category", "Software", [
                        ("Development Tools", "devtools.onion"),
                        ("Security Software", "security.onion"),
                        ("Operating Systems", "os.onion")
                    ]),
                    ("category", "Services", [
                        ("Web Hosting", "hosting.onion"),
                        ("VPN Services", "vpn.onion"),
                        ("Cloud Storage", "storage.onion")
                    ])
                ]
            }
        }
        
        # Load home page
        self.load_page("home")

    def load_page(self, url):
        if url in self.websites:
            self.current_page = url
            self.interactive_elements = []
            
            if self.history_index < len(self.history) - 1:
                self.history = self.history[:self.history_index + 1]
            
            self.history.append(url)
            self.history_index = len(self.history) - 1
            
            # Reset scroll position
            self.scroll_y = 0
            self.input_text = url
            
            # Update URL bar
            if self.active_input == self.url_box:
                self.input_text = url

    def create_clickable(self, rect, action, text="", color=GRAY):
        self.interactive_elements.append({
            "rect": rect,
            "action": action,
            "text": text,
            "color": color,
            "hover": False
        })

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            relative_pos = (mouse_pos[0] - self.x, mouse_pos[1] - self.y)
            
            # Handle close button
            close_button = pg.Rect(self.width - 30, 5, 20, 20)
            if close_button.collidepoint(relative_pos):
                self.desktop.browsers.remove(self)
                return
            
            # Handle scroll
            if event.button == 4:  # Scroll up
                self.scroll_y = max(0, self.scroll_y - 30)
            elif event.button == 5:  # Scroll down
                self.scroll_y = min(self.max_scroll, self.scroll_y + 30)
            
            # Handle navigation buttons
            if self.back_button.collidepoint(relative_pos) and self.history_index > 0:
                self.history_index -= 1
                self.load_page(self.history[self.history_index])
            elif self.forward_button.collidepoint(relative_pos) and self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.load_page(self.history[self.history_index])
            elif self.refresh_button.collidepoint(relative_pos):
                self.load_page(self.current_page)
            
            # Handle input boxes
            if self.url_box.collidepoint(relative_pos):
                self.active_input = self.url_box
                if self.current_page == "home":
                    self.input_text = ""
            elif self.current_page == "home" and self.search_box.collidepoint(relative_pos):
                self.active_input = self.search_box
                self.input_text = ""
            else:
                # Check interactive elements
                clicked_pos = (relative_pos[0], relative_pos[1] - self.scroll_y)
                for element in self.interactive_elements:
                    if element["rect"].collidepoint(clicked_pos):
                        if callable(element["action"]):
                            element["action"]()
                        elif isinstance(element["action"], str):
                            self.load_page(element["action"])
                
                self.active_input = None
            
        elif event.type == pg.KEYDOWN:
            if self.active_input:
                if event.key == pg.K_RETURN:
                    if self.active_input == self.url_box:
                        if self.input_text in self.websites:
                            self.load_page(self.input_text)
                    elif self.active_input == self.search_box:
                        # Simulate search
                        self.load_page("categories.onion")
                    self.active_input = None
                elif event.key == pg.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
        
        elif event.type == pg.MOUSEMOTION:
            relative_pos = (event.pos[0] - self.x, event.pos[1] - self.y)
            # Update hover states
            for element in self.interactive_elements:
                element["hover"] = element["rect"].collidepoint(relative_pos)

    def draw_navigation(self):
        # Back button
        pg.draw.rect(self.surface, (200,200,200) if self.history_index > 0 else GRAY, self.back_button)
        # Forward button
        pg.draw.rect(self.surface, (200,200,200) if self.history_index < len(self.history) - 1 else GRAY, self.forward_button)
        # Refresh button
        pg.draw.rect(self.surface, (200,200,200), self.refresh_button)
        
        # URL bar
        pg.draw.rect(self.surface, WHITE, self.url_box)
        pg.draw.rect(self.surface, GRAY if self.active_input != self.url_box else GREEN, self.url_box, 2)
        
        # URL text
        url_text = self.font.render(self.input_text if self.active_input == self.url_box else self.current_page, True, BLACK)
        self.surface.blit(url_text, (self.url_box.x + 5, self.url_box.y + 5))

    def draw_content(self):
        if self.current_page not in self.websites:
            return
        
        page = self.websites[self.current_page]
        y_offset = 100
        
        for element_type, *data in page["content"]:
            if element_type == "title":
                title_surface = self.font_title.render(data[0], True, BLACK)
                title_rect = title_surface.get_rect(centerx=self.width//2, top=y_offset)
                self.surface.blit(title_surface, title_rect)
                y_offset += 50
            
            elif element_type == "image":
                _, x, y, w, h = data
                pg.draw.rect(self.surface, LIGHT_GRAY, (x, y, w, h))
                logo = pg.image.load("assets/images/logo_dark_seeker.png")
                logo = pg.transform.scale(logo, (w, h))
                text_rect = logo.get_rect(center=(x + w//2, y + h//2))
                self.surface.blit(logo, text_rect)
                y_offset = y + h + 30
            
            elif element_type == "text":
                text_surface = self.font.render(data[0], True, BLACK)
                text_rect = text_surface.get_rect(centerx=self.width//2, top=y_offset)
                self.surface.blit(text_surface, text_rect)
                y_offset += 40
            
            elif element_type == "search":
                if self.current_page == "home":
                    pg.draw.rect(self.surface, WHITE, self.search_box)
                    pg.draw.rect(self.surface, GRAY if self.active_input != self.search_box else GREEN, self.search_box, 2)
                    
                    placeholder = data[0]
                    if self.active_input == self.search_box:
                        text = self.input_text
                    else:
                        text = placeholder
                    
                    text_surface = self.font.render(text, True, GRAY if text == placeholder else BLACK)
                    self.surface.blit(text_surface, (self.search_box.x + 10, self.search_box.y + 10))
                    y_offset = self.search_box.bottom + 30
            
            elif element_type == "links":
                link_y = y_offset
                for text, url in data[0]:
                    link_rect = pg.Rect(self.width//4, link_y, self.width//2, 30)
                    self.create_clickable(link_rect, url, text, BLUE)
                    link_y += 40
                y_offset = link_y + 20
            
            elif element_type == "category":
                title, links = data
                category_surface = self.font_title.render(title, True, BLACK)
                self.surface.blit(category_surface, (40, y_offset))
                y_offset += 40
                
                for link_text, link_url in links:
                    link_rect = pg.Rect(60, y_offset, self.width - 120, 30)
                    self.create_clickable(link_rect, link_url, link_text, BLUE)
                    y_offset += 40
                
                y_offset += 20
            
            elif element_type == "warning":
                warning_surface = self.font.render(data[0], True, RED)
                warning_rect = warning_surface.get_rect(centerx=self.width//2, top=y_offset)
                self.surface.blit(warning_surface, warning_rect)
                y_offset += 40
        
        # Update max scroll
        self.max_scroll = max(0, y_offset - self.height + 100)

    def draw(self):
        # Main background
        self.surface.fill(WHITE)
        
        # Top bar
        pg.draw.rect(self.surface, (240,240,240), (0, 0, self.width, 80))
        
        # Close button
        close_button = pg.Rect(self.width - 30, 5, 20, 20)
        pg.draw.rect(self.surface, RED, close_button)
        
        # Draw navigation elements
        self.draw_navigation()
        
        # Content area
        content_rect = pg.Rect(0, 80, self.width, self.height - 80)
        pg.draw.rect(self.surface, WHITE, content_rect)
        
        # Draw page content
        self.draw_content()
        
        # Draw interactive elements
        for element in self.interactive_elements:
            rect = pg.Rect(element["rect"])
            rect.y += self.scroll_y  # Adjust for scrolling
            
            if element["hover"]:
                pg.draw.rect(self.surface, (230,230,255), rect)
            
            text_surface = self.font.render(element["text"], True, element["color"])
            text_rect = text_surface.get_rect(center=rect.center)
            self.surface.blit(text_surface, text_rect)
        
        # Draw cursor for active input
        if self.active_input and time.time() - self.cursor_timer > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = time.time()
        
        if self.active_input and self.cursor_visible:
            input_text = self.font.render(self.input_text, True, BLACK)
            cursor_x = self.active_input.x + 5 + input_text.get_width()
            cursor_y = self.active_input.y + 5
            pg.draw.line(self.surface, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + 20))
        
        # Window border
        pg.draw.rect(self.surface, GRAY, (0, 0, self.width, self.height), 2)
        
        # Blit to screen
        self.desktop.screen.blit(self.surface, (self.x, self.y))