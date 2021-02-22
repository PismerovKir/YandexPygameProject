import pygame
import os
import sys
import random
from os import path

pygame.init()
# pygame.mixer.init()
# TODO Здесь будет список всех файлов, которые есть в проге. Сначала их подгружаем, и если файл не найден то остальная
#  прога не работает
# files = [f for f in os.listdir(data)]
# files = ['alien.png', 'alienBang.png', 'alienbang1.png', 'alienbang2.png', 'alienbang3.png', 'alienbang4.png',
#          'alienbang5.png', 'alienpew.wav', 'bip.wav', 'body.png', 'ButtoContinue.png', 'ButtonContinue.png',
#          'ButtonExit.png', 'ButtonGoBack.png', 'ButtonMenu.png', 'ButtonMusicOff.png', 'ButtonMusicOn.png',
#          'ButtonPlay.png', 'ButtonPlus.png', 'ButtonReplay.png', 'ButtonUpgrade.png', 'Coin.png', 'count.wav',
#          'Cursor.png', 'ExitButton.png', 'explosion.png', 'explosion1.png', 'explosion2.png', 'explosion3.png',
#          'explosion4.png', 'fly_right.wav', 'fon.png', 'fon2.png', 'fon3.png', 'gamedata.txt', 'go.wav', 'gun.png',
#          'Health.png', 'icon.png', 'korabl1.png', 'korabl2.png', 'korablLeft1.png', 'korablLeft2.png',
#          'korablRight1.png', 'korablRight2.png', 'LaserBulletAlien.png', 'LaserBulletLong.png', 'meteor1.png',
#          'meteor2.png', 'meteor3.png', 'meteorBang.png', 'meteorbang1.png', 'meteorbang2.png', 'meteorbang3.png',
#          'meteorbang4.png', 'meteorbang5.png', 'minKorabl.png', 'motor.png', 'musicPause.mp3', 'music_fon.mp3',
#          'one.png', 'pewpew.wav', 'ShieldRight.png', 'Soundoff.png', 'Soundon.png', 'StartMenuFon.png', 'three.png',
#          'two.png', 'vzriv1.png', 'Ссылка.txt']
#
# for elem in files:
#     try:
#         file = open(f'data/{elem}', 'r')
#     except FileNotFoundError:
#         print(f'Файл {elem} не найден')


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
MUSIC = True
SOUND = True

pygame.mouse.set_visible(False)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Космострелялка')
clock = pygame.time.Clock()

MusicPlayer = pygame.mixer.music
MusicPlayer.load("data/music_fon.mp3")
MusicPlayer.set_volume(70)

# pew = pygame.mixer.Channel(0)
pew = pygame.mixer.Sound("data/pewpew.wav")
pew.set_volume(0.4)

alienpew = pygame.mixer.Sound("data/alienpew.wav")
alienpew.set_volume(0.4)

buyUpgrade = pygame.mixer.Sound("data/buyUpgrade.wav")
noMoney = pygame.mixer.Sound("data/noMoney.wav")



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

pygame.display.set_icon(load_image('minKorabl.png'))


