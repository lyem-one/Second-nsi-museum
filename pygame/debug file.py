import pygame
import sys


def FadeIn(SCREENWIDTH, SCREENHEIGHT, screen):
    fade = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
    fade.fill((0, 0, 0))
    for opacity in range(0, 256):
        fade.set_alpha(opacity)
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)
        print("Opacity:", opacity)  # Ajoutez un délai de 10 millisecondes entre chaque mise à jour

def FadeOut(SCREENWIDTH, SCREENHEIGHT, screen):
    fade = pygame.Surface((SCREENWIDTH, SCREENHEIGHT), pygame.SRCALPHA)  # Surface avec transparence

    for opacity in range(255, -1, -1):
        fade.fill((0, 0, 0, opacity))  # Remplir la surface avec l'opacité mise à jour
        screen.fill((255, 0, 0))  # Réinitialiser l'affichage avec la couleur de fond rouge
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(10)
        print(f"Opacité: {opacity}, Couleur: {fade.get_at((0, 0))}")  # Débogage de l'opacité et de la couleur

def main():
    pygame.init()
    SCREENWIDTH, SCREENHEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Fade Effect Demo")

    # Remplir l'écran avec une couleur de fond
    screen.fill((255, 0, 0))  # Rouge comme arrière-plan pour plus de contraste
    pygame.display.update()

    # Attendre un moment avant de commencer le fondu
    pygame.time.delay(1000)

    # Appliquer l'effet de fondu au noir
    FadeOut(SCREENWIDTH, SCREENHEIGHT, screen)

    # Attendre un peu avant de quitter
    pygame.time.delay(2000)

    # Gestion des événements pour éviter la fermeture immédiate de la fenêtre
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


main()
