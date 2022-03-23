import pygame

class Portal(pygame.sprite.Sprite):
    def __init__(self, x, y):
        """
        Portal class 
        :param x: x coordinate of portal sprite 
        :param y: y coordinate of portal sprite 
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10*1.5, 50*1.5))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y