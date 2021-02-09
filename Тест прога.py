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


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        global LEVEL_DMG, LEVEL_SPD, LEVEL_SPEED

        self.imageRight1 = load_image('korablRight1.png')
        self.imageLeft1 = load_image('korablLeft1.png')
        self.image1 = load_image('korabl1.png')


        self.image = self.image1

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.centery = HEIGHT / 2

        self.speed = 1 + LEVEL_SPD
        self.health = 3 + LEVEL_DUR
        self.prev_shot = 0
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):

        if self.health < 1:
            EndGame()


        k = pygame.key.get_pressed()

        self.image = self.image1

        if k[pygame.K_LEFT]:
            self.image = self.imageLeft1
            self.rect.x -= self.speed
        if k[pygame.K_RIGHT]:
            self.image = self.imageRight1
            self.rect.x += self.speed


        if k[pygame.K_UP]:
            self.rect.y -= self.speed
        if k[pygame.K_DOWN]:
            self.rect.y += self.speed

        if k[pygame.K_SPACE]:
            if SCORE - self.prev_shot > 60:
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


Startbackground = load_image('StartMenuFon.png')
Startbackground2 = load_image('StartMenuFon.png')

Startbackground_rect = Startbackground.get_rect()
Startbackground_rect2 = Startbackground.get_rect()
Startbackground_rect2.x = 1500


def ShowStartBackground():
    Startbackground_rect.x -= 1
    Startbackground_rect2.x -= 1

    screen.blit(Startbackground, Startbackground_rect)
    screen.blit(Startbackground2, Startbackground_rect2)

    if Startbackground_rect.right < 0:
        Startbackground_rect.x = 1500

    if Startbackground_rect2.right < 0:
        Startbackground_rect2.x = 1500


def StartGame():

    start_sprites = pygame.sprite.Group()

    PlayButton = Button('Play', 490, 260)
    UpgradeButton = Button('Upgrade', 490, 360)
    ExitButton = Button('Exit', 490, 460)


    start_sprites.add(PlayButton)
    start_sprites.add(UpgradeButton)
    start_sprites.add(ExitButton)

    font = pygame.font.Font(None, 50)
    text = font.render(f"BEST : {PREV_BEST}", True, (255, 216, 0))

    coin = load_image('Coin.png')

    runningStartGame = True

    while runningStartGame:
        clock.tick(FPS)


        screen.fill(BLACK)

        ShowStartBackground()

        showmoney = font.render(f" : {MONEY}", True, (255, 216, 0))
        screen.blit(showmoney, (1000, 0))
        screen.blit(text, (0, 0))

        screen.blit(coin, (960, 0))


        start_sprites.draw(screen)

        pygame.display.flip()



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
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ExitButton.rect.collidepoint(event.pos):
                    return True




