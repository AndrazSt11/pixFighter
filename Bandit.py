import pygame


class Bandit: 
	def __init__(self, x, y, name, hp): 
		"""
		A class of a bandit
		:param x: starting x coordinate of a player
		:param y: starting y coordinate of a player
		:param name: name of a player
		:param hp: health of a user
		"""

		# bandit data
		self.x = x
		self.y = y
		self.name = name
		self.hp = hp
		self.alive = True

		# animation
		self.animation = {} # dictionary containing images of actions - idle, attack, walk, etc. 
		self.index = 0
		self.update_time = pygame.time.get_ticks() 
		self.animation_cooldown = 200

		current_list = []
		for i in range(3): 
			img = pygame.image.load(f"./textures/Sprites/Heavy/Idle/HeavyBandit_Idle_{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["idle"] = current_list # add action to database of animations

		animation_data = self.animation["idle"]

		self.image = animation_data[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) 


	def update(self, action="idle"):
		"""
		Handle animation
		:param action: gives name of action that player is preforming (idle by default)
		"""

		# update image
		self.image = self.animation[action][self.index]

		# check for the time between updates
		if pygame.time.get_ticks() - self.update_time > self.animation_cooldown: 
			self.update_time = pygame.time.get_ticks()
			self.index += 1

		# check if index is higher than number of images in the animation
		if self.index >= len(self.animation[action]):
			self.index = 0
		