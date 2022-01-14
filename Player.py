import pygame
from Physics import Physics
import math


# declare physics
physics = Physics()

class Player: 
	def __init__(self, x, y, name, hp): 
		"""
		A class of a player
		:param x: starting x coordinate of a player
		:param y: starting y coordinate of a player
		:param name: name of a player
		:param hp: health of a user
		"""

		# player data
		self.x = x
		self.y = y 
		self.moveX = 0
		self.moveY = 0
		self.name = name
		self.hp = hp
		self.alive = True 
		self.points = 0 

		# player extra points for time 
		self.extra_p = 300
		self.start_time = None

		# player jumping
		self.is_jumping = False
		self.velocity = 9
		self.mass = 1

		# animation 
		self.animation = {} # dictionary containing images of actions - idle, attack, walk, etc. 
		self.index = 0
		self.update_time = pygame.time.get_ticks()
		self.frame = 0

		# idle images
		current_list = []
		for i in range(3): 
			img = pygame.image.load(f"./textures/Player/Player1/adventurer-idle-2-0{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["idle"] = current_list # add action to database of animations 

		# walking images
		current_list = []
		for i in range(5): 
			img = pygame.image.load(f"./textures/Player/Player1/adventurer-run-0{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["run"] = current_list # add action to database of animations

		# walking images
		current_list = []
		for i in range(5): 
			img = pygame.image.load(f"./textures/Player/Player1/adventurer-attack2-0{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["attack"] = current_list # add action to database of animations 

		# jumping images
		current_list = []
		for i in range(3): 
			img = pygame.image.load(f"./textures/Player/Player1/adventurer-jump-0{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["jump"] = current_list # add action to database of animations

		# by default use idle, because player is static
		animation_data = self.animation["idle"]
		self.image = animation_data[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) 


	def update(self, action, flip, cooldown):
		"""
		Handle animation
		:param action: gives name of action that player is preforming (idle by default) 
		:param flip: bool parameter to flip image when moving to left side
		""" 
		if flip:
			# update image
			self.image = pygame.transform.flip(self.animation[action][self.index], True, False)
		else: 
			self.image = self.animation[action][self.index]

		# check for the time between updates
		if pygame.time.get_ticks() - self.update_time > cooldown: 
			self.update_time = pygame.time.get_ticks()
			self.index += 1


		# check if index is higher than number of images in the animation
		if self.index >= len(self.animation[action]):
			self.index = 0 
		

	def control_position(self, x, y):
		"""
		Calculate for how much player is going to move
		:param x: movement on x axis
		:param y: movement on y axis
		"""
		self.moveX, self.moveY = physics.control_position(x, y, self.moveX, self.moveY)


	def update_movement(self): 
		"""
		Move player for calculated distance
		"""
		self.x, self.y = physics.update_movement(self.x, self.y, self.moveX, self.moveY)


	def jumping(self): 
		"""
		Calculating jump
		"""

		# calculate force
		force = (1 / 2)*self.mass*(self.velocity**2) 

		# change y coordinate
		self.y -= force
		self.velocity = self.velocity - 1

		# if object has reached maximum height
		if self.velocity < 0:
			self.mass =-1

		# if object reaches its original state
		if self.velocity ==-10:
			
			# set the jumping boolean to False 
			self.is_jumping = False
			self.velocity = 9
			self.mass = 1 
			 

	def attack(self, bandits): 
		"""
		Function for attacking enemies 
		:param flip: boolean variable if player is fliped
		:param player: player that is in the game
		:param bandits: bandits that are in the game
		"""
		
		for bandit in bandits:
			# direction vector between player and bandit
			dx, dy = self.x - bandit.x, self.y - bandit.y
			dist = math.hypot(dx, dy) 

			# check if bandit and player are 0 distance away
			if dist >= 0 and dist <= 30: 
				bandit.hp -= 20
				bandit.action = "hurt"
				bandit.index = 0
				bandit.animation_cooldown = 300

		