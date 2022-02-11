import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        """
        Platform class 
        :param x: x coordinate of platform 
        :param y: y coordinate of platform 
        :param w: width of platform 
        :param h: heigth of platform
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y