class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        global LEVEL_DMG, LEVEL_SPD, LEVEL_SPEED

        self.imageRight1 = load_image('korablRight1.png')
        self.imageLeft1 = load_image('korablLeft1.png')
        self.image1 = load_image('korabl1.png')
        self.imageRight2 = load_image('korablRight2.png')
        self.imageLeft2 = load_image('korablLeft2.png')
        self.image2 = load_image('korabl2.png')


        self.image = self.image1
        self.imageRight = self.imageRight1
        self.imageLeft = self.imageLeft1

        self.counter = 0

        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.centery = HEIGHT / 2

        self.speed = 1 + LEVEL_SPD
        self.health = 5 + LEVEL_DUR
        self.prev_shot = 0
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):

        if SCORE % 10 == 0:
            if self.counter % 2 == 0:
                self.image = self.image2
                self.imageLeft = self.imageLeft2
                self.imageRight = self.imageRight2
            else:
                self.image = self.image1
                self.imageLeft = self.imageLeft1
                self.imageRight = self.imageRight1
            self.counter += 1

        k = pygame.key.get_pressed()

        if k[pygame.K_LEFT]:
            self.image = self.imageLeft
            self.rect.x -= self.speed
        if k[pygame.K_RIGHT]:
            self.image = self.imageRight
            self.rect.x += self.speed


        if k[pygame.K_UP]:
            self.rect.y -= self.speed
        if k[pygame.K_DOWN]:
            self.rect.y += self.speed

        if k[pygame.K_SPACE]:
            if SCORE - self.prev_shot > 60:
                self.prev_shot = SCORE
                bul = LaserBulletLong(self.rect.right - 66, self.rect.top + 26)
                all_sprites.add(bul)
                bullets.add(bul)
                if SOUND:
                    pew.play(0)


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
            if pygame.sprite.collide_mask(self, touched):
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
        self.damage = 3


    def update(self):
        if self.rect.right < 0:
            self.kill()

        if pygame.sprite.spritecollideany(self, Player):
            touched = pygame.sprite.spritecollideany(self, Player)
            if pygame.sprite.collide_mask(self, touched):
                touched.health -= self.damage
                self.kill()

        self.rect.x -= self.speed


class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('alien.png')
        self.rect = self.image.get_rect()
        self.bangimage1 = load_image('alienbang1.png')
        self.bangimage2 = load_image('alienbang2.png')
        self.bangimage3 = load_image('alienbang3.png')
        self.bangimage4 = load_image('alienbang4.png')
        self.bangimage5 = load_image('alienbang5.png')
        self.rect.x = WIDTH
        self.rect.y = random.randrange(50, HEIGHT - self.rect.height - 50)
        self.speedy = 1
        self.speedx = 1
        self.health = 3
        self.damage = 3
        self.mask = pygame.mask.from_surface(self.image)
        self.deathCounter = -1
        self.prev_shot = 0

    def update(self):
        self.rect.x -= self.speedx
        self.deathCounter -= 1
        if self.deathCounter == 32:
            self.image = self.bangimage2
        if self.deathCounter == 24:
            self.image = self.bangimage3
        if self.deathCounter == 16:
            self.image = self.bangimage4
        if self.deathCounter == 8:
            self.image = self.bangimage5


        if self.deathCounter == 0:
            self.kill()

        if self.health < 1 and self.deathCounter < 0:
            self.image = self.bangimage1
            self.deathCounter = 40

        # БАЗОВЫЙ ИИ TODO
        if self.rect.centery in range(spaceship.rect.centery - 30, spaceship.rect.centery + 30) and SCORE - self.prev_shot > 70:
            self.prev_shot = SCORE
            enemybullet = LaserBulletAlien(self.rect.left, self.rect.centery)
            all_sprites.add(enemybullet)
            enemybullets.add(enemybullet)
            if SOUND:
                alienpew.play()

        if self.rect.centery < spaceship.rect.centery:
            self.rect.y += self.speedy
        if self.rect.centery > spaceship.rect.centery:
            self.rect.y -= self.speedy




class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(f'meteor{random.randint(1, 3)}.png')
        self.bangimage1 = load_image('meteorBang1.png')
        self.bangimage2 = load_image('meteorBang2.png')
        self.bangimage3 = load_image('meteorBang3.png')
        self.bangimage4 = load_image('meteorBang4.png')
        self.bangimage5 = load_image('meteorBang5.png')

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randrange(50, HEIGHT - self.rect.height - 50)
        self.speedy = random.randrange(-1, 2)
        self.speedx = 3
        self.health = 3
        self.damage = 3
        self.mask = pygame.mask.from_surface(self.image)
        self.deathCounter = -1

    def update(self):
        self.deathCounter -= 1
        if self.deathCounter == 32:
            self.image = self.bangimage2
        if self.deathCounter == 24:
            self.image = self.bangimage3
        if self.deathCounter == 16:
            self.image = self.bangimage4
        if self.deathCounter == 8:
            self.image = self.bangimage5

        self.rect.x -= self.speedx
        self.rect.y += self.speedy

        if self.deathCounter == 0:
            self.kill()

        if self.health < 1 and self.deathCounter < 0:
            self.image = self.bangimage1
            self.deathCounter = 40




