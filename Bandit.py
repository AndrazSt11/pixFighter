import pygame 
import math
import random
from Sounds import Sounds 
from Physics import Physics

# vector 
vec = pygame.math.Vector2

# physics
physics = Physics()

class Bandit: 
	def __init__(self, x, y, hp, speed, power, is_light): 
		"""
		A class of a bandit
		:param x: starting x coordinate of a player
		:param y: starting y coordinate of a player
		:param hp: health of a user 
		:param velocity: tuple of range for speed
		:param power: power of a bandit
		:param is_light: boolean for changing between light and heavy bandit sprites
		""" 
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10, 15))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)

		# bandit data
		self.pos = vec(x, y)
		self.vel = vec(0, 0) # velocity for moving
		self.acc = vec(0, 0) # acceloration of player
		self.hp = hp
		self.alive = True 
		self.power = power
		self.velocity = random.randint(speed[0], speed[1]) # create a bandit with random speed of running

		# bandit jumping
		self.is_jumping = False
		self.vle = 12
		self.mass = 1

		# animation
		self.animation = {} # dictionary containing images of actions - idle, attack, walk, etc. 
		self.index = 0
		self.update_time = pygame.time.get_ticks() 
		self.animation_cooldown = 100 
		self.action = "idle" 
		self.hurt_time = 0

		# attack
		self.update_time_attack = pygame.time.get_ticks() 

		# sounds
		self.sounds = Sounds()

		# load images for sprites 
		if is_light:
			# sprites of light bandit
			self.animation["idle"] = self.load_sprites("./textures/Sprites/LightBandit/Idle/LightBandit_Idle_{}.png", 3)
			self.animation["run"] = self.load_sprites("./textures/Sprites/LightBandit/Run/LightBandit_Run_{}.png", 7)
			self.animation["attack"] = self.load_sprites("./textures/Sprites/LightBandit/Attack/LightBandit_Attack_{}.png", 7) 		
			self.animation["hurt"] = self.load_sprites("./textures/Sprites/LightBandit/Hurt/LightBandit_Hurt_{}.png", 1) 
		else:
			# sprites of heavy bandit
			self.animation["idle"] = self.load_sprites("./textures/Sprites/Heavy/Idle/HeavyBandit_Idle_{}.png", 3)
			self.animation["run"] = self.load_sprites("./textures/Sprites/Heavy/Run/HeavyBandit_Run_{}.png", 7)
			self.animation["attack"] = self.load_sprites("./textures/Sprites/Heavy/Attack/HeavyBandit_Attack_{}.png", 7) 		
			self.animation["hurt"] = self.load_sprites("./textures/Sprites/Heavy/Hurt/HeavyBandit_Hurt_{}.png", 1) 

		# by default set the animation to run
		animation_data = self.animation["run"]
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


	def update(self, player):
		"""
		Handle animation
		:param action: gives name of action that player is preforming (idle by default)
		:param player: a player that is in the game
		""" 

		if player.pos.x < self.pos.x:
			# update image
			self.image = self.animation[self.action][self.index]
		else: 
			self.image = pygame.transform.flip(self.animation[self.action][self.index], True, False)

		# check for the time between updates
		if pygame.time.get_ticks() - self.update_time > self.animation_cooldown: 
			self.update_time = pygame.time.get_ticks()
			self.index += 1

		# check if bandit has reached the player or near player location, to put animation to idle else to run 
		if self.hurt_time == 5:
			if player.pos.x - 30 <= self.pos.x <= (player.pos.x + 30) and player.pos.y - 30 <= self.pos.y <= (player.pos.y + 30):
				self.action="attack" 
				self.animation_cooldown = 100 
				self.attack_player(player) 
			elif player.pos.x - 30 <= self.pos.x <= (player.pos.x + 30):
				self.action="idle" 
				self.animation_cooldown = 100 
			else: 
				self.action = "run" 
				self.animation_cooldown = 100 

			self.hurt_time = 0
		else:
			self.hurt_time += 1

		# check if index is higher than number of images in the animation
		if self.index >= len(self.animation[self.action]):
			self.index = 0 


	def move_towards_player(self, player, WIDTH):
		"""
		Move bandit towards player
		:param player: a player that bandits are moving towards
		:param WIDTH: width of a game window
		""" 

		# direction vector between player and bandit
		dx, dy = player.pos.x - self.pos.x, player.pos.y - self.pos.y
		dist = math.hypot(dx, dy)

		# check if bandit and player are 0 distance away
		if dist != 0:
			# normalize
			#dx, dy = dx / dist, dy / dist 

			self.acc.y = 2.5
			self.pos = physics.update_movement(self.pos, self.vel, self.acc) 
			self.acc.y = 0

			# wrap aroung the sides of the screen
			if self.pos.x > WIDTH: 
				self.pos.x = -50
			if self.pos.x < -50: 
				self.pos.x = WIDTH

			self.rect.midbottom = self.pos

		# move towards player at current speed
		#self.pos.x += dx * self.velocity 


	def jumping(self): 
		"""
		Calculating jump
		"""
		# calculate force
		self.vle = 12
		force = (1 / 2)*self.mass*(self.vle**2)

		# change y coordinate
		self.pos.y -= force
		self.rect.y -= force
		self.vle = self.vle - 1

		# if object has reached maximum height
		if self.vle < 0:
			self.mass =-1

		# if object reaches its original state
		if self.vle ==-13:
			
			# set the jumping boolean to False 
			self.is_jumping = False
			self.vle = 12
			self.mass = 1 
		

	def attack_player(self, player): 
		"""
		Attack player
		:param player: a player that bandits are attacking 
		"""
		
		# direction vector between player and bandit
		dx, dy = player.pos.x - self.pos.x, player.pos.y - self.pos.y
		dist = math.hypot(dx, dy) 

		# check if bandit and player are 0 distance away
		if dist != 0 and pygame.time.get_ticks() - self.update_time_attack > 680: 
			player.hp -= self.power
			self.update_time_attack = pygame.time.get_ticks()
			self.sounds.hit_sound()

		return player