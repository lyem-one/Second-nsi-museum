import pygame 
import time
from random import gauss
from collections import deque

CPS_40WPM = 5 * 40 / 60
BASE_DELAY_MS = 2000/CPS_40WPM

# Une très grande partie du code provient de https://gjenkinsedu.com/post/pygame_scrolling_typewriter_text_box_0008/

def _type_delay(word_per_min=40.0):
    speed_factor = 40/word_per_min
    mean = BASE_DELAY_MS * speed_factor
    v = gauss(mean, mean/2)
    return mean

class TypingArea:
    def __init__ (self, text, area, font, fg_color, bk_color, corx, wps=80):
        self.boup_sound = pygame.mixer.Sound("content/Audio/boop.wav")
        self.char_queue = deque(text)
        self.rect = area.copy()
        self.font = font
        self.corx = corx
        self.fg_color = fg_color
        self.bk_color = bk_color
        self.size = area.size
        self.area_surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.area_surface.fill(bk_color)
        self.wps = wps
        self.y = corx
        self.y_delta = self.font.size("M")[1]
        self.line = ""
        self.next_time = time.time()
        self.dirty = 0
    def _render_new_line(self):
            self.y += self.y_delta
            self.line = ""
            if self.y + self.y_delta > self.size[1]:
               self.area_surface.blit(self.area_surface, self.bk_color, (0, self.y, self.size[0], self.size[1] - self.y))
               self.dirty = 1
    def _render_char(self, c):
        if c == '\n':
            self._render_new_line()
        else:
            self.line += c
            text = self.font.render(self.line, True, self.fg_color)
            self.area_surface.blit(text, (0, self.y))
            self.dirty = 1
            if c != ' ' and c != '.':
                pygame.mixer.init()
                pygame.mixer.Sound.play(self.boup_sound)

    def update(self):
        while self.char_queue and self.next_time <= time.time():
            self._render_char(self.char_queue.popleft())
            self.next_time += _type_delay(self.wps)/1000

    def draw(self, screen):
        if self.dirty:
            screen.blit(self.area_surface, self.rect)
            self.dirty = 0

    def is_typing_complete(self):
        return not bool(self.char_queue)