class Button(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image(f'Button{name}.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y



cursor = load_image('cursor.png')
def ShowCursor():
    x, y = pygame.mouse.get_pos()
    if pygame.mouse.get_focused():
        screen.blit(cursor, (x, y))





def PauseGame():
    global MUSIC, SOUND

    MusicPlayer.pause()
    backgr = screen.copy()
    runningPause = True
    ContinueButton = Button('Continue', 480, 300)
    MenuButton = Button('Menu', 480, 400)

    musicButton = Button('MusicOn', 45, HEIGHT - 40)
    soundButton = Button('SoundOn', 0, HEIGHT - 40)

    butts = pygame.sprite.Group()
    butts.add(ContinueButton)
    butts.add(MenuButton)


    while runningPause:
        clock.tick(FPS)

        screen.fill(BLACK)
        screen.blit(backgr, (0, 0))

        if MUSIC:
            musicButton.kill()
            musicButton = Button('MusicOff', 45, HEIGHT - 40)
        else:
            musicButton.kill()
            musicButton = Button('MusicOn', 45, HEIGHT - 40)

        if SOUND:
            soundButton.kill()
            soundButton = Button('SoundOff', 0, HEIGHT - 40)
        else:
            soundButton.kill()
            soundButton = Button('SoundOn', 0, HEIGHT - 40)

        butts.add(soundButton)
        butts.add(musicButton)

        butts.draw(screen)

        ShowCursor()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runningPause = False
                return True
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    MusicPlayer.unpause()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ContinueButton.rect.collidepoint(event.pos):
                    MusicPlayer.unpause()
                    return


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if MenuButton.rect.collidepoint(event.pos):
                    pygame.mixer.music.unpause()
                    for elem in all_sprites:
                        elem.kill()
                    if StartGame():
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if musicButton.rect.collidepoint(event.pos):
                    if MUSIC:
                        MUSIC = False
                    else:
                        MUSIC = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if soundButton.rect.collidepoint(event.pos):
                    if SOUND:
                        SOUND = False
                    else:
                        SOUND = True










def EndGame():
    MusicPlayer.stop()

    global SCORE, PREV_BEST
    font = pygame.font.Font(None, 50)
    newBest = font.render(f"", True, (255, 216, 0))
    money = font.render(f"Монет получено: ", True, (255, 216, 0))
    current = font.render(f"Счет: {SCORE}", True, (255, 216, 0))

    if SCORE > PREV_BEST:
        # PREV_BEST = SCORE TODO СНЯТЬ этот коммент
        newBest = font.render(f"Новый рекорд: {SCORE}!", True, (255, 216, 0))
        current = font.render(f"", True, (255, 216, 0))



    EndBackground = screen.copy()
    runningEndGame = True

    butts = pygame.sprite.Group()

    MenuButton = Button('Menu', 480, 500)
    MenuButton.rect.x = 600 - MenuButton.rect.width//2
    butts.add(MenuButton)
    AgainButton = Button('Replay', 480, 400)
    AgainButton.rect.x = 600 - AgainButton.rect.width // 2
    butts.add(AgainButton)

    while runningEndGame:
        clock.tick(FPS)
        screen.fill(BLACK)

        screen.blit(EndBackground, (0, 0))

        screen.blit(newBest, (600 - newBest.get_width()//2, 300))
        screen.blit(current, (600 - current.get_width()//2, 300))
        screen.blit(money, (600 - money.get_width() // 2, 350))


        butts.draw(screen)


        ShowCursor()
        pygame.display.flip()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                if StartGame():
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if MenuButton.rect.collidepoint(event.pos):
                    if StartGame():
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if AgainButton.rect.collidepoint(event.pos):
                    if Game():
                        return True





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

    if Startbackground_rect.right == 0:
        Startbackground_rect.x = 1500

    if Startbackground_rect2.right == 0:
        Startbackground_rect2.x = 1500


def StartGame():

    global MUSIC, SOUND

    start_sprites = pygame.sprite.Group()
    MusicPlayer.load('data/music_fon.mp3')

    if not MusicPlayer.get_busy():
        MusicPlayer.play(-1)

    PlayButton = Button('Play', 490, 260)
    UpgradeButton = Button('Upgrade', 490, 360)
    ExitButton = Button('Exit', 490, 460)

    musicButton = Button('MusicOn', 45, HEIGHT - 40)
    soundButton = Button('SoundOn', 0, HEIGHT - 40)


    start_sprites.add(PlayButton)
    start_sprites.add(UpgradeButton)
    start_sprites.add(ExitButton)

    font = pygame.font.Font(None, 50)
    text = font.render(f"BEST : {PREV_BEST}", True, (255, 216, 0))

    coin = load_image('Coin.png')

    runningStartGame = True

    while runningStartGame:
        clock.tick(FPS)

        if MUSIC:
            musicButton.kill()
            musicButton = Button('MusicOff', 45, HEIGHT - 40)
            if not MusicPlayer.get_busy():
                MusicPlayer.play(-1)
        else:
            musicButton.kill()
            musicButton = Button('MusicOn', 45, HEIGHT - 40)
            MusicPlayer.stop()

        if SOUND:
            soundButton.kill()
            soundButton = Button('SoundOff', 0, HEIGHT - 40)
        else:
            soundButton.kill()
            soundButton = Button('SoundOn', 0, HEIGHT - 40)

        start_sprites.add(soundButton)
        start_sprites.add(musicButton)


        screen.fill(BLACK)

        ShowStartBackground()

        showmoney = font.render(f" : {MONEY}", True, (255, 216, 0))
        screen.blit(showmoney, (WIDTH - showmoney.get_width() - 5, 0))
        screen.blit(text, (0, 0))

        screen.blit(coin, (WIDTH - showmoney.get_width() - 50, 0))


        start_sprites.draw(screen)

        ShowCursor()
        pygame.display.flip()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if PlayButton.rect.collidepoint(event.pos):
                    MusicPlayer.stop()
                    if Game():
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeButton.rect.collidepoint(event.pos):
                    if UpgradeGame():
                        return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ExitButton.rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if musicButton.rect.collidepoint(event.pos):
                    if MUSIC:
                        MUSIC = False
                    else:
                        MUSIC = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if soundButton.rect.collidepoint(event.pos):
                    if SOUND:
                        SOUND = False
                    else:
                        SOUND = True




def UpgradeGame():

    global MONEY, LEVEL_SPD, LEVEL_DUR, LEVEL_DMG, SOUND

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

    textcolor = pygame.color.Color(0, 50, 255)
    # textcolor.hsva = [240, 100, 80]


    titleDur =  font.render(f"Прочность", True, textcolor)
    titleSpd =  font.render(f"Скорость", True, textcolor)
    titleDmg =  font.render(f"Урон", True, textcolor)


    coin = load_image('Coin.png')


    gun = load_image('gun.png')
    body = load_image('body.png')
    motor = load_image('motor.png')


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
        screen.blit(showmoney, (WIDTH - showmoney.get_width() - 5, 0))
        screen.blit(coin, (WIDTH - showmoney.get_width() - 50, 0))



        costDur = font.render(f"Цена: {5 + LEVEL_DUR * 5}", True, textcolor)
        costSpd = font.render(f"Цена: {5 + LEVEL_SPD * 5}", True, textcolor)
        costDmg = font.render(f"Цена: {5 + LEVEL_DMG * 5}", True, textcolor)

        screen.blit(costDur, (200 - costDur.get_size()[0] // 2, 350))
        screen.blit(costSpd, (600 - costDmg.get_size()[0] // 2, 350))
        screen.blit(costDmg, (1000 - costSpd.get_size()[0] // 2, 350))

        currentDur = font.render(f"Текущая: {5 + LEVEL_DUR}", True, textcolor)
        currentSpd = font.render(f"Текущая: {1 + LEVEL_SPD}", True, textcolor)
        currentDmg = font.render(f"Текущий: {1 + LEVEL_DMG}", True, textcolor)

        screen.blit(currentDur, (200 - currentDur.get_size()[0] // 2, 500))
        screen.blit(currentSpd, (600 - currentSpd.get_size()[0] // 2, 500))
        screen.blit(currentDmg, (1000 - currentDmg.get_size()[0] // 2, 500))

        screen.blit(body, (200 - body.get_size()[0] // 2, 650))
        screen.blit(motor, (600 - motor.get_size()[0] // 2, 650))
        screen.blit(gun, (1000 - gun.get_size()[0] // 2, 650))



        upgrade_sprites.draw(screen)

        ShowCursor()
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
                        if SOUND:
                            buyUpgrade.play()
                    else:
                        if SOUND:
                            noMoney.play()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeDMGButton.rect.collidepoint(event.pos):
                    if MONEY >= LEVEL_DMG * 5 + 5:
                        MONEY -= LEVEL_DMG * 5 + 5
                        LEVEL_DMG += 1
                        if SOUND:
                            buyUpgrade.play()
                    else:
                        if SOUND:
                            noMoney.play()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if UpgradeSPDButton.rect.collidepoint(event.pos):
                    if MONEY >= LEVEL_SPD * 5 + 5:
                        MONEY -= LEVEL_SPD * 5 + 5
                        LEVEL_SPD += 1
                        if SOUND:
                            buyUpgrade.play()
                    else:
                        if SOUND:
                            noMoney.play()

            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    return


def Game():

    global SCORE, spaceship, MUSIC
    SCORE = 0
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

    count = pygame.mixer.Sound('data/count.wav')
    go = pygame.mixer.Sound('data/go.wav')

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    three = load_image('three.png')
    screen.blit(three, (480, 200))
    if SOUND:
        count.play()
    pygame.display.flip()
    clock.tick(1)

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    two = load_image('two.png')
    screen.blit(two, (480, 200))
    if SOUND:
        count.play()
    pygame.display.flip()
    clock.tick(1)

    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    one = load_image('one.png')
    screen.blit(one, (480, 200))
    pygame.display.flip()
    if SOUND:
        count.play()
    clock.tick(1)
    if SOUND:
        go.play()

    MusicPlayer.load('data/music_fight.mp3')

    if MUSIC:
        MusicPlayer.play(-1)



    while runningGame:
        clock.tick(FPS)

        if spaceship.health < 0:
            screen.fill(BLACK)
            screen.blit(background, background_rect)
            screen.blit(background2, background_rect2)
            bullets.draw(screen)
            enemybullets.draw(screen)
            enemy.draw(screen)
            x, y = spaceship.rect.centerx, spaceship.rect.centery
            screen.blit(load_image('explosion.png'), (x - 50, y - 50))
            for sprite in all_sprites:
                sprite.kill()
            if EndGame():
                return True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                    if PauseGame():
                        return True


        if SCORE % 100 == 0:
            meteor = Meteor()
            enemy.add(meteor)
            all_sprites.add(meteor)

        if SCORE % 100 == 0:
            alien = Alien()
            enemy.add(alien)
            all_sprites.add(alien)



        if background_rect.right == 0:
            background_rect.x = WIDTH

        if background_rect2.right == 0:
            background_rect2.x = WIDTH

        background_rect.x -= 4
        background_rect2.x -= 4

        enemy.update()

        all_sprites.update()

        screen.fill(BLACK)
        screen.blit(background, background_rect)
        screen.blit(background2, background_rect2)

        Player.draw(screen)
        bullets.draw(screen)
        enemybullets.draw(screen)
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
    data = file.readlines()
    PREV_BEST = int(data[0])
    MONEY = int(data[1])
    LEVEL_DUR, LEVEL_DMG, LEVEL_SPD = int(data[2]), int(data[3]), int(data[4])
    file.close()
except FileNotFoundError:
   file = open('data/gamedata.txt', 'w')
   file.write('''-1
0
0
0
0''')
   file.close()
except Exception:
    file = open('data/gamedata.txt', 'w')
    file.write('''-2
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





spaceship = SpaceShip()
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