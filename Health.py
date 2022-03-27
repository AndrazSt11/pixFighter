import pygame

class Health(pygame.sprite.Sprite):
    def __init__(self, x, y, res):
        """
        Health class 
        :param x: x coordinate of health sprite 
        :param y: y coordinate of health sprite 
        :param res: resolution of screen
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30*res, 15*res))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y