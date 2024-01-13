import pygame
import os

BIRD_IMAGES = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('../imgs','bird3.png')))
]

class Bird:
    IMGS = BIRD_IMAGES

    #animações da rotação
    MAX_ROTATION = 25
    SPEED_ROTATION = 20
    ANIMATION_TIME = 5

    #atributos do passáro
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = 0
        self.speed = 0
        self.height = self.y
        self.time = 0
        self.image_count = 0
        self.image = self.IMGS[0]

    def jump(self):
        self.speed = -10.5
        self.time = 0
        self.height = self.y

    def move(self):
        #calcular o deslocamento
        self.time += 1
        displacement = 1.5 * (self.time ** 2) + self.speed * self.time

        #restringir o deslocamento
        if displacement > 16:
            displacement = 16
        elif displacement < 0:
            displacement -=2

        self.y += displacement

        #angulo do passaro (para fazer a animação)
        if displacement < 0 or self.y < (self.height + 50):
            if self.angle < self.MAX_ROTATION:
                self.angle = self.MAX_ROTATION
            else:
                if self.angle > -90:
                    self.angle -= self.SPEED_ROTATION

    def draw(self, screen):
        #definir qual image do passaro vai usar
        self.image_count += 1
        if self.image_count < self.ANIMATION_TIME:
            self.image = self.IMGS[0]
        elif self.image_count < self.ANIMATION_TIME * 2:
            self.image = self.IMGS[1]
        elif self.image_count < self.ANIMATION_TIME * 3:
            self.image = self.IMGS[2]
        elif self.image_count < self.ANIMATION_TIME * 4:
            self.image = self.IMGS[1]
        elif self.image_count >= self.ANIMATION_TIME * 4 + 1:
            self.image = self.IMGS[0]
            self.image_count = 0

        #se o passaro estiver caindo eu não vou bater asas
        if self.angle <= -80:
            self.image = self.IMGS[1]
            self.image_count = self.ANIMATION_TIME * 2

        #desenhar a imagem
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        position_center_image = self.image.get_rect(topleft=(self.x, self.y)).center
        rectangle = rotated_image.get_rect(center=position_center_image)
        screen.blit(rotated_image, rectangle.topleft)

    def get_mask(self):
        #pegando a mascara do pássaro (ele divide a imagem em vários retangulos menores (pixels))
        return pygame.mask.from_surface(self.image)