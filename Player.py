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

		# player data
		self.x = x
		self.y = y 
		self.moveX = 0
		self.moveY = 0
		self.name = name
		self.hp = hp
		self.alive = True

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
		Contol movement of a player
		:param x: new x coordinate
		:param y: new y coordinate
		"""
		self.moveX += x
		self.moveY += y 

	
	def update_movement(self): 
		"""
		Update position of a player 
		""" 

		self.x += self.moveX 
		self.y += self.moveY 

	def hit_sound(self): 
		"""
		Play hit sound
		"""
		# sounds
		pygame.mixer.pre_init(44100, -16, 2, 2048)
		pygame.init()
		pygame.mixer.music.load(f"./sounds/player/player_attack.wav")
		pygame.mixer.music.play()



		