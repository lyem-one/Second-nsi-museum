import pygame
import threading
import cv2
import jpp
import config


def ratio(width2, height2, width3, height3, screen):

    larg = width2
    haut = height2
    posX = 0
    posY = 0

    if width2 / height2 == 16 / 9:
        ratio = width2 / width3
        larg = height2 * (16 / 9)
        width, height = intro60("content/UI/vid.mov", "content/Audio/video.mp3",screen, posX, posY, larg, haut)

    elif width2 / height2 == 16 / 10:
        ratio = height2 / height3
        haut = width2 * (10 / 16)
        width, height = intro60("content/UI/video.mov", "content/Audio/video.mp3",screen, posX, posY, larg, haut)

    elif width2 / height2 == 4 / 3:
        ratio = height2 / height3
        haut = width2 * (3 / 4)
        width, height = intro60("content/UI/vidold.mov", "content/Audio/video.mp3",screen, posX, posY, larg, haut)

    elif width2 / height2 > 16 / 9:
        ratio = width2 / width3
        larg = height2 * (16 / 9)
        posX = (width2 - larg) / 2
        width, height = intro60("content/UI/vid.mov", "content/Audio/video.mp3",screen, posX, posY, larg, haut)

    elif 4 / 3 < width2 / height2 < 16 / 9:
        ratio = height2 / height3
        haut = width2 * (10 / 16)
        posY = (height2 - haut) / 2
        width, height = intro60("content/UI/video.mov", "content/Audio/video.mp3",screen, posX, posY, larg, haut)

    elif width2 / height2 < 4 / 3:
        ratio = height2 / height3
        haut = width2 * (3 / 4)
        posY = (height2 - haut) / 2
        width, height = intro60("content/UI/vidold.mov", "content/Audio/video.mp3", screen, posX, posY, larg, haut)

    return width, height, ratio, posY, posX

def intro60(path_to_file, audio_file, screen, posX, posY, largflt, hautflt):
    input_file = path_to_file
    clock = pygame.time.Clock()

    video = cv2.VideoCapture(input_file)
    success, video_image = video.read()
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    larg = int(largflt)
    haut = int(hautflt)

    if not success:
        print("Erreur lors de l'ouverture de la vidéo.")
        return

    print (larg, haut)


    print(f"Résolution de la vidéo originale : {width}x{height}")
    print(f"Redimensionnement à : {larg}x{haut}")

    # Process audio
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(1)

    # lecture de la vidéo + affichage de chaque frames sur la fenêtre pygame (ne pas mettre trop de fps sinon: ram)
    run = success
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        success, video_image = video.read()
        if success:
            try:
                print(f"Taille originale de la frame : {video_image.shape}")
                # Redimensionner l'image de la frame
                frame_resized = cv2.resize(video_image, (int(larg), int(haut)))
                print(f"Frame redimensionnée à : {frame_resized.shape}")

                # Convertir l'image redimensionnée en surface Pygame
                video_surf = pygame.surfarray.make_surface(cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB).swapaxes(0, 1))
                print("Conversion en surface Pygame réussie")

                # Afficher la surface sur la fenêtre Pygame
                screen.blit(video_surf, (posX, posY))
                pygame.display.flip()
            except Exception as e:
                print(f"Erreur lors du redimensionnement ou de l'affichage : {e}")
                run = False
        else:
            run = False




    return width, height

def music(path_to_file, loop, difloop, path_to_file2):
    while not config.start_stop:
        if difloop==1:
            pygame.mixer.init()
            pygame.mixer.music.load(path_to_file)
            pygame.mixer.music.play(1)
            difloop = 0
        else:
            pygame.mixer.music.queue(path_to_file2)
        if config.start_stop:
            pygame.mixer.music.stop()
            break


def dialogue(text, screen, clock, w, h, font, fg_color, bg_color, corx, y, xmarge):
    area_rect = pygame.Rect(xmarge, y, w-xmarge*2, h-25)
    message = jpp.TypingArea(text, area_rect, font, fg_color, bg_color, corx, wps=400)
    wy = message.is_typing_complete()
    while wy == False:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        else:
            message.update()
            wy = message.is_typing_complete()
            message.draw(screen)

            pygame.display.flip()
            clock.tick(60)
            print(wy)