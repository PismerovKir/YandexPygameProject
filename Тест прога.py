import pygame
import os
import sys
import random

pygame.init()

WIDTH = 1200
HEIGHT = 800
FPS = 100
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SCORE = 0
LEVEL_DUR = 0
LEVEL_DMG = 0
LEVEL_SPD = 0
PREV_BEST = 0
MONEY = 0



screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def LoadData():
    file = open('data/gamedata.txt', 'r')
    data = file.readlines()
    global LEVEL_DMG, LEVEL_SPD, LEVEL_DUR, MONEY, PREV_BEST
    PREV_BEST = int(data[0])
    MONEY = int(data[1])
    LEVEL_DUR, LEVEL_DMG, LEVEL_SPD = int(data[2]), int(data[3]), int(data[4])




class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        global LEVEL_DMG, LEVEL_SPD, LEVEL_SPEED

        self.image = load_image('korabl.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.centery = HEIGHT / 2

        self.speed = 4 + LEVEL_SPD
        self.health = 5 + LEVEL_DUR
        self.prev_shot = 0
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):

        if self.health < 1:
            EndGame()


        k = pygame.key.get_pressed()

        self.image = load_image('korabl.png')

        if k[pygame.K_LEFT]:
            self.image = load_image('korablLeft.png')
            self.rect.x -= self.speed
        if k[pygame.K_RIGHT]:
            self.image = load_image('korablRight.png')
            self.rect.x += self.speed


        if k[pygame.K_UP]:
            self.rect.y -= self.speed
        if k[pygame.K_DOWN]:
            self.rect.y += self.speed

        if k[pygame.K_SPACE]:
            if SCORE - self.prev_shot > 50:
                self.prev_shot = SCORE
                bul = LaserBulletLong(self.rect.right - 20, self.rect.top + 50)
                all_sprites.add(bul)
                bullets.add(bul)


        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 30:
            self.rect.top = 30

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT


class LaserBulletLong(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_image('LaserBulletLong.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.mask = pygame.mask.from_surface(self.image)

        self.damage = 1 + LEVEL_DMG


    def update(self):
        if self.rect.x > WIDTH:
            self.kill()
        self.rect.x += 10

        if pygame.sprite.spritecollideany(self, enemy):
            touched = pygame.sprite.spritecollideany(self, enemy)
            touched.health -= self.damage
            self.kill()



class LaserBulletAlien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = load_image('LaserBulletAlien.png')
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10


    def update(self):
        if self.rect.right < 0:
            self.kill()

        self.rect.x -= self.speed


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('alien.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-40, 100)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < -200 or self.rect.right > HEIGHT + -200:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-400, -100)
            self.speedy = random.randrange(1, 4)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('meteor1.png')
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randrange(50, HEIGHT - self.rect.height - 50)
        self.speedy = random.randrange(-1, 2)
        self.speedx = 3
        self.health = 3
        self.damage = 3
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.health < 1:
            self.kill()



class Button(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(f'Button{name}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




def PauseGame():
    runningPause = True
    while runningPause:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningPause = False
                return True
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    return


def EndGame():
    pass


def StartGame():

    start_sprites = pygame.sprite.Group()

    PlayButton = Button('Play', 490, 260)
    UpgradeButton = Button('Upgrade', 490, 360)

    start_sprites.add(PlayButton)
    start_sprites.add(UpgradeButton)




    Startbackground = load_image('StartMenuFon.png')
    Startbackground2 = load_image('StartMenuFon.png')
    Startbackground_rect = Startbackground.get_rect()
    Startbackground_rect2 = Startbackground.get_rect()
    Startbackground_rect2.x = WIDTH

    runningStartGame = True

    while runningStartGame:
        clock.tick(FPS)


        Startbackground_rect.x -= 1
        Startbackground_rect2.x -= 1

        screen.fill(BLACK)
        screen.blit(Startbackground, Startbackground_rect)
        screen.blit(Startbackground2, Startbackground_rect2)

        font = pygame.font.Font(None, 50)
        text = font.render(f"BEST : {PREV_BEST}", True, (255, 255, 255))
        screen.blit(text, (0, 0))

        start_sprites.draw(screen)

        pygame.display.flip()

        if Startbackground_rect.right < 0:
            Startbackground_rect.x = WIDTH

        if Startbackground_rect2.right < 0:
            Startbackground_rect2.x = WIDTH


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PlayButton.rect.collidepoint(event.pos):
                    if Game():
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeButton.rect.collidepoint(event.pos):
                    if UpgradeGame():
                        return True




def UpgradeGame():

    upgrade_sprites = pygame.sprite.Group()

    # UpgradeDMGButton = Button('Plus', 490, 360)
    # upgrade_sprites.add(UpgradeDMGButton)
    #
    # UpgradeDURButton = Button('Upgrade', 490, 360)
    # upgrade_sprites.add(UpgradeDURButton)
    #
    # UpgradeSPDButton = Button('Upgrade', 490, 360)
    # upgrade_sprites.add(UpgradeSPDButton)

    GoBackButton = Button('GoBack', 0, 0)
    upgrade_sprites.add(GoBackButton)

    Upgradebackground = load_image('StartMenuFon.png')
    Upgradebackground2 = load_image('StartMenuFon.png')
    Upgradebackground_rect = Upgradebackground.get_rect()
    Upgradebackground_rect2 =Upgradebackground.get_rect()
    Upgradebackground_rect2.x = WIDTH

    runningUpgradeGame = True

    while runningUpgradeGame:
        clock.tick(FPS)


        Upgradebackground_rect.x -= 1
        Upgradebackground_rect2.x -= 1

        screen.fill(BLACK)
        screen.blit(Upgradebackground, Upgradebackground_rect)
        screen.blit(Upgradebackground2,Upgradebackground_rect2)

        upgrade_sprites.draw(screen)

        pygame.display.flip()

        if Upgradebackground_rect.right < 0:
            Upgradebackground_rect.x = WIDTH

        if Upgradebackground_rect2.right < 0:
            Upgradebackground_rect2.x = WIDTH


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if GoBackButton.rect.collidepoint(event.pos):
                    return
















def Game():

    global SCORE
    runningGame = True

    background = load_image('fon3.png')
    background2 = load_image('fon3.png')
    background_rect = background.get_rect()
    background_rect2 = background.get_rect()
    background_rect2.x = WIDTH

    health = load_image('Health.png')

    font = pygame.font.Font(None, 50)

    while runningGame:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    if PauseGame():
                        return True

        if SCORE % 250 == 0:
            meteor = Meteor()
            enemy.add(meteor)



        if background_rect.right < 0:
            background_rect.x = WIDTH

        if background_rect2.right < 0:
            background_rect2.x = WIDTH

        background_rect.x -= 4
        background_rect2.x -= 4

        enemy.update()



        all_sprites.update()

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(background2, background_rect2)



        enemy.draw(screen)
        all_sprites.draw(screen)
        SCORE += 1
        text = font.render(f"Счет: {SCORE}", True, (255, 255, 255))
        screen.blit(text, (150, 0))

        cur_health = font.render(f": {spaceship.health}", True, (0, 127, 14))
        screen.blit(health, (0, 0))
        screen.blit(cur_health, (30, 0))

        pygame.display.flip()



#######################################################################################################################
LoadData()


all_sprites = pygame.sprite.Group()
spaceship = SpaceShip()
all_sprites.add(spaceship)
bullets = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
SpaceShipGroup = pygame.sprite.Group()
enemy = pygame.sprite.Group()


# for i in range(2):
#     alien = Alien()
#     all_sprites.add(alien)
#     enemy.add(alien)

StartGame()

pygame.quit()