import pygame


class Player: 
	def __init__(self, x, y, name, hp): 
		"""
		A class of a player
		:param x: starting x coordinate of a player
		:param y: starting y coordinate of a player
		:param name: name of a player
		:param hp: health of a user
		"""
		self.x = x
		self.y = y
		self.name = name
		self.hp = hp
		self.alive = True
		self.animation = []
		self.index = 0
		self.update_time = pygame.time.get_ticks()

		for i in range(3): 
			img = pygame.image.load(f"./textures/Player/Player1/adventurer-idle-2-0{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			self.animation.append(img)
		
		self.image = self.animation[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) 


	def update(self):
		"""
		Handel animation
		"""
		animation_cooldown = 200

		# update image
		self.image = self.animation[self.index]

		# check for the time between updates
		if pygame.time.get_ticks() - self.update_time > animation_cooldown: 
			self.update_time = pygame.time.get_ticks()
			self.index += 1

		# check if index is higher than number of images in the animation
		if self.index >= len(self.animation):
			self.index = 0
		