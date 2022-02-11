import pygame
from Physics import Physics
import math


# declare physics
physics = Physics()

# vector 
vec = pygame.math.Vector2

class Player(pygame.sprite.Sprite): 
	def __init__(self, x, y, name, hp): 
		"""
		A class of a player
		:param x: starting x coordinate of a player
		:param y: starting y coordinate of a player
		:param name: name of a player
		:param hp: health of a user
		""" 

		# needed for sprite colision
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 30))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# player data
		self.pos = vec(x, y)
		self.vel = vec(0, 0) # velocity for moving
		self.acc = vec(0, 0) # acceloration of player
		self.name = name
		self.hp = hp
		self.alive = True 
		self.points = 0 

		# player extra points for time 
		self.extra_p = 300
		self.start_time = None

		# player jumping
		self.is_jumping = False
		self.velocity = 12
		self.mass = 1

		# animation 
		self.animation = {} # dictionary containing images of actions - idle, attack, walk, etc. 
		self.index = 0
		self.update_time = pygame.time.get_ticks()
		self.frame = 0

		# load images for sprites
		self.animation["idle"] = self.load_sprites("./textures/Player/Player1/adventurer-idle-2-0{}.png", 3)
		self.animation["run"] = self.load_sprites("./textures/Player/Player1/adventurer-run-0{}.png", 5)
		self.animation["attack"] = self.load_sprites("./textures/Player/Player1/adventurer-attack2-0{}.png", 5)
		self.animation["jump"] = self.load_sprites("./textures/Player/Player1/adventurer-jump-0{}.png", 3) 

		# by default use idle, because player is static
		animation_data = self.animation["idle"]
		self.image = animation_data[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) 


	def load_sprites(self, path, rg):
		"""
		Method for loading sprites
		:param path: path to the images 
		:param rg: num of images in sprite
		:return current_list: list of sprites
		"""
		current_list = []
		for i in range(rg): 
			img = pygame.image.load(path.format(i))
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img) 

		return current_list


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
		

	def control_position(self, player_acc):
		"""
		Calculate for how much player is going to move
		:param player_acc: player acceloration
		"""
		self.acc = physics.control_position(player_acc, self.acc)


	def update_movement(self): 
		"""
		Move player for calculated distance
		""" 
		self.acc.y = 2.5
		self.pos = physics.update_movement(self.pos, self.vel, self.acc) 
		self.rect.midbottom = self.pos


	def jumping(self): 
		"""
		Calculating jump
		"""
		# calculate force
		force = (1 / 2)*self.mass*(self.velocity**2) 

		# change y coordinate
		self.pos.y -= force
		self.rect.y -= force
		self.velocity = self.velocity - 1

		# if object has reached maximum height
		if self.velocity < 0:
			self.mass =-1

		# if object reaches its original state
		if self.velocity ==-13:
			
			# set the jumping boolean to False 
			self.is_jumping = False
			self.velocity = 12
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
			dx, dy = self.pos.x - bandit.x, self.pos.y - bandit.y
			dist = math.hypot(dx, dy) 

			# check if bandit and player are 0 distance away
			if dist >= 0 and dist <= 30: 
				bandit.hp -= 20
				bandit.action = "hurt"
				bandit.index = 0
				bandit.animation_cooldown = 300

		