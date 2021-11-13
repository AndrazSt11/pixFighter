import pygame 

class Physics: 
    def __init__(self): 
        physics = None 


    def control_position(self, x, y, moveX, moveY):
        """
		Contol movement of a player
		:param x: new x coordinate
		:param y: new y coordinate
        :param moveX: updating x value 
        :param moveY: updating y value
		""" 

        moveX += x
        moveY += y 

        return moveX, moveY 


    def update_movement(self, x, y, moveX, moveY): 
        """
        Update position of a player 
        :param x: current x of a player
        :param y: current y of a player 
        :param moveX: updating x value
        :param moveY: updating y value
        """ 
        x += moveX 
        y += moveY 

        return x, y 