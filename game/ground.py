import pygame
import os

GROUND_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs', 'base.png')))

class Ground:
    SPEED = 5
    WIDTH = GROUND_IMAGE.get_width()
    IMAGE = GROUND_IMAGE

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.SPEED
        self.x2 -= self.SPEED

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, tela):
        tela.blit(self.IMAGE, (self.x1, self.y))
        tela.blit(self.IMAGE, (self.x2, self.y))