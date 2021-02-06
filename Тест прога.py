import pygame
import os
import sys
import random

pygame.init()

WIDTH = 1000
HEIGHT = 800
FPS = 100
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SCORE = 0



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

        self.image = pygame.image.load(os.path.join("data\korabl2.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20


    def update(self):

        k = pygame.key.get_pressed()
        self.image = load_image('korabl2.png')

        if k[pygame.K_LEFT]:
            self.image = load_image('korabl1.png')
            self.rect.x += -5
        if k[pygame.K_RIGHT]:
            self.image = load_image('korabl3.png')
            self.rect.x += 5

        if k[pygame.K_UP]:
            self.rect.y += -6
        if k[pygame.K_DOWN]:
            self.rect.y += 6

        if k[pygame.K_SPACE]:
            bul = LaserBulletLong(self.rect.right, self.rect.top + 26)
            all_sprites.add(bul)
            bullets.add(bul)

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

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


    def update(self):
        if self.rect.x > WIDTH:
            self.kill()
        self.rect.x += 10

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_image('alien.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.left < -200 or self.rect.right > HEIGHT + -200:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -50)
            self.speedy = random.randrange(1, 4)

def ShowScore():
    font = pygame.font.Font(None, 50)
    text = font.render(f"{SCORE}", True, (255, 255, 255))
    text_x =  text.get_width()
    text_y = text.get_height()
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (0, 0))
    # pygame.draw.rect(screen, (255, 255, 255), (text_x - 10, text_y - 10,
    #                                        text_w + 20, text_h + 20), 1)




# background = pygame.image.load(os.path.join("data/fon.png")).convert()
# background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
spaceship = SpaceShip()
all_sprites.add(spaceship)
bullets = pygame.sprite.Group()

background = load_image('fon3.png')
background2 = load_image('fon3.png')
background_rect = background.get_rect()
background_rect2 = background.get_rect()
background_rect2.x = WIDTH

aliens = pygame.sprite.Group()
all_sprites.add(spaceship)

for i in range(2):
    alien = Alien()
    all_sprites.add(alien)
    aliens.add(alien)

running = True
while running:
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if background_rect.right < 0:
        background_rect.x = WIDTH

    if background_rect2.right < 0:
        background_rect2.x = WIDTH

    background_rect.x -= 5
    background_rect2.x -= 5



    all_sprites.update()
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    screen.blit(background2, background_rect2)
    all_sprites.draw(screen)
    SCORE += 1
    ShowScore()
    pygame.display.flip()

pygame.quit()