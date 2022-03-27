import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y, res):
        """
        Portal class 
        :param x: x coordinate of portal sprite 
        :param y: y coordinate of portal sprite 
        :param res: resolution of screen
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10*res, 50*res))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y