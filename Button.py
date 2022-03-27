import pygame
from pygame.locals import *

bg = (204, 102, 0)
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# define global variable
clicked = False
counter = 0

class Button:
		
    # colours for button
    button_col = (179, 21, 153)
    hover_col = (235, 129, 217)
    click_col = (50, 150, 255)
    
    # text color of button
    text_col = white

    # dimensions of button
    width = 100
    height = 30

    def __init__(self, x, y, res, text): 
        """
        BUtton class
        :param x: x coordinate of button
        :param y: y coordinate of button 
        :param res: resolution of button
        :param text: text of the button
        """
        self.x = x
        self.y = y
        self.res = res
        self.text = text
        self.clicked = False 

        self.width = Button.width * self.res
        self.height = Button.height * self.res


    def draw_button(self, screen):
        """
        Method that draws button on the screen 
        :param screen: screen of the game
        """
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        button_rect = Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
                action = True
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(screen, self.button_col, button_rect)

        # add text to button
        font = pygame.font.SysFont('freesansbold.ttf', round(25*self.res))
        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + int(self.width / 2) - int(text_len / 2), self.y + 8)) 
        
        return action