# Загрузка нужных библиотек
import pygame
import os
import random

pygame.init()
# Список файлов, нужных для запуска программы
files = ['alien.png', 'alienbang.wav', 'alienbang1.png', 'alienbang2.png', 'alienbang3.png', 'alienbang4.png',
         'alienbang5.png', 'alienpew.wav', 'body.png', 'ButtoContinue.png', 'ButtonContinue.png',
         'ButtonExit.png', 'ButtonGoBack.png', 'ButtonMenu.png', 'ButtonMusicOff.png', 'ButtonMusicOn.png',
         'ButtonPlay.png', 'ButtonPlus.png', 'ButtonReplay.png', 'ButtonSoundOff.png', 'ButtonSoundOn.png',
         'ButtonUpgrade.png', 'buyUpgrade.wav', 'Coin.png', 'count.wav', 'Cursor.png', 'ExitButton.png',
         'explosion1.png', 'explosion2.png', 'explosion3.png', 'explosion4.png', 'explosion5.png', 'fon3.png', 'go.wav',
         'gun.png', 'Health.png', 'killedAliensCounter.png', 'killedMeteorsCounter.png',
         'korabl1.png', 'korabl2.png', 'korablLeft1.png', 'korablLeft2.png', 'korablRight1.png', 'korablRight2.png',
         'LaserBulletAlien.png', 'LaserBulletLong.png', 'lastBang.wav', 'meteor1.png', 'meteor2.png', 'meteor3.png',
         'meteorbang.wav', 'meteorbang1.png', 'meteorbang2.png', 'meteorbang3.png', 'meteorbang4.png',
         'meteorbang5.png', 'meteorbangplayer.wav', 'meteorhit.wav', 'minKorabl.png', 'motor.png', 'musicPause.mp3',
         'music_fight.mp3', 'music_fon.mp3', 'noMoney.wav', 'one.png', 'pewpew.wav', 'PlayerHit.wav',
         'StartMenuFon.png', 'three.png', 'two.png']

notfound = []
OK = True
#Попытка открыть все файлы, в случае неудчи игра не запуститься
for elem in files:
    try:
        file = open(f'data/{elem}', 'r')
    except FileNotFoundError:
        OK = False
        notfound.append(elem)

