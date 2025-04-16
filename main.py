import pygame
import intro
import sys
import threading
import fade
import feur
import config



def darkness(img, screen, coordinate, amount, intensity):
    copy = img.copy()
    for i in range(0, amount):
        copy.fill((0, 0, 0, intensity), None, pygame.BLEND_RGBA_MULT)
        copy.fill((0, 0, 0)[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
        screen.blit(copy, (coordinate))
        pygame.display.flip()
        print(f"Opacité: {i}, Couleur: {copy.get_at((0, 0))}")
    print("FINI")
    print(i)
    return copy

def introduction():
    # création de la fenêtre pygame
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    global start_stop

    # import des images
    fond = pygame.image.load("content/UI/bg.jpg").convert_alpha()
    title_import = pygame.image.load("content/UI/title screen.png").convert_alpha()
    btn_start_import = pygame.image.load("content/UI/start button.png").convert_alpha()

    # initialisation des variables
    btn_pressed = 0
    width2, height2 = screen.get_size()
    width3, height3 = fond.get_size()
    scrn_ratio = width2 / height2
    width_btn, height_btn = btn_start_import.get_size()
    width_ttls, height_ttls = title_import.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, int(73*width2/1920))
    corx = height2-font.get_height()-100
    alpha = 0
    fondu = 0
    darker = 0

    # création d'une variable pour stop la musique
    config.start_stop = False
    
    intro.dialogue("Launching the game. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . OK", screen, clock, width2, 1080, font, "#FFFFFF","#000000", corx, 0, 25)
    pygame.time.delay(200)
    intro.dialogue("Running necessary dependencies . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . OK", screen, clock, width2, 1080, font, "#FFFFFF","#000000", corx, 0, 25)
    pygame.time.delay(200)
    intro.dialogue("Running Intro.mp4 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . OK", screen, clock, width2, 1080, font, "#FFFFFF","#000000", corx, 0, 25)
    pygame.time.delay(1000)
    intro.dialogue("_", screen, clock, width2, 1080, font, "#FFFFFF","#000000", 20, 0, 25)
    pygame.time.delay(500)
    intro.dialogue(" ", screen, clock, width2, 1080, font, "#FFFFFF", "#000000", 20, 0, 25)
    pygame.time.delay(500)
    intro.dialogue("_", screen, clock, width2, 1080, font, "#FFFFFF", "#000000", 20, 0, 25)
    pygame.time.delay(500)
    intro.dialogue(" ", screen, clock, width2, 1080, font, "#FFFFFF", "#000000", 20, 0, 25)
    pygame.time.delay(500)
    intro.dialogue("_", screen, clock, width2, 1080, font, "#FFFFFF", "#000000", 20, 0, 25)
    pygame.time.delay(500)
    intro.dialogue(" ", screen, clock, width2, 1080, font, "#FFFFFF", "#000000", 20, 0, 25)
    
    pygame.time.delay(1500)

    width, height, ratio, posY, posX = intro.ratio(width2, height2, width3, height3, screen)
    # transformation des images
    IMAGE_BIG = pygame.transform.rotozoom(fond, 0, ratio)
    start_btn = pygame.transform.rotozoom(btn_start_import, 0, ratio * 2)
    ttls = pygame.transform.rotozoom(title_import, 0, ratio * 2)

    #création de variables pour les coordonnées
    xbtn = width2 / 2 - width_btn * ratio
    ybtn = height2 / 2 + 250 * ratio

    xttls = width2 / 2 - width_ttls * ratio
    yttls = 50 * ratio

    #mise en place des coordonnées de l'image
    img_big = (IMAGE_BIG, (0, 0))
    startbtn = (start_btn, (xbtn, ybtn))
    ttl_s = (ttls, (xttls, yttls))

    #affichage en bonne et du forme
    screen.blit(IMAGE_BIG, (0, 0))
    screen.blit(start_btn, (xbtn, ybtn))
    screen.blit(ttls, (xttls, yttls))

    # affichage des images par fondu
    fade.FadeOut(width2, height2, screen, img_big, startbtn, ttl_s)
    pygame.display.flip()



    # création d'un environnement isolé pour la musique (plutot un thread)
    music_thread2 = threading.Thread(target=intro.music, args=("content/Audio/music.wav", -1, 1, "content/Audio/mmlpng.wav"))
    music_thread2.start()
    while fondu ==0:
        posiX, posiY = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("CLIIQUE")  # debug button_pressed
                # vérification si lors du clique, le curseur se trouve entre le (0, 0) et le (x, y) du bouton

                print(width_btn, height_btn)

                #wow le calcul (juste pour savoir su curseur inclu dans bouton)
                if width2 / 2 - width_btn * ratio <= posiX <= width2 / 2 - width_btn * ratio + width_btn * ratio * 2 and height2 / 2 + 250 * ratio <= posiY <= height2 / 2 + 250 * ratio + height_btn*ratio * 2:
                    btn_pressed = 1  # le bouton a été presser
                    config.start_stop = True
                    music_thread2.join()
                    ptitbrt=pygame.mixer.Sound("content/Audio/cnfrm.wav")
                    ptitbrt.play()
        # vérification de si bouton pressé
        if btn_pressed == 1:

            #assombrissement plus élevé du bouton (juice visuel)
            co = (xbtn, ybtn)
            darkness(start_btn, screen, co, 1, 100)
            pygame.time.delay(100)

            #fondu en noir
            fade.FadeIn(width2, height2, screen)
            fondu = 1

        #vérif de la position du curseur
        if width2 / 2 - width_btn * ratio <= posiX <= width2 / 2 - width_btn * ratio + width_btn * ratio * 2 and height2 / 2 + 250 * ratio <= posiY <= height2 / 2 + 250 * ratio + height_btn*ratio * 2:
            # est ce que l'image est dja assombrie
            if darker == 0:
                #assombrissement du bouton légerement (juice visuel)
                co = (xbtn, ybtn)
                darkness(start_btn, screen, co,7,  8)
                pygame.display.flip()
                darker = 1
        else:
            screen.blit(start_btn, (xbtn, ybtn))
            pygame.display.flip()
            darker = 0

    pygame.time.delay(1000)
    feur.game(screen)

introduction()