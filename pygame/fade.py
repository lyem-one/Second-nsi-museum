import pygame
import sys


def FadeIn(SCREENWIDTH, SCREENHEIGHT, screen):
    fade = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    fade.fill((0,0,0))
    opacity = 0
    for r in range(0, 51):
        opacity = r
        fade.set_alpha(opacity)
        screen.blit(fade, (0,0))
        pygame.display.update()
        print("actif 2", r)
    print(opacity)

def FadeOut(width2, height2, screen, *items):
    fade = pygame.Surface((width2, height2), pygame.SRCALPHA)
    fade.fill((0, 0, 0, 255))
    for opacity in range(255, -1, -7):
        fade.fill((0, 0, 0, opacity))  # Remplir la surface avec l'opacité mise à jour
        for item, position in items:
            screen.blit(item, position)
        screen.blit(fade, (0, 0))
        pygame.display.update()
