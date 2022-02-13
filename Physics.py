import pygame 

class Physics: 
    def __init__(self): 
        """
        Simple physics class
        """
        physics = None 


    def control_position(self, player_acc, acc):
        """
		Contol movement of a player
		:param player_acc: player acceloration 
        :param acc: x and y of acc 
        :return acc
		""" 

        acc.x += player_acc

        return acc 


    def update_movement(self, pos, vel, acc): 
        """
        Update position of a player 
        :param pos: current pos of a player 
        :param vel: velocity of a player
        :param acc: acc of player 
        :return pos: new x and y coordinates 
        """ 

        vel += acc
        pos.y += vel.y + 0.5 * acc.y
        pos += acc

        return pos