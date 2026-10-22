import pygame
import pygame.font
from pygame.locals import KEYDOWN, MOUSEBUTTONDOWN
import time
from typing import List, Tuple, Optional

class Typewriter:
    """
    A class that animates typing text into a dialogue box with word wrapping
    and auto-pausing when the box is full.
    """
    
    def __init__(self, message: str, speed: float, width: int, height: int, 
                 font_size: int = 24, font_name: Optional[str] = None):
        """
        Initialize the Typewriter.
        
        Args:
            message: The text to be typed
            speed: Characters per second (float)
            width: Width of the dialogue box in pixels
            height: Height of the dialogue box in pixels
            font_size: Size of the font (default: 24)
            font_name: Name of the font (default: None uses default pygame font)
        """
        self.full_message = message
        self.speed = speed
        self.box_width = width
        self.box_height = height
        self.font_size = font_size
        self.font_name = font_name
        
        # Initialize pygame font if not already done
        if not pygame.font.get_init():
            pygame.font.init()
        
        # Create font
        self.font = pygame.font.Font(font_name, font_size)
        
        # State variables
        self.displayed_text = ""
        self.char_index = 0
        self.last_update = time.time()
        self.finished = False
        self.paused = False
        self.needs_clear = False
        self.waiting_for_input = False
        self.lines = []
        self.line_height = self.font.get_linesize()
        
        # Calculate max lines that fit in the box
        # Add some padding (10px on each side)
        self.padding = 10
        self.max_line_width = self.box_width - (self.padding * 2)
        self.max_lines = (self.box_height - (self.padding * 2)) // self.line_height
        
        # Pre-wrap the entire message into lines
        self.all_lines = self._wrap_text(message)
        
        # Track current line being typed
        self.current_line_index = 0
        self.current_char_in_line = 0
        
    def _wrap_text(self, text: str) -> List[str]:
        """
        Wrap text into lines that fit within the box width.
        
        Args:
            text: The text to wrap
            
        Returns:
            List of wrapped lines
        """
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            # Check if adding this word would exceed max width
            word_surface = self.font.render(word + ' ', False, (0, 0, 0))
            word_width = word_surface.get_width()
            
            if current_width + word_width <= self.max_line_width:
                current_line.append(word)
                current_width += word_width
            else:
                # Start new line
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
        
        # Add the last line
        if current_line:
            lines.append(' '.join(current_line))
        
        # Handle empty text
        if not lines:
            lines = ['']
            
        return lines
    
    def update(self, dt: float = None) -> None:
        """
        Update the typing animation.
        
        Args:
            dt: Delta time in seconds (optional, uses actual time if not provided)
        """
        if self.finished or self.paused or self.waiting_for_input:
            return
        
        if dt is None:
            current_time = time.time()
            dt = current_time - self.last_update
            self.last_update = current_time
        
        # Calculate characters to type based on speed
        chars_to_type = int(self.speed * dt)
        
        if chars_to_type <= 0:
            return
        
        # Type characters
        while chars_to_type > 0 and not self.finished:
            if self.current_line_index >= len(self.all_lines):
                self.finished = True
                self.waiting_for_input = True
                break
            
            current_line = self.all_lines[self.current_line_index]
            
            if self.current_char_in_line < len(current_line):
                # Type next character
                self.current_char_in_line += 1
                chars_to_type -= 1
                
                # Update displayed text for current line
                self._update_displayed_lines()
            else:
                # Move to next line
                self.current_line_index += 1
                self.current_char_in_line = 0
                
                # Check if we've exceeded max lines
                if self.current_line_index >= self.max_lines:
                    # Box is full, pause and wait for input
                    self.waiting_for_input = True
                    self.paused = True
                    break
    
    def _update_displayed_lines(self) -> None:
        """Update the displayed text based on current line and character positions."""
        lines_to_show = []
        for i in range(max(0, self.current_line_index - self.max_lines + 1), 
                      self.current_line_index + 1):
            if i < len(self.all_lines):
                if i == self.current_line_index:
                    # Current line: show partial text
                    lines_to_show.append(self.all_lines[i][:self.current_char_in_line])
                else:
                    lines_to_show.append(self.all_lines[i])
        
        self.lines = lines_to_show
    
    def handle_input(self) -> None:
        """Handle input event to clear box and continue typing."""
        if self.waiting_for_input:
            if self.finished:
                # If completely finished, reset or just mark as done
                self.waiting_for_input = False
                self.paused = False
            else:
                # Clear the box and continue
                self.waiting_for_input = False
                self.paused = False
                self.lines = []
                # Continue from where we left off
                # The update loop will handle continuing
    
    def render(self, surface: pygame.Surface, x: int, y: int, 
               text_color: Tuple[int, int, int] = (255, 255, 255),
               bg_color: Optional[Tuple[int, int, int]] = None) -> None:
        """
        Render the typed text onto the given surface.
        
        Args:
            surface: The pygame surface to render on
            x: X position of the dialogue box
            y: Y position of the dialogue box
            text_color: RGB color for text (default: white)
            bg_color: RGB color for background (optional)
        """
        # Draw background if specified
        if bg_color:
            pygame.draw.rect(surface, bg_color, 
                           (x, y, self.box_width, self.box_height))
        
        # Draw border
        pygame.draw.rect(surface, text_color, 
                        (x, y, self.box_width, self.box_height), 2)
        
        # Draw each line of text
        for i, line in enumerate(self.lines):
            if i < self.max_lines:
                text_surface = self.font.render(line, False, text_color)
                surface.blit(text_surface, 
                           (x + self.padding, 
                            y + self.padding + (i * self.line_height)))
        
        # Draw cursor at the end of current line if still typing
        if not self.finished and not self.waiting_for_input and self.lines:
            cursor_x = x + self.padding + self.font.size(self.lines[-1])[0]
            cursor_y = y + self.padding + ((len(self.lines) - 1) * self.line_height)
            # Draw blinking cursor
            if int(time.time() * 2) % 2 == 0:
                pygame.draw.line(surface, text_color,
                               (cursor_x, cursor_y),
                               (cursor_x, cursor_y + self.line_height), 2)
        
        # Draw "Press any key" indicator if waiting for input
        if self.waiting_for_input:
            indicator = "▼ Press any key to continue..."
            if self.finished:
                indicator = "▼ Press any key to close..."
            indicator_surf = self.font.render(indicator, True, text_color)
            indicator_x = x + (self.box_width - indicator_surf.get_width()) // 2
            indicator_y = y + self.box_height - self.padding - self.line_height
            surface.blit(indicator_surf, (indicator_x, indicator_y))
    
    def is_finished(self) -> bool:
        """Return whether all text has been typed."""
        return self.finished and not self.waiting_for_input
    
    def is_paused(self) -> bool:
        """Return whether typing is currently paused."""
        return self.paused or self.waiting_for_input
    
    def get_lines(self) -> List[str]:
        """Return the currently displayed lines of text."""
        return self.lines.copy()
    
    def reset(self, new_message: Optional[str] = None) -> None:
        """
        Reset the typewriter with a new message or reuse the same.
        
        Args:
            new_message: New message to type (optional)
        """
        if new_message is not None:
            self.full_message = new_message
            self.all_lines = self._wrap_text(new_message)
        
        self.displayed_text = ""
        self.char_index = 0
        self.finished = False
        self.paused = False
        self.waiting_for_input = False
        self.lines = []
        self.current_line_index = 0
        self.current_char_in_line = 0
        self.last_update = time.time()


# Example usage:
def example():
    """Example of how to use the Typewriter class."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Typewriter Demo")
    clock = pygame.time.Clock()
    
    # Create typewriter
    message = "This is a long message that will wrap around the dialogue box. " \
              "It will continue typing until the box is full, then pause for " \
              "input before clearing and continuing. " \
              "This demonstrates the auto-pause and resume functionality."
    
    typewriter = Typewriter(
        message=message,
        speed=15.0,  # characters per second
        width=600,
        height=200,
        font_size=24
    )
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN or event.type == MOUSEBUTTONDOWN:
                # Handle input to continue typing
                if typewriter.is_paused():
                    typewriter.handle_input()
        
        # Update typewriter
        typewriter.update(dt)
        
        # Clear screen
        screen.fill((50, 50, 50))
        
        # Render typewriter
        typewriter.render(
            surface=screen,
            x=100,
            y=200,
            text_color=(255, 255, 255),
            bg_color=(0, 0, 0)
        )
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    example()