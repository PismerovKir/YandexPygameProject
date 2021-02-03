import pygame
from os import path

WIDTH = 1000
HEIGHT = 800
FPS = 100
BLACK = (0, 0, 0)
RED = (255, 0, 0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()



class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 90))
        self.image = pygame.image.load(path.join("korabl1.png")).convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speedX = 0

    def update(self):
        self.speedX = 0
        k = pygame.key.get_pressed()
        if k[pygame.K_LEFT]:
            self.speedX = -8
        if k[pygame.K_RIGHT]:
            self.speedX = 8
        self.rect.x += self.speedX
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 10:
            self.rect.left = 0



all_sprites = pygame.sprite.Group()
spaceship = SpaceShip()
all_sprites.add(spaceship)


running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()
    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()