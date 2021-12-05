import pygame 
import math
import random


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
		self.moveX = 0
		self.moveY = 0
		self.name = name
		self.hp = hp
		self.alive = True 

		# bandit jumping
		self.is_jumping = False
		self.velocity = random.randint(2,4) # create a bandit with random speed of running
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

		# idle images
		current_list = []
		for i in range(3): 
			img = pygame.image.load(f"./textures/Sprites/Heavy/Idle/HeavyBandit_Idle_{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["idle"] = current_list # add action to database of animations 

		# run images
		current_list = []
		for i in range(7): 
			img = pygame.image.load(f"./textures/Sprites/Heavy/Run/HeavyBandit_Run_{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["run"] = current_list # add action to database of animations

		# attack images
		current_list = []
		for i in range(7): 
			img = pygame.image.load(f"./textures/Sprites/Heavy/Attack/HeavyBandit_Attack_{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["attack"] = current_list # add action to database of animations 

		# hurt images
		current_list = []
		for i in range(1): 
			img = pygame.image.load(f"./textures/Sprites/Heavy/Hurt/HeavyBandit_Hurt_{i}.png")
			img = pygame.transform.scale(img, (150, 100))
			current_list.append(img)
		
		self.animation["hurt"] = current_list # add action to database of animations 

		animation_data = self.animation["run"]
		self.image = animation_data[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = (x, y) 


	def update(self, player):
		"""
		Handle animation
		:param action: gives name of action that player is preforming (idle by default)
		:param player: a player that is in the game
		""" 

		if player.x < self.x:
			# update image
			self.image = self.animation[self.action][self.index]
		else: 
			self.image = pygame.transform.flip(self.animation[self.action][self.index], True, False)

		# check for the time between updates
		if pygame.time.get_ticks() - self.update_time > self.animation_cooldown: 
			self.update_time = pygame.time.get_ticks()
			self.index += 1

		# check if bandit has reached the player or near player location, to put 
		# animation to idle else to run 
		if self.hurt_time == 5:
			if self.x <= (player.x + 30) and self.x >= player.x - 30:
				self.action="attack" 
				self.animation_cooldown = 100 
				self.attack_player(player)
			else: 
				self.action = "run" 
				self.animation_cooldown = 100 

			self.hurt_time = 0
		else:
			self.hurt_time += 1

		# check if index is higher than number of images in the animation
		if self.index >= len(self.animation[self.action]):
			self.index = 0 


	def move_towards_player(self, player):
		"""
		Move bandit towards player
		:param player: a player that bandits are moving towards
		""" 

		# direction vector between player and bandit
		dx, dy = player.x - self.x, player.y - self.y
		dist = math.hypot(dx, dy)

		# check if bandit and player are 0 distance away
		if dist != 0:
			# normalize
			dx, dy = dx / dist, dy / dist

		# move towards player at current speed
		self.x += dx * self.velocity 

	def attack_player(self, player): 
		"""
		Attack player
		:param player: a player that bandits are attacking 
		"""
		
		# direction vector between player and bandit
		dx, dy = player.x - self.x, player.y - self.y
		dist = math.hypot(dx, dy) 

		# check if bandit and player are 0 distance away
		if dist != 0 and pygame.time.get_ticks() - self.update_time_attack > 250: 
			player.hp -= 0.3
			self.update_time_attack = pygame.time.get_ticks()

		return player