if OK:
    #Глобальные переменные
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

    # Вспомогательные действия с окном, загрузка звуков и музыки
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

    PlayerHit = pygame.mixer.Sound("data/PlayerHit.wav")

    alienbang = pygame.mixer.Sound('data/alienbang.wav')

    meteorbang = pygame.mixer.Sound('data/meteorbang.wav')

    meteorhit = pygame.mixer.Sound('data/meteorhit.wav')

    meteorbangplayer = pygame.mixer.Sound('data/meteorbangplayer.wav')

    # Функция для загрузки картинки
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


    # Класс космического корабля
    class SpaceShip(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            global LEVEL_DMG, LEVEL_SPD, LEVEL_SPEED

            # Загрузка всех его картинок для анимации
            self.imageRight1 = load_image('korablRight1.png')
            self.imageLeft1 = load_image('korablLeft1.png')
            self.image1 = load_image('korabl1.png')
            self.imageRight2 = load_image('korablRight2.png')
            self.imageLeft2 = load_image('korablLeft2.png')
            self.image2 = load_image('korabl2.png')

            self.image = self.image1
            self.imageRight = self.imageRight1
            self.imageLeft = self.imageLeft1

            # Счетчик для анимации
            self.counter = 0

            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = 0
            self.rect.centery = HEIGHT / 2

            # Характеристики корабля
            self.speed = 2 + LEVEL_SPD
            self.health = 5 + LEVEL_DUR
            # Счетчик для стрельбы корабля
            self.prev_shot = 0
            self.mask = pygame.mask.from_surface(self.image)


        def update(self):
            # Смена картинки корабля (10 раз в секунду)
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

            # Движение корабля
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

            # Стрельба корабля
            if k[pygame.K_SPACE]:
                if SCORE - self.prev_shot > 75:
                    self.prev_shot = SCORE
                    bul = LaserBulletLong(self.rect.right - 66, self.rect.top + 26)
                    all_sprites.add(bul)
                    bullets.add(bul)
                    if SOUND:
                        pew.play(0)

            # Корабль может летать не везде
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

            if self.rect.top < 30:
                self.rect.top = 30

            if self.rect.right > 700:
                self.rect.right = 700

            if self.rect.bottom > HEIGHT:
                self.rect.bottom = HEIGHT


    # Выстрелы игрока
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

            # Поадание по врагу
            if pygame.sprite.spritecollideany(self, enemy):
                touched = pygame.sprite.spritecollideany(self, enemy)
                if pygame.sprite.collide_mask(self, touched):
                    touched.health -= self.damage
                    self.kill()
                    if SOUND:
                        meteorhit.play()


    # Выстрелы врага
    class LaserBulletAlien(pygame.sprite.Sprite):
        def __init__(self, x, y):
            pygame.sprite.Sprite.__init__(self)

            self.image = load_image('LaserBulletAlien.png')
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            # Ускорение и увеличение урона со временем
            self.speed = 9 + SCORE // 1500
            if self.speed > 30:
                self.speed = 30
            self.damage = 1 + SCORE // 2000

        def update(self):
            if self.rect.right < 0:
                self.kill()

            # Попадание по игроку
            if pygame.sprite.spritecollideany(self, Player):
                touched = pygame.sprite.spritecollideany(self, Player)
                if pygame.sprite.collide_mask(self, touched):
                    touched.health -= self.damage
                    if SOUND:
                        PlayerHit.play()

                    self.kill()

            self.rect.x -= self.speed


    # Класс пришельца
    class Alien(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # Загрузка картинки пришельца и его взрыва
            self.image = load_image('alien.png')
            self.rect = self.image.get_rect()
            self.bangimage1 = load_image('alienbang5.png')
            self.bangimage2 = load_image('alienbang4.png')
            self.bangimage3 = load_image('alienbang3.png')
            self.bangimage4 = load_image('alienbang2.png')
            self.bangimage5 = load_image('alienbang1.png')
            self.rect.x = WIDTH - 1
            self.rect.y = random.randrange(50, HEIGHT - self.rect.height - 50)

            # Ускорение пригельца со временем
            self.speedy = 1 + SCORE // 9000
            if SCORE > 18000:
                self.speedy = 2
            self.speedx = 1 + SCORE // 6000
            if SCORE > 12000:
                self.speedx = 2

            self.health = 5 + SCORE // 3000
            self.mask = pygame.mask.from_surface(self.image)
            # Счетчики для смерти и стрельбы
            self.deathCounter = -1
            self.prev_shot = 0
            self.bumpcounter = 0
            self.monets = 2 + SCORE // 2500

        def update(self):
            global KILLEDALIENS, MONEYGET

            # Загрузка картинок взрыва
            self.deathCounter -= 1
            if self.deathCounter == 32:
                self.image = self.bangimage2
            if self.deathCounter == 24:
                self.image = self.bangimage3
            if self.deathCounter == 16:
                self.image = self.bangimage4
            if self.deathCounter == 8:
                self.image = self.bangimage5

            # Смерть Исчезнновение пришельца
            if self.deathCounter == 0:
                KILLEDALIENS += 1
                MONEYGET += self.monets
                self.kill()

            # Начало анимации смерти
            if self.health < 1 and self.deathCounter < 0:
                if SOUND:
                    alienbang.play()
                self.image = self.bangimage1
                self.deathCounter = 40

            # Пришелец стреляет
            if self.rect.centery in range(spaceship.rect.centery - 30,
                                          spaceship.rect.centery + 30) and SCORE - self.prev_shot > 75:
                self.prev_shot = SCORE
                enemybullet = LaserBulletAlien(self.rect.left, self.rect.centery)
                all_sprites.add(enemybullet)
                enemybullets.add(enemybullet)
                if SOUND:
                    alienpew.play()

            # Пришельцы летают влево вправо вверх вниз
            if self.rect.bottom < 0 or self.rect.top > HEIGHT:
                self.speedy = - self.speedy

            if self.rect.left < 700:
                self.rect.x = 700
                self.speedx = - self.speedx / 2

            if self.rect.left > 1205:
                self.rect.x = 1200
                self.speedx = - self.speedx * 2

            self.rect.x += self.speedx

            self.bumpcounter -= 1

            if self.bumpcounter == 0:
                self.speedy = - self.speedy
            elif self.bumpcounter > 0:
                if bullets:
                    moved = False
                    for bullet in bullets:
                        if bullet.rect.left < self.rect.right:
                            if bullet.rect.centery in range(self.rect.top - 20,
                                                            self.rect.top + self.rect.height // 2 + 20):
                                self.rect.y += self.speedy
                            elif bullet.rect.centery in range(
                                    self.rect.top - 20 + self.rect.height // 2,
                                    self.rect.bottom + 20):
                                self.rect.y -= self.speedy
                            else:
                                if not moved:
                                    moved = True
                                    if self.rect.centery < spaceship.rect.centery:
                                        self.rect.y += self.speedy
                                    if self.rect.centery > spaceship.rect.centery:
                                        self.rect.y -= self.speedy

                        else:
                            if not moved:
                                moved = True
                                if self.rect.centery < spaceship.rect.centery:
                                    self.rect.y += self.speedy
                                if self.rect.centery > spaceship.rect.centery:
                                    self.rect.y -= self.speedy

                else:
                    if self.rect.centery < spaceship.rect.centery:
                        self.rect.y += self.speedy
                    if self.rect.centery > spaceship.rect.centery:
                        self.rect.y -= self.speedy
            # Есть небольшая хаотичность движений
            # Пришелец уворачивается от выстрелов игрока, попутно приближаясь к нему
            elif self.bumpcounter < 0:
                if len(enemy) > 1:
                    movedmoved = False
                    for enemy1 in enemy:
                        if self != enemy1:
                            if not movedmoved:
                                movedmoved = True
                                if pygame.sprite.collide_mask(self, enemy1):
                                    self.bumpcounter = 100
                                    self.speedy = - self.speedy
                                    if type(enemy1) == Alien:
                                        enemy1.bumpcounter = 100
                                        enemy1.speedy = - enemy1.speedy
                                else:
                                    # Спидран по ии поехали
                                    # +- 20 в range(...) это зазор между пулей и пришельцем
                                    if bullets:
                                        moved = False
                                        for bullet in bullets:
                                            if bullet.rect.left < self.rect.right:
                                                if bullet.rect.centery in range(self.rect.top - 20,
                                                                                self.rect.top + self.rect.height // 2 + 20):
                                                    self.rect.y += self.speedy
                                                elif bullet.rect.centery in range(
                                                        self.rect.top - 20 + self.rect.height // 2,
                                                        self.rect.bottom + 20):
                                                    self.rect.y -= self.speedy
                                                else:
                                                    if not moved:
                                                        moved = True
                                                        if self.rect.centery < spaceship.rect.centery:
                                                            self.rect.y += self.speedy
                                                        if self.rect.centery > spaceship.rect.centery:
                                                            self.rect.y -= self.speedy

                                            else:
                                                if not moved:
                                                    moved = True
                                                    if self.rect.centery < spaceship.rect.centery:
                                                        self.rect.y += self.speedy
                                                    if self.rect.centery > spaceship.rect.centery:
                                                        self.rect.y -= self.speedy

                                    else:
                                        if self.rect.centery < spaceship.rect.centery:
                                            self.rect.y += self.speedy
                                        if self.rect.centery > spaceship.rect.centery:
                                            self.rect.y -= self.speedy

                else:
                    # Спидран по ии поехали
                    # +- 20 в range(...) это зазор между пулей и пришельцем
                    if bullets:
                        moved = False
                        for bullet in bullets:
                            if bullet.rect.left < self.rect.right:
                                if bullet.rect.centery in range(self.rect.top - 20,
                                                                self.rect.top + self.rect.height // 2 + 20):
                                    self.rect.y += self.speedy
                                elif bullet.rect.centery in range(self.rect.top - 20 + self.rect.height // 2,
                                                                  self.rect.bottom + 20):
                                    self.rect.y -= self.speedy
                                else:
                                    if not moved:
                                        moved = True
                                        if self.rect.centery < spaceship.rect.centery:
                                            self.rect.y += self.speedy
                                        if self.rect.centery > spaceship.rect.centery:
                                            self.rect.y -= self.speedy

                            else:
                                if not moved:
                                    moved = True
                                    if self.rect.centery < spaceship.rect.centery:
                                        self.rect.y += self.speedy
                                    if self.rect.centery > spaceship.rect.centery:
                                        self.rect.y -= self.speedy

                    else:
                        if self.rect.centery < spaceship.rect.centery:
                            self.rect.y += self.speedy
                        if self.rect.centery > spaceship.rect.centery:
                            self.rect.y -= self.speedy


    class Meteor(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            # Картинки метеора и его взрыв
            self.image = load_image(f'meteor{random.randint(1, 3)}.png')
            self.bangimage1 = load_image('meteorBang5.png')
            self.bangimage2 = load_image('meteorBang4.png')
            self.bangimage3 = load_image('meteorBang3.png')
            self.bangimage4 = load_image('meteorBang2.png')
            self.bangimage5 = load_image('meteorBang1.png')
            self.rect = self.image.get_rect()
            self.rect.x = WIDTH
            # Случайное появление метеоров (Сверхк или снизу)
            if random.randint(1, 2) == 1:
                self.rect.y = random.randrange(0, 400)
                self.speedy = random.randint(0, 1)
            else:
                self.rect.y = random.randrange(400, 800)
                self.speedy = random.randint(-1, 0)

            # Ускорение со временем
            if self.speedy:
                if self.speedy < 0:
                    self.speedy -= SCORE // 2500
                else:
                    self.speedy += SCORE // 2500

            # Ограничение на вертикальную скорость
            if self.speedy > 5:
                self.speedy = 5
            if self.speedy < -5:
                self.speedy = -5

            # Ускорение со временем
            self.rect.y = random.randrange(50, HEIGHT - self.rect.height - 50)
            self.speedx = 2 + SCORE // 2500
            # Ограничение на горизонтальную скорость
            if self.speedx > 8:
                self.speedx = 8

            # Усиление со временем
            self.health = 3 + SCORE // 1500
            self.damage = 2 + SCORE // 1500
            self.mask = pygame.mask.from_surface(self.image)
            # Счетчик анимации взрыва
            self.deathCounter = -1

        def update(self):
            global KILLEDMETEORS, MONEYGET
            self.deathCounter -= 1
            # Анимация взрыва
            if self.deathCounter == 32:
                self.image = self.bangimage2
            if self.deathCounter == 24:
                self.image = self.bangimage3
            if self.deathCounter == 16:
                self.image = self.bangimage4
            if self.deathCounter == 8:
                self.image = self.bangimage5

            # Движение
            self.rect.x -= self.speedx
            self.rect.y += self.speedy

            if self.deathCounter == 0:
                KILLEDMETEORS += 1
                self.kill()
            # Начало анимации взрыва
            if self.health < 1 and self.deathCounter < 0:
                MONEYGET += 1 + SCORE // 3000
                if SOUND:
                    meteorbang.play()
                self.image = self.bangimage1
                self.deathCounter = 40

            # Столкновение с игроком
            if pygame.sprite.collide_mask(self, spaceship) and self.deathCounter < 0:
                spaceship.health -= self.damage
                self.damage = 0
                if SOUND:
                    meteorbangplayer.play()
                self.image = self.bangimage1
                self.deathCounter = 40

            # Вылет за экран = смерть
            if self.rect.right < 0:
                self.kill()

    # Класс кнопки
    class Button(pygame.sprite.Sprite):
        def __init__(self, name, x, y):
            pygame.sprite.Sprite.__init__(self)
            # Все кнопки для удобства имеют схожие названия
            self.image = load_image(f'Button{name}.png')
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

    # Картинка курсора загружается 1 раз
    cursor = load_image('cursor.png')
    # Отображение курсора на месте мышки
    def ShowCursor():
        x, y = pygame.mouse.get_pos()
        if pygame.mouse.get_focused():
            screen.blit(cursor, (x, y))


    # Задний фон меню тоже загружается один раз
    Startbackground = load_image('StartMenuFon.png')
    Startbackground2 = load_image('StartMenuFon.png')

    Startbackground_rect = Startbackground.get_rect()
    Startbackground_rect2 = Startbackground.get_rect()
    Startbackground_rect2.x = 1500

    # Движение фона в меню вынесено в отдельную функцию для единства фона в главном меню и меню улечшений
    def ShowStartBackground():
        Startbackground_rect.x -= 1
        Startbackground_rect2.x -= 1

        screen.blit(Startbackground, Startbackground_rect)
        screen.blit(Startbackground2, Startbackground_rect2)

        if Startbackground_rect.right == 0:
            Startbackground_rect.x = 1500

        if Startbackground_rect2.right == 0:
            Startbackground_rect2.x = 1500


    # Главное меню
    def StartGame():

        global MUSIC, SOUND

        #Музыка
        start_sprites = pygame.sprite.Group()
        MusicPlayer.load('data/music_fon.mp3')

        if not MusicPlayer.get_busy():
            MusicPlayer.play(-1)

        #Кнопки
        PlayButton = Button('Play', 490, 260)
        UpgradeButton = Button('Upgrade', 490, 360)
        ExitButton = Button('Exit', 490, 460)

        musicButton = Button('MusicOn', 45, HEIGHT - 40)
        soundButton = Button('SoundOn', 0, HEIGHT - 40)

        start_sprites.add(PlayButton)
        start_sprites.add(UpgradeButton)
        start_sprites.add(ExitButton)

        # Текст рекорда
        font = pygame.font.Font(None, 50)
        text = font.render(f"BEST : {PREV_BEST}", True, (255, 216, 0))

        coin = load_image('Coin.png')

        runningStartGame = True

        while runningStartGame:
            clock.tick(FPS)

            # Определение кнопки музыки и звука
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

            # Задний офн
            ShowStartBackground()

            # Показ монеток выравнивается
            showmoney = font.render(f" : {MONEY}", True, (255, 216, 0))
            screen.blit(showmoney, (WIDTH - showmoney.get_width() - 5, 0))
            screen.blit(text, (0, 0))

            screen.blit(coin, (WIDTH - showmoney.get_width() - 50, 0))

            start_sprites.draw(screen)

            # В самом конце отображается курсор
            ShowCursor()
            pygame.display.flip()

            # Ожидаем нажатия на кнопки
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



    # Меню улучшений
    def UpgradeGame():

        global MONEY, LEVEL_SPD, LEVEL_DUR, LEVEL_DMG, SOUND

        upgrade_sprites = pygame.sprite.Group()

        #Кнопки
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

        # Текст и картинки
        titleDur = font.render(f"Прочность", True, textcolor)
        titleSpd = font.render(f"Скорость", True, textcolor)
        titleDmg = font.render(f"Урон", True, textcolor)

        coin = load_image('Coin.png')

        gun = load_image('gun.png')
        body = load_image('body.png')
        motor = load_image('motor.png')

        runningUpgradeGame = True

        while runningUpgradeGame:
            clock.tick(FPS)

            screen.fill(BLACK)
            ShowStartBackground()

            # Бортики
            pygame.draw.line(screen, (0, 0, 0,), (400, 0), (400, HEIGHT), 2)
            pygame.draw.line(screen, (0, 0, 0,), (800, 0), (800, HEIGHT), 2)

            # Отрисовка всего
            screen.blit(titleDur, (110, 100))
            screen.blit(titleSpd, (520, 100))
            screen.blit(titleDmg, (958, 100))

            showmoney = font.render(f" : {MONEY}", True, (255, 216, 0))
            screen.blit(showmoney, (WIDTH - showmoney.get_width() - 5, 0))
            screen.blit(coin, (WIDTH - showmoney.get_width() - 50, 0))

            costDur = font.render(f"Цена: {2 + LEVEL_DUR * 2}", True, textcolor)
            costSpd = font.render(f"Цена: {5 + LEVEL_SPD * 7}", True, textcolor)
            costDmg = font.render(f"Цена: {3 + LEVEL_DMG * 5}", True, textcolor)

            screen.blit(costDur, (200 - costDur.get_size()[0] // 2, 350))
            screen.blit(costSpd, (600 - costDmg.get_size()[0] // 2, 350))
            screen.blit(costDmg, (1000 - costSpd.get_size()[0] // 2, 350))

            currentDur = font.render(f"Текущая: {5 + LEVEL_DUR}", True, textcolor)
            currentSpd = font.render(f"Текущая: {2 + LEVEL_SPD}", True, textcolor)
            currentDmg = font.render(f"Текущий: {1 + LEVEL_DMG}", True, textcolor)

            screen.blit(currentDur, (200 - currentDur.get_size()[0] // 2, 500))
            screen.blit(currentSpd, (600 - currentSpd.get_size()[0] // 2, 500))
            screen.blit(currentDmg, (1000 - currentDmg.get_size()[0] // 2, 500))

            screen.blit(body, (200 - body.get_size()[0] // 2, 650))
            screen.blit(motor, (600 - motor.get_size()[0] // 2, 650))
            screen.blit(gun, (1000 - gun.get_size()[0] // 2, 650))

            upgrade_sprites.draw(screen)

            # В конце курсор
            ShowCursor()
            pygame.display.flip()

            # Ожидание кнопок
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if GoBackButton.rect.collidepoint(event.pos):
                        return

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if UpgradeDURButton.rect.collidepoint(event.pos):
                        if MONEY >= LEVEL_DUR * 2 + 2:
                            MONEY -= LEVEL_DUR * 2 + 2
                            LEVEL_DUR += 1
                            if SOUND:
                                buyUpgrade.play()
                        else:
                            if SOUND:
                                noMoney.play()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if UpgradeDMGButton.rect.collidepoint(event.pos):
                        if MONEY >= LEVEL_DMG * 5 + 3:
                            MONEY -= LEVEL_DMG * 5 + 3
                            LEVEL_DMG += 1
                            if SOUND:
                                buyUpgrade.play()
                        else:
                            if SOUND:
                                noMoney.play()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if UpgradeSPDButton.rect.collidepoint(event.pos):
                        if MONEY >= LEVEL_SPD * 7 + 5:
                            MONEY -= LEVEL_SPD * 7 + 5
                            LEVEL_SPD += 1
                            if SOUND:
                                buyUpgrade.play()
                        else:
                            if SOUND:
                                noMoney.play()

                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        return


    # Сама игра
    def Game():

        # Необходимые переменные
        global SCORE, spaceship, MUSIC, KILLEDALIENS, KILLEDMETEORS
        KILLEDALIENS = 0
        KILLEDMETEORS = 0
        SCORE = 0
        runningGame = True
        MONEYGET = 0

        spaceship = SpaceShip()
        Player.add(spaceship)
        all_sprites.add(spaceship)
        prev_alien = 0

        # Счетчик убитых врагов
        killedAliens = load_image('killedAliensCounter.png')
        killedMeteors = load_image('killedMeteorsCounter.png')

        # Создание заднего фона
        background = load_image('fon3.png')
        background2 = load_image('fon3.png')
        background_rect = background.get_rect()
        background_rect2 = background.get_rect()
        background_rect2.x = WIDTH

        health = load_image('Health.png')

        font = pygame.font.Font(None, 50)

        count = pygame.mixer.Sound('data/count.wav')
        go = pygame.mixer.Sound('data/go.wav')

        # Счетчик перед началом игры
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

            if not MUSIC:
                MusicPlayer.stop()

            # В случае смерти корабля анимация взрыва и вызов конца игры
            if spaceship.health < 1:
                MusicPlayer.stop()
                alienpew.stop()
                pew.stop()
                screen.fill(BLACK)
                screen.blit(background, background_rect)
                screen.blit(background2, background_rect2)
                bullets.draw(screen)
                enemybullets.draw(screen)
                enemy.draw(screen)
                backg = screen.copy()
                counter = 50
                x, y = spaceship.rect.centerx, spaceship.rect.centery
                if SOUND:
                    pygame.mixer.Sound('data/lastBang.wav').play()
                while counter > 0:
                    screen.blit(backg, (0, 0))
                    clock.tick(100)
                    if counter == 50:
                        screen.blit(load_image('explosion5.png'), (x - 50, y - 50))
                        pygame.display.flip()
                    if counter == 40:
                        screen.blit(load_image('explosion4.png'), (x - 50, y - 50))
                        pygame.display.flip()
                    if counter == 30:
                        screen.blit(load_image('explosion3.png'), (x - 50, y - 50))
                        pygame.display.flip()
                    if counter == 20:
                        screen.blit(load_image('explosion2.png'), (x - 50, y - 50))
                        pygame.display.flip()
                    if counter == 10:
                        screen.blit(load_image('explosion1.png'), (x - 50, y - 50))
                        pygame.display.flip()
                    counter -= 1
                screen.blit(load_image('explosion1.png'), (x - 50, y - 50))

                for sprite in all_sprites:
                    sprite.kill()
                if EndGame():
                    return True

            # Ожидание паузы Esc
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        if PauseGame():
                            return True

            # Появление метеорв(Ускоряется со временем)
            if SCORE < 60000:
                if SCORE % (150 - (SCORE // 500)) == 0:
                    meteor = Meteor()
                    enemy.add(meteor)
                    meteors.add(meteor)
                    all_sprites.add(meteor)
            else:
                if SCORE % 30 == 0:
                    meteor = Meteor()
                    enemy.add(meteor)
                    meteors.add(meteor)
                    all_sprites.add(meteor)

            # Появление пришельцев
            if SCORE > 1500:
                if len(aliens) < 2:
                    if SCORE - prev_alien > 300:
                        prev_alien = SCORE
                        alien = Alien()
                        enemy.add(alien)
                        all_sprites.add(alien)
                        aliens.add(alien)
                else:
                    prev_alien = SCORE

            # отрисовка заднего фона
            if background_rect.right < 0:
                background_rect.x = background_rect2.right

            if background_rect2.right < 0:
                background_rect2.x = background_rect.right

            background_rect.x -= 4 + SCORE // 6000
            background_rect2.x -= 4 + SCORE // 6000



            # Обновление и отрисовка спрайтов, счетчиков и жизней
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

            killedAlienstext = font.render(f": {KILLEDALIENS}", True, (255, 255, 255))
            screen.blit(killedAlienstext, (1200 - killedAlienstext.get_width(), 0))
            screen.blit(killedAliens, (1200 - killedAlienstext.get_width() - killedAliens.get_width() - 5, 0))

            killedMeteorstext = font.render(f": {KILLEDMETEORS}", True, (255, 255, 255))
            screen.blit(killedMeteorstext,
                        (
                            1200 - killedAlienstext.get_width() - killedAliens.get_width() - killedMeteorstext.get_width() - 10,
                            0))
            screen.blit(killedMeteors, (
                1200 - killedAlienstext.get_width() - killedAliens.get_width() - killedMeteorstext.get_width() - killedMeteors.get_width() - 15,
                0))

            pygame.display.flip()

    # Пауза
    def PauseGame():
        global MUSIC, SOUND

        # Остановка звуков
        alienpew.stop()
        pew.stop()
        PlayerHit.stop()
        alienbang.stop()
        meteorbang.stop()
        meteorhit.stop()

        # Кнопки, задний фон
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

            # Музыка звуки
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

            butts.add(soundButton)
            butts.add(musicButton)

            butts.draw(screen)

            ShowCursor()
            # Курсор
            pygame.display.flip()

            # Ожидание кнопок
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runningPause = False
                    return True
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
                        return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if ContinueButton.rect.collidepoint(event.pos):
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


    # Конец игры
    def EndGame():


        # Текст
        global SCORE, PREV_BEST, MONEY, MONEYGET
        font = pygame.font.Font(None, 50)
        newBest = font.render(f"", True, (255, 216, 0))
        money = font.render(f"Монет получено: {MONEYGET}", True, (255, 216, 0))
        current = font.render(f"Счет: {SCORE}", True, (255, 216, 0))


        # Тексты меняются если побит рекорд
        if SCORE > PREV_BEST:
            PREV_BEST = SCORE
            newBest = font.render(f"Новый рекорд: {SCORE}!", True, (255, 216, 0))
            current = font.render(f"", True, (255, 216, 0))

        MONEY += MONEYGET
        MONEYGET = 0

        EndBackground = screen.copy()
        runningEndGame = True

        butts = pygame.sprite.Group()
        # Кнопки

        MenuButton = Button('Menu', 480, 500)
        MenuButton.rect.x = 600 - MenuButton.rect.width // 2
        butts.add(MenuButton)
        AgainButton = Button('Replay', 480, 400)
        AgainButton.rect.x = 600 - AgainButton.rect.width // 2
        butts.add(AgainButton)

        while runningEndGame:
            clock.tick(FPS)
            screen.fill(BLACK)

            screen.blit(EndBackground, (0, 0))

            # Отрисовка текстов по середине
            screen.blit(newBest, (600 - newBest.get_width() // 2, 300))
            screen.blit(current, (600 - current.get_width() // 2, 300))
            screen.blit(money, (600 - money.get_width() // 2, 350))

            butts.draw(screen)

            ShowCursor()
            # Курсор в конце
            pygame.display.flip()

            # Ожидание нажатия кнопок
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
    except FileNotFoundError: # Файла может не оказаться, тогда рекорд -1
        file = open('data/gamedata.txt', 'w')
        file.write('''-1
    0
    0
    0
    0''')
        file.close()
    except Exception: # Или может нехватить строк, в них будут записаны не числа и т.д. -> рекорд -2
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

    # Создание кораблика и групп спрайтов (должны быть глобальными  чтобы вызываться из классов)
    spaceship = SpaceShip()
    all_sprites = pygame.sprite.Group()
    Player = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemybullets = pygame.sprite.Group()
    enemy = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    meteors = pygame.sprite.Group()
    KILLEDALIENS = 0
    KILLEDMETEORS = 0
    MONEYGET = 0


    # В конце игры запись результатов
    if StartGame():
        file = open('data/gamedata.txt', 'w')
        file.write(f'''{PREV_BEST}
    {MONEY}
    {LEVEL_DUR}
    {LEVEL_DMG}
    {LEVEL_SPD}''')
        file.close()

    pygame.quit()

else:
    # Если некоторых файлов не хватает, то появится окошко со списком недостающих файлов
    screen = pygame.display.set_mode((1200, 800))
    screen.fill((0, 0, 0))
    pygame.display.set_caption('Нехватка данных')
    font = pygame.font.Font(None, 30)
    for i in range(len(notfound)):
        message = font.render(f'Не найден слудующий файл: {notfound[i]}', True, (255, 255, 255))
        screen.blit(message, (0, i * 30))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
