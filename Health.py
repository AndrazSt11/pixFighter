import pygame

class Health(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Health class 
        :param x: x coordinate of health sprite 
        :param y: y coordinate of health sprite 
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((80, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y