import pygame
pygame.font.init()

class Checkbox:
    def __init__(self, surface, x, y, res, idnum, color=(230, 230, 230), caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1), font='freesansbold'):
        """
        Checkbox class: 
        :param surface: game window, 
        :param x: x coordinate of checkbox, 
        :param y: y coordinate of chekbox, 
        :param res: resolution of checkbox,
        :param idnum: id of checkbox, 
        :param color: color of checkbox, 
        :param caption: caption of checkbox, 
        :param outline_color: outline color of checkbox, 
        :param check_color: color of a checkbox when it's checked, 
        :param font_size: size of a caption, 
        :param font_color: color of a caption, 
        :param text_offset: distance between checkbox and caption, 
        :param font: font used in caption
        """
        self.res = res
        self.surface = surface
        self.x = x * self.res
        self.y = y * self.res
        self.color = color
        self.caption = caption
        self.oc = outline_color
        self.cc = check_color
        self.fs = round(font_size * self.res)
        self.fc = font_color
        self.to = text_offset
        self.ft = font

        #identification for removal and reorginazation
        self.idnum = idnum

        # checkbox object
        self.checkbox_obj = pygame.Rect(self.x, self.y, 12*self.res, 12*self.res)
        self.checkbox_outline = self.checkbox_obj.copy()

        # variables to test the different states of the checkbox
        self.checked = False

    def _draw_button_text(self):
        """
        Method that draws the checkbox caption
        """
        self.font = pygame.font.SysFont(self.ft, self.fs)
        self.font_surf = self.font.render(self.caption, True, self.fc)
        w, h = self.font.size(self.caption)
        self.font_pos = (self.x + self.to[0], self.y + 12 / 2 - h / 2 + 
        self.to[1])
        self.surface.blit(self.font_surf, self.font_pos)

    def render_checkbox(self):
        """
        Method that renders checkbox
        """
        if self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
            pygame.draw.circle(self.surface, self.cc, (self.x + 6*self.res, self.y + 6*self.res), 4*self.res)

        elif not self.checked:
            pygame.draw.rect(self.surface, self.color, self.checkbox_obj)
            pygame.draw.rect(self.surface, self.oc, self.checkbox_outline, 1)
        self._draw_button_text()

    def _update(self, event_object):
        """
        Method that updates the checkbox (clicked/not clicked)
        :param event_object: object of event
        """
        x, y = pygame.mouse.get_pos()
        px, py, w, h = self.checkbox_obj
        if px < x < px + w and py < y < py + w:
            if self.checked:
                self.checked = False
            else:
                self.checked = True

    def update_checkbox(self, event_object):
        """
        Method that calls update function
        :param event_object: object of event
        """
        if event_object.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
            self._update(event_object)