def UpgradeGame():

    global MONEY, LEVEL_SPD, LEVEL_DUR, LEVEL_DMG

    upgrade_sprites = pygame.sprite.Group()

    UpgradeDURButton = Button('Plus', 131, 200)
    upgrade_sprites.add(UpgradeDURButton)

    UpgradeDMGButton = Button('Plus', 931, 200)
    upgrade_sprites.add(UpgradeDMGButton)

    UpgradeSPDButton = Button('Plus', 531, 200)
    upgrade_sprites.add(UpgradeSPDButton)

    GoBackButton = Button('GoBack', 0, 0)
    upgrade_sprites.add(GoBackButton)

    font = pygame.font.Font(None, 50)

    textcolor = pygame.color.Color(0, 150, 0)
    textcolor.hsva = [240, 100, 80]


    titleDur =  font.render(f"Прочность", True, textcolor)
    titleSpd =  font.render(f"Скорость", True, textcolor)
    titleDmg =  font.render(f"Урон", True, textcolor)


    coin = load_image('Coin.png')


    runningUpgradeGame = True

    while runningUpgradeGame:
        clock.tick(FPS)



        screen.fill(BLACK)
        ShowStartBackground()


        pygame.draw.line(screen, (0, 0, 0,), (400, 0), (400, HEIGHT), 2)
        pygame.draw.line(screen, (0, 0, 0,), (800, 0), (800, HEIGHT), 2)

        screen.blit(titleDur, (110, 100))
        screen.blit(titleSpd, (520, 100))
        screen.blit(titleDmg, (958, 100))

        showmoney = font.render(f" : {MONEY}", True, (255, 216, 0))

        screen.blit(coin, (960, 0))
        screen.blit(showmoney, (1000, 0))

        costDur = font.render(f"Цена: {5 + LEVEL_DUR * 5}", True, textcolor)
        costSpd = font.render(f"Цена: {5 + LEVEL_SPD * 5}", True, textcolor)
        costDmg = font.render(f"Цена: {5 + LEVEL_DMG * 5}", True, textcolor)


        screen.blit(costDur, (200 - costDur.get_size()[0] // 2, 300))
        screen.blit(costSpd, (600 - costDmg.get_size()[0] // 2, 300))
        screen.blit(costDmg, (1000 - costSpd.get_size()[0] // 2, 300))

        upgrade_sprites.draw(screen)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if GoBackButton.rect.collidepoint(event.pos):
                    return

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeDURButton.rect.collidepoint(event.pos):
                    if MONEY >= LEVEL_DUR * 5 + 5:
                        MONEY -= LEVEL_DUR * 5 + 5
                        LEVEL_DUR += 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeDMGButton.rect.collidepoint(event.pos):
                    if MONEY >= LEVEL_DMG * 5 + 5:
                        MONEY -= LEVEL_DMG * 5 + 5
                        LEVEL_DMG += 1

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeSPDButton.rect.collidepoint(event.pos):
                    if MONEY >= LEVEL_SPD * 5 + 5:
                        MONEY -= LEVEL_SPD * 5 + 5
                        LEVEL_SPD += 1


def Game():

    global SCORE
    runningGame = True

    spaceship = SpaceShip()
    Player.add(spaceship)
    all_sprites.add(spaceship)


    background = load_image('fon3.png')
    background2 = load_image('fon3.png')
    background_rect = background.get_rect()
    background_rect2 = background.get_rect()
    background_rect2.x = WIDTH

    health = load_image('Health.png')

    font = pygame.font.Font(None, 50)

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    three = load_image('three.png')
    screen.blit(three, (480, 200))
    pygame.display.flip()
    clock.tick(1)

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    two = load_image('two.png')
    screen.blit(two, (480, 200))
    pygame.display.flip()
    clock.tick(1)

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    one = load_image('one.png')
    screen.blit(one, (480, 200))
    pygame.display.flip()
    clock.tick(1)


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
        all_sprites.draw(screen)
        enemy.draw(screen)

        SCORE += 1
        text = font.render(f"Счет: {SCORE}", True, (255, 255, 255))
        screen.blit(text, (150, 0))

        cur_health = font.render(f": {spaceship.health}", True, (0, 127, 14))
        screen.blit(health, (0, 0))
        screen.blit(cur_health, (30, 0))

        pygame.display.flip()



#######################################################################################################################
# Начало работы программы
#######################################################################################################################

# Загружаем данные
try:
    file = open('data/gamedata.txt', 'r')
except FileNotFoundError:
   file = open('data/gamedata.txt', 'w')
   file.write('''0
0
0
0
0''')
   file.close()
   file = open('data/gamedata.txt', 'r')

data = file.readlines()
PREV_BEST = int(data[0])
MONEY = int(data[1])
LEVEL_DUR, LEVEL_DMG, LEVEL_SPD = int(data[2]), int(data[3]), int(data[4])
file.close()

all_sprites = pygame.sprite.Group()
Player = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemybullets = pygame.sprite.Group()
enemy = pygame.sprite.Group()



if StartGame():
    file = open('data/gamedata.txt', 'w')
    file.write(f'''{PREV_BEST}
{MONEY}
{LEVEL_DUR}
{LEVEL_DMG}
{LEVEL_SPD}''')
    file.close()




pygame.quit()