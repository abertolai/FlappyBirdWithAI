import pygame
import os
import random

PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs', 'pipe.png')))

class Pipe:
    DISTANCE_TOP_BASE = 180
    SPEED = 9.5

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.pos_top = 0
        self.pos_base = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BASE = PIPE_IMAGE
        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.pos_top = self.height - self.PIPE_TOP.get_height()
        self.pos_base = self.height + self.DISTANCE_TOP_BASE

    def move(self):
        self.x -= self.SPEED

    def draw(self, tela):
        tela.blit(self.PIPE_TOP, (self.x, self.pos_top))
        tela.blit(self.PIPE_BASE, (self.x, self.pos_base))

    def collide(self, passaro):
        bird_mask = passaro.get_mask()
        top_mas = pygame.mask.from_surface(self.PIPE_TOP)
        base_mask = pygame.mask.from_surface(self.PIPE_BASE)

        distance_top = (self.x - round(passaro.x), self.pos_top - round(passaro.y))
        distance_base = (self.x - round(passaro.x), self.pos_base - round(passaro.y))

        top_point = bird_mask.overlap(top_mas, distance_top)
        base_point = bird_mask.overlap(base_mask, distance_base)

        if base_point or top_point:
            return True
        else:
            return False