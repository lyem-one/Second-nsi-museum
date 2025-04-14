import pygame
from pygame import *
import jpp

def dialogue(STORY, screen, clock, w, h, font, fg_color, bg_color, corx):
    area_rect = pygame.Rect(25, 0, w-50, h-25)
    message = jpp.TypingArea(STORY, area_rect, font, fg_color, bg_color, corx, wps=400)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        else:
            message.update()
            message.draw(screen)

            pygame.display.flip()
            clock.tick(60)

        