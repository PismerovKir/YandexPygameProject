import pygame
import os
import sys


WIDTH = 1000
HEIGHT = 800
FPS = 100
BLACK = (0, 0, 0)
RED = (255, 0, 0)


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





# background = pygame.image.load(os.path.join("data/fon.png")).convert()
# background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
spaceship = SpaceShip()
all_sprites.add(spaceship)
bullets = pygame.sprite.Group()

background = load_image('fon.png')
background2 = load_image('fon.png')
background_rect = background.get_rect()
background_rect2 = background.get_rect()
background_rect2.x =  WIDTH

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
    pygame.display.flip()

pygame.quit()