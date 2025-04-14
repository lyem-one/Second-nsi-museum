import pygame
from pygame.locals import *
import sys
import fade
import intro

# création de la fenêtre pygame
#pygame.init()
#clock = pygame.time.Clock()
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
def entree():
    attente_confirmation = True
    while attente_confirmation:
        for confirm_event in pygame.event.get():
            if confirm_event.type == pygame.KEYDOWN and confirm_event.key == pygame.K_RETURN:
                attente_confirmation = False  # Confirmation reçue, sortir de la sous-boucle
def game(fnt):
    value = 0
    valueleft = 0
    valueright = 0
    valuedown = 0
    valueidle = 0

    x, y = fnt.get_size()
    xmage = 400
    ymage = 400

    # initialisation du module pygame
    pygame.init()

    # affichage de la fenêtre
    SCREEN_WIDTH, SCREEN_HEIGHT = fnt.get_size()
    fond = pygame.image.load("content/salle/salle 1.png").convert()
    # variable pour afficher qu'une seul image
    mage_idle1 = pygame.image.load("content/perso/main/main char up_0001.png").convert_alpha()
    bdd_init = pygame.image.load("content/UI/boite de dialogue.png")
    font = pygame.font.Font(None, int(73 * SCREEN_WIDTH / 1920))
    corx = SCREEN_HEIGHT - font.get_height() - 100


    #liste des images pour l'animation vers le haut
    mage_up = [pygame.image.load("content/perso/main/main char up_0001.png").convert_alpha(),
            pygame.image.load("content/perso/main/main char up_0002.png").convert_alpha(),
            pygame.image.load("content/perso/main/main char up_0003.png").convert_alpha(),
            pygame.image.load("content/perso/main/main char up_0004.png").convert_alpha(),]
    #liste des images pour l'animation vers la droite
    mage_right = [pygame.image.load("content/perso/main/main char right_0001.png").convert_alpha(),
               pygame.image.load("content/perso/main/main char right_0002.png").convert_alpha(),
               pygame.image.load("content/perso/main/main char right_0003.png").convert_alpha(),
               pygame.image.load("content/perso/main/main char right_0004.png").convert_alpha(), ]
    #liste des images pour l'animation vers la gauche
    mage_left = [pygame.image.load("content/perso/main/main char left_0001.png").convert_alpha(),
               pygame.image.load("content/perso/main/main char left_0002.png").convert_alpha(),
               pygame.image.load("content/perso/main/main char left_0003.png").convert_alpha(),
               pygame.image.load("content/perso/main/main char left_0004.png").convert_alpha(), ]
    #liste des images pour l'animation vers le bas
    mage_down = [pygame.image.load("content/perso/main/main char down_0001.png").convert_alpha(),
                 pygame.image.load("content/perso/main/main char down_0002.png").convert_alpha(),
                 pygame.image.load("content/perso/main/main char down_0003.png").convert_alpha(),
                 pygame.image.load("content/perso/main/main char down_0004.png").convert_alpha(), ]
    #liste des images pour l'animation imobile (vers le haut uniquement
    mage_idle = [pygame.image.load("content/perso/main/main char idle_0001.png").convert_alpha(),
                 pygame.image.load("content/perso/main/main char idle_0002.png").convert_alpha(), ]
    BG_COLOR = (0, 0, 0)

    img_x, img_y = fond.get_size()
    mult=SCREEN_HEIGHT/img_y
    if SCREEN_WIDTH/SCREEN_HEIGHT >= 16/10:
        mult = SCREEN_HEIGHT / img_y
    elif SCREEN_WIDTH/SCREEN_HEIGHT < 16/10:
        mult = SCREEN_WIDTH / img_x

    IMAGE_BIG = pygame.transform.rotozoom(fond, 0, mult*(1-0.06))
    perso1 = pygame.transform.rotozoom(mage_idle1, 0, mult*(1-0.06))
    bdd = pygame.transform.rotozoom(bdd_init, 0, 0.75)
    bg_width, bg_height = IMAGE_BIG.get_size()


    sprite_rect1 = perso1.get_rect()
    persox, persoy = perso1.get_size()
    sprite_rect1.y = SCREEN_HEIGHT/2-persoy/2
    sprite_rect1.x = SCREEN_WIDTH/2-persox/2
    print("\n rect: \n", sprite_rect1.x, sprite_rect1.y)
    print("\n value: \n", SCREEN_WIDTH/2-persox/2, SCREEN_HEIGHT/2-persoy/2)
    x=1920 - img_x * mult
    imgx, imgy = IMAGE_BIG.get_size()

    #affectation des coordonnées aux images
    img_big = (IMAGE_BIG, (SCREEN_WIDTH/2-imgx/2, SCREEN_HEIGHT/2-imgy/2))
    pers1 = (perso1, (SCREEN_WIDTH/2-persox/2, SCREEN_HEIGHT/2-persoy/2))

    # Exemple d'objet statique pour collision
    # Liste des objets statiques
    objets_statiques = [
        {"id": 1, "rect": pygame.Rect(390, 541, 50, 10)},  # Objet 1
        {"id": 2, "rect": pygame.Rect(542, 541, 50, 10)},  # Objet 2
        {"id": 3, "rect": pygame.Rect(695, 541, 50, 10)},  # Objet 3
        {"id": 4, "rect": pygame.Rect(1177, 541, 50, 10)},  # Objet 4
        {"id": 5, "rect": pygame.Rect(1330, 541, 50, 10)},  # Objet 5
        {"id": 6, "rect": pygame.Rect(1482, 541, 50, 10)},  # Objet 6
    ]

    murs_statiques = [
        pygame.Rect(150, 33, 100, 1008),  # mur 1
        pygame.Rect(251, 33, 642, 100),  # mur 2
        pygame.Rect(1030, 33, 642, 100),  # mur 3
        pygame.Rect(1672, 33, 100, 1008),  # mur 4
        pygame.Rect(150, 1041, 792, 10), # mur 5
        pygame.Rect(1030, 1041, 792, 10), #mur 6
    ]
    #initialisation des images + fondu en noir sortant sans rafraichir la fenetre pour éviter un effet glitch
    fade.FadeOut(x, y, fnt, img_big, pers1)
    fnt.blit(IMAGE_BIG, (SCREEN_WIDTH/2-imgx/2, SCREEN_HEIGHT/2-imgy/2))
    fnt.blit(perso1, (SCREEN_WIDTH/2-persox/2, SCREEN_HEIGHT/2-persoy/2))

    print(f"bg_width: {bg_width}, SCREEN_WIDTH: {SCREEN_WIDTH}")

    # Utilisez pygame.mixer pour la musique
    pygame.mixer.init()
    pygame.mixer.music.load("content/Audio/musée_.wav")
    pygame.mixer.music.play(-1) # -1 = boucle INFINII IIIII


    while True:

        # Obtenir les coordonnées de la souris
        x, y = pygame.mouse.get_pos()

        # Afficher les coordonnées dans la console


        # obtenir les touches pressées
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Obtenir la position du clic
                x, y = pygame.mouse.get_pos()
                print(f"Clic détecté à la position : x = {x}, y = {y}")
            if event.type == QUIT:
                # fermer la fenêtre
                pygame.quit()
                sys.exit()
            # Vérifier si la touche "Entrée" est pressée
            if event.type == pygame.KEYDOWN:  # Détection de pression de touche
                if event.key == pygame.K_RETURN:  # Vérifier si c'est "Entrée"
                    for objet in objets_statiques:
                        if sprite_rect1.colliderect(objet["rect"]):

                            # -------------------------------
                            # INTEL
                            # -------------------------------

                            if objet['id'] == 1:
                                fnt.blit(bdd, (0, 607))
                                intro.dialogue("Vous regarder le présentoir:\n\n"
                                               "vous voyez marqué un nom qui vous est familié: Intel",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF","#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue('Intel est une entreprise informatique fondé en 1968 aux Etats Unis\n \n'
                                               "par Gordon Moore, Robert Noyce et Andrew Grove, connu pour sa\n \n"
                                               "famille de processeur Intel core (maintenant core ultra).",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF","#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("Cette entreprise a été l'une des première à avoir créé en 1971\n\n"
                                               "un microprocesseur x86 du nom de 'intel 4004' et a pendant longtemps\n\n"
                                               "équippé les mac de leurs puces de 2006 à 2020.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF","#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("Elle est maintenant la 200ème plus grande entreprise du monde avec \n\n "
                                               '€76Md de capitalisation boursière et essaie de produire des cartes \n graphiques.',
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)
                                entree()

                            # -------------------------------
                            # AMD
                            # -------------------------------

                            elif objet['id'] == 2:
                                fnt.blit(bdd, (0, 607))
                                intro.dialogue("Vous regarder le présentoir:\n\n "
                                                "vous voyez marqué un nom marqué en noir: AMD",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("AMD (Advanced Micro Devices) est une entreprise informatique fondé \n\n"
                                               "en 1969 par Jerry Handers, Edwin Turney, John Carey, Sven Simonsen,\n\n"
                                               " Jack Gifford, Frank Botte, Jim Giles et Larry Stenger aux Etats-Unis.",
                                fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("Tout ce beau monde va en 1995 (soit 24 ans après Intel) créer le \n\n"
                                    "premier micro processeur x86 de l'entreprise: le 'AMD-K5'.",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("En 2006, AMD va racheter ATI (un fabricant de carte graphique) et va \n\n"
                                    "grâce à cela, s'immiscer dans le monde du GPU (graphics compute unit \n\n"
                                    "(carte graphique quoi)).",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("En 2017, AMD annonce l'arrivé de l'architecture Zen et ainsi l'arrivé\n\n"
                                               "d'une nouvelle gamme, la gamme Ryzen. (Encore d'actualité \n\n"
                                               "aujourd'hui, On est à la 9ème génération de Ryzen.)",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)

                                entree()

                                intro.dialogue("Aujourd'hui, AMD est la 92ème plus grosse entreprise du monde avec \n\n"
                                               "€134Md de capitalisation boursière.",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b", 0, 700, 75)

                                entree()

                            # -------------------------------
                            # NVIDIA
                            # -------------------------------

                            elif objet['id'] == 3:
                                fnt.blit(bdd, (0, 607))
                                intro.dialogue("Vous regarder le présentoir:\n\n "
                                               "vous voyez marqué d'un logo vert: Nvidia",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Nvidia est une entreprise fondée en 1993 par Jen-Hsun Huang,\n\n"
                                               "Chris A. Malachowsky et Curtis Priem aux Etats-Unis connu pour sa\n\n"
                                               "gamme de carte graphique GTX et aujourd'hui RTX.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("La toute première puce graphique créé par Nvidia est la NV1\n\n"
                                               "en 1995, qui sera gravée en 500 NANOMETRES???? (aujourd'hui on \n\n"
                                               "est aux alentours des 5 nm soit 100 fois moins.)",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Ce qui a réellement chamboulé le monde du Gaming du coté de Nvidia,\n\n"
                                               "c'est l'annonce des cartes RTX 20XX amenant le Ray Tracing dans\n\n"
                                               "le jeu vidéo.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Aujourd'hui, Nvidia est la 3ème entreprise du monde par\n\n"
                                               "capitalisation boursière, capitale s'élevant à €2 381Md.\n\n"
                                               "(non je ne me suis pas tromper.)",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                            # -------------------------------
                            # MACOS
                            # -------------------------------

                            elif objet['id'] == 4:
                                fnt.blit(bdd, (0, 607))
                                intro.dialogue("Vous regarder le présentoir:\n\n "
                                               "vous voyez une pomme.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("MacOS est un système d'exploitation créer en 1984 par la société\n\n"
                                               "Apple. Il se base sur le noyau UNIX et est à sa 14ème version\n\n"
                                               "(macOS sequoia).",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Aujourd'hui, ce système est principalement utilisé dans le monde\n\n"
                                               "professionnel (montage vidéo, création de musique, etc.) même si\n\n"
                                               "Apple montre une ouverture au monde du gaming (game porting tool)",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("MacOS n'est pas un système installable partout. La politique d'Apple\n\n"
                                               "est très strict et ce système ne peux être installer QUE sur un appareil \n\n"
                                               "Apple.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                            # -------------------------------
                            # WINDAUBE
                            # -------------------------------

                            elif objet['id'] == 5:
                                fnt.blit(bdd, (0, 607))

                                intro.dialogue("Vous regarder le présentoir:\n\n "
                                               "vous voyez un logo à 4 carré.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Windows est un système d'exploitation créé en 1985 par la société\n\n"
                                               "Microsoft. Windows était un dérivé de MS-DOS. (aujourd'hui basé sur\n\n"
                                               "son propre noyau Windows NT.)",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Aujourd'hui, Windows représente 69% des système utiliser sur\n\n"
                                               "ordinateur ce qui en fait le système n°1 loin devant macOS. et est\n\n"
                                               "principalement utiliser pour de la bureautique et du jeu vidéo.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()


                            #-------------------------------
                            # LINUX
                            #-------------------------------

                            elif objet['id'] == 6:
                                fnt.blit(bdd, (0, 607))
                                intro.dialogue("Vous regarder le présentoir:\n\n "
                                               "vous voyez marqué un nom qui ne vous est PAS DU TOUT familié: Linux",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Linux est un système d'exploitation créé par Linus Torvald en 1992.\n\n"
                                               "Basé sur le noyau UNIX.",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue("Ce système devrait réellement s'appelé GNU/LINUX car la licence sous\n\n"
                                               "laquelle il a été publier est la licence GNU GPL qui stipule que le\n\n"
                                               "projet mis sous cette licenses, est réutilisable, modifiable,",
                                               fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                               0, 700, 75)

                                entree()

                                intro.dialogue(
                                    "s'il est publié sous la même licence (c'est un peu plus compliqué...)",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                    0, 700, 75)

                                entree()

                                intro.dialogue(
                                    "Linux est une base pour de nombreux systèmes d'exploitations \n\n"
                                    "(environ 3000) et sa licenses permet la création de fork (dérivé) ce qui \n\n"
                                    "permet a des systèmes de se baser sur d'autres systèmes d'exploitations",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                    0, 700, 75)

                                entree()

                                intro.dialogue(
                                    "Par exemple, Pop!_OS est un dérivé de Ubuntu qui lui même est un\n\n"
                                    "dérivé de Debian qui lui aussi est un dérivé de Linux (Wouf)",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                    0, 700, 75)

                                entree()

                                intro.dialogue(
                                    "Aujourd'hui, Linux est beaucoup utiliser par des développeurs, ou\n\n"
                                    "même par des gamers (via le steam deck, une console dont son\n\n"
                                    "système est basé sur un système linux).",
                                    fnt, pygame.time.Clock(), SCREEN_WIDTH, 300, font, "#FFFFFF", "#65004b",
                                    0, 700, 75)

                                entree()


        for objet in objets_statiques:
            tolerance = 5  # Marge de tolérance
            if sprite_rect1.colliderect(objet["rect"]):
                if abs(sprite_rect1.right - objet["rect"].left) < tolerance:  # Collision à gauche
                    sprite_rect1.right = objet["rect"].left
                elif abs(sprite_rect1.left - objet["rect"].right) < tolerance:  # Collision à droite
                    sprite_rect1.left = objet["rect"].right
                elif abs(sprite_rect1.bottom - objet["rect"].top) < tolerance:  # Collision par le haut
                    sprite_rect1.bottom = objet["rect"].top
                elif abs(sprite_rect1.top - objet["rect"].bottom) < tolerance:  # Collision par le bas
                    sprite_rect1.top = objet["rect"].bottom

        for objet in murs_statiques:
            tolerance = 5  # Marge de tolérance
            if sprite_rect1.colliderect(objet):
                print(f"Collision détectée ! Position personnage : {sprite_rect1}, Position objet : {objet}")
                if abs(sprite_rect1.right - objet.left) < tolerance:  # Collision à gauche
                    sprite_rect1.right = objet.left
                elif abs(sprite_rect1.left - objet.right) < tolerance:  # Collision à droite
                    sprite_rect1.left = objet.right
                elif abs(sprite_rect1.bottom - objet.top) < tolerance:  # Collision par le haut
                    sprite_rect1.bottom = objet.top
                elif abs(sprite_rect1.top - objet.bottom) < tolerance:  # Collision par le bas
                    sprite_rect1.top = objet.bottom


        if keys[pygame.K_LEFT]:
            if keys[pygame.K_RIGHT]:
                sprite_rect1.x += 0
            elif keys[pygame.K_DOWN]:
                if down == 1:
                    sprite_rect1.x -= 4.25
                    # affichage de l'animation
                    if int(valueleft) >= len(mage_left):
                        valueleft = 0
                    perso1 = mage_left[int(valueleft)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    valueleft += 0.15 #en 10 fps
                else:
                    sprite_rect1.y += 4.25
                    if int(valuedown) >= len(mage_down):
                        valuedown = 0
                    perso1 = mage_down[int(valuedown)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    valuedown += 0.15 #en 10 fps
            elif keys[pygame.K_UP]:
                if up == 1:
                    sprite_rect1.x -= 4.25
                    if int(valueleft) >= len(mage_left):
                        valueleft = 0
                    perso1 = mage_left[int(valueleft)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    valueleft += 0.15 #en 10 fps
                else:
                    sprite_rect1.y -= 4.25
                    if int(value) >= len(mage_up):
                        value = 0
                    perso1 = mage_up[int(value)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    value += 0.15 #en 10 fps
            else:
                sprite_rect1.x -= 4.25
                down=0
                up=0
                if int(valueleft) >= len(mage_left):
                    valueleft = 0
                perso1 = mage_left[int(valueleft)]
                perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                valueleft += 0.15 #en 10 fps

        elif keys[pygame.K_RIGHT]:
            if keys[pygame.K_DOWN]:
                if down == 1:
                    sprite_rect1.x += 4.25
                    if int(valueright) >= len(mage_right):
                        valueright = 0
                    perso1 = mage_right[int(valueright)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    valueright += 0.15 #en 10 fps
                else:
                    sprite_rect1.y += 4.25
                    if int(valuedown) >= len(mage_down):
                        valuedown = 0
                    perso1 = mage_down[int(valuedown)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    valuedown += 0.15 #en 10 fps
            elif keys[pygame.K_UP]:
                if up == 1:
                    sprite_rect1.x += 4.25
                    if int(valueright) >= len(mage_right):
                        valueright = 0
                    perso1 = mage_right[int(valueright)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    valueright += 0.15 #en 10 fps
                else:
                    sprite_rect1.y -= 4.25
                    if int(value) >= len(mage_up):
                        value = 0
                    perso1 = mage_up[int(value)]
                    perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                    value += 0.15 #en 10 fps
            else:
                sprite_rect1.x += 4.25
                down=0
                up=0
                if int(valueright) >= len(mage_right):
                    valueright = 0
                perso1 = mage_right[int(valueright)]
                perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                valueright += 0.15 #en 10 fps

        elif keys[pygame.K_UP]:
            if keys[pygame.K_DOWN]:
                sprite_rect1.y += 0
            else:
                sprite_rect1.y -= 4.25
                if int(value) >= len(mage_up):
                    value = 0
                perso1 = mage_up[int(value)]
                perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
                value += 0.15 #en 10 fps
                up = 1

        elif keys[pygame.K_DOWN]:
            sprite_rect1.y += 4.25
            down = 1
            if int(valuedown) >= len(mage_down):
                valuedown = 0
            perso1 = mage_down[int(valuedown)]
            perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
            valuedown += 0.15 #en 10 fps
        else:
            if int(valueidle) >= len(mage_idle):
                valueidle = 0
            perso1 = mage_idle[int(valueidle)]
            perso1 = pygame.transform.rotozoom(perso1, 0, mult * (1 - 0.06))
            valueidle += 0.05 #en 2 fps


        fnt.fill((0,0,0))
        fnt.blit(IMAGE_BIG, (SCREEN_WIDTH/2-imgx/2, SCREEN_HEIGHT/2-imgy/2))
        fnt.blit(perso1, sprite_rect1)
        pygame.display.update()
        pygame.time.Clock().tick(60) #limiter l'écran à 60 fps (NE PAS CHANGER sauf si tt les valeurs correspondant au temps sont modifié)