import pygame
import os
import random
from Player import Player
from Bandit import Bandit
from Physics import Physics 
from Sounds import Sounds 
from enum import Enum


class State(Enum): 
	"""
	Class of the main game states
	"""
	TITLE = 1 
	LVL1 = 2
	LVL2 = 3
	LVL3 = 4
	LVL4 = 5
	LVL5 = 6
	LVL6 = 7
	LVL7 = 8
	LVL8 = 9
	LVL9 = 10
	LVL10 = 11 
	LVL11 = 12
	GAME_OVER = 13 
	FINISH = 14


class Game:
	clock = pygame.time.Clock() 

	# constants for creating main surface (new window of this width and heigth)
	WIDTH, HEIGTH = 900, 500
	WHITE = (255, 255 ,255) 
	FPS = 60

	WIN = pygame.display.set_mode((WIDTH, HEIGTH))
	pygame.display.set_caption("pixFighter")

	def __init__(self): 

		# default state
		self.state = State.TITLE 

		# level states 
		self.levels = [State.LVL1, State.LVL2, State.LVL3, State.LVL4, State.LVL5, State.LVL6, State.LVL7, State.LVL8, State.LVL9, State.LVL10, State.LVL11] 
		self.current_level = 0

		# data storing
		self.assets = {}
		self.data = {} 

		# declare player
		self.player = Player(0, 380, "Player", 100)

		# declare bandit 
		self.bandits = [] 

		# declare sounds object 
		self.sounds = Sounds() 

		# default player animations 
		self.animation_action = "idle" 
		self.animation_cooldown = 200
		self.flip = False # boolean for fliping character

		# boolean for running game
		self.run = True 

		# boolean for playing game
		self.isplaying = False 


	# load methods
	def init(self):
		"""
		Method for loading default positions of elements 
		"""
		# background
		self.data['ground_heigth'] = [0, 0]
		self.data['hill_position'] = [0, 100]
		self.data['floor_position'] = [0, 350]

		# player 
		self.data['player_position'] = [0, 360]


	def load(self):
		"""
		Method that loads all the images needed for game
		"""

		# background lvl_1
		self.assets["lvl1_back"] = pygame.image.load("./textures/Background/bg0.png").convert()
		self.assets["lvl1_back"] = pygame.transform.scale(self.assets["lvl1_back"], (900, 500))


		self.assets["lvl1_mountain"] = pygame.image.load("./textures/Background/bg2.png")
		self.assets["lvl1_mountain"] = pygame.transform.scale(self.assets["lvl1_mountain"], (900, 500))


		self.assets["lvl1_hill"] = pygame.image.load("./textures/Background/bg3.png")
		self.assets["lvl1_hill"] = pygame.transform.scale(self.assets["lvl1_hill"], (900, 400))


		self.assets["lvl1_floor"] = pygame.image.load("./textures/Background/bg4.png")
		self.assets["lvl1_floor"] = pygame.transform.scale(self.assets["lvl1_floor"], (900, 150)) 


	def create_bandits(self, num):
		"""
		Method for creating bandits
		"""
		for i in range(num): 
			self.bandits.append(Bandit(random.randint(100, 800), 380, 100)) 


	# draw methods
	def draw_background(self):
		"""
		Method for drawing background to the window
		"""

		# background
		Game.WIN.blit(self.assets["lvl1_back"], [0, 0])
		Game.WIN.blit(self.assets["lvl1_mountain"], self.data['ground_heigth'])
		Game.WIN.blit(self.assets["lvl1_hill"], self.data['hill_position'])
		Game.WIN.blit(self.assets["lvl1_floor"], self.data['floor_position'])


	def draw_player(self, action, flip, animation_cooldown): 
		"""
		Method that updates and draws player on the canvas
		:param action: type of action that we are preforming (idle, run, attack)
		:param flip: boolean to check if image is fliped 
		:param animation_cooldown: integer for animation cooldown
		"""
		self.player.update(action, flip, animation_cooldown)
		Game.WIN.blit(self.player.image, [self.player.x, self.player.y])


	def draw_bandit(self, player): 
		"""
		Method for drawing bandits on screen
		:param player: a player that is in the game
		"""
		for bandit in self.bandits:
			bandit.update(player)
			Game.WIN.blit(bandit.image, [bandit.x, bandit.y]) 


	def draw_player_data(self): 
		"""
		Method, that draws health of a player on the screen
		""" 
		font = pygame.font.Font('freesansbold.ttf', 20)
		health = font.render(f'Health: {round(self.player.hp, 0)}', True, [255, 255, 255],None) 
		points = font.render(f'Points: {round(self.player.points, 0)}', True, [255, 255, 255],None)

		textRect = health.get_rect() 
		pointsRect = points.get_rect()

		textRect.center = (100, 50) 
		pointsRect.center = (100, 80)
		Game.WIN.blit(health, textRect)
		Game.WIN.blit(points, pointsRect) 


	def draw_text(self, surface, text, color, x, y, font_size): 
		"""
		Method for drawing text on screen
		:param surface: 
		:param text: text that we are drawing 
		:param color: color of the text 
		:param x: x position of the text 
		:param y: y position of the text
		""" 
		font = pygame.font.Font('freesansbold.ttf', font_size)
		text_surface = font.render(text, True, color) 
		text_rect = text_surface.get_rect() 
		text_rect.center = (x, y) 
		surface.blit(text_surface, text_rect) 


	# event methods
	def get_events(self):
		"""
		Method for event managing
		"""

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 
			
			# if we click x the game quits
			if event.type == pygame.QUIT: 
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				
				# move left 
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					self.player.index = 0
					self.player.control_position(-5, 0)
					self.animation_action = "run"
					self.animation_cooldown = 150
					self.flip = True

				# move right
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					self.player.index = 0
					self.player.control_position(5, 0)
					self.animation_action = "run" 
					self.animation_cooldown = 150
					self.flip = False 

				# jump
				if event.key == pygame.K_UP or event.key == ord('w'): 
					self.player.index = 0
					self.player.is_jumping = True
					self.animation_action = "jump" 
					self.animation_cooldown = 250

				# attack
				if event.key == ord('k'):
					self.animation_action = "attack" 
					self.animation_cooldown = 90 
					self.player.attack(self.bandits)
					self.sounds.hit_sound()


			if event.type == pygame.KEYUP:

				if event.key == pygame.K_LEFT or event.key == ord('a'):
					self.player.control_position(5, 0)
					self.player.index = 0 
					self.animation_action = "idle"

				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					self.player.control_position(-5, 0)
					self.player.index = 0
					self.animation_action = "idle"

				if event.key == pygame.K_UP or event.key == ord('w'):
					self.player.index = 0
					self.animation_action = "idle"

				if event.key == ord('k'):
					self.player.index = 0
					self.animation_action = "idle"
					self.animation_cooldown = 200 


	def get_events_title(self):
		"""
		Method for event managing
		"""

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 
			
			# if we click x the game quits
			if event.type == pygame.QUIT: 
				pygame.quit()

			if event.type == pygame.KEYUP:
				
				# on enter press start the game
				if event.key == pygame.K_RETURN:
					self.state = self.levels[0]
					self.current_level += 1
					self.isplaying = True


	# update methods
	def bandit_update(self): 
		"""
		Method for updating bandits
		"""
		for bandit in self.bandits: 
			# move bandits until they reach the player
			if not (bandit.x <= (self.player.x + 30) and bandit.x >= self.player.x - 30):
				bandit.move_towards_player(self.player) 

			# check if bandit is dead
			if bandit.hp <= 0: 
				self.player.points += 10
				self.sounds.body_hit_sound()
				self.bandits.remove(bandit) 

		if len(self.bandits) == 0: 
			self.isplaying = False 
			self.state = self.levels[0]
			self.levels = self.levels[1:]


	# main state loop methods
	def main(self): 
		"""
		Main playing method
		"""

		while self.isplaying: 

			# insures that program runs 60FPS
			Game.clock.tick(Game.FPS)

			# event manager function
			self.get_events() 

			if self.player.hp > 0:

				# check if player is_jumping boolean is True
				if self.player.is_jumping:
					self.player.jumping()

				# draws background
				self.draw_background()

				# draws player
				self.player.update_movement()
				self.draw_player(self.animation_action, self.flip, self.animation_cooldown) 

				# bandit update
				self.bandit_update()

				# draws bandit
				self.draw_bandit(self.player)  

				# draws data of a player 
				self.draw_player_data()

				# updates display
				pygame.display.update() 
			
			else: 
				self.isplaying = False
				self.state = State.GAME_OVER


	def main_title(self): 
		"""
		Main title method
		"""
		while self.isplaying != True: 

			# insures that program runs 60FPS
			Game.clock.tick(Game.FPS)

			# event manager function
			self.get_events_title()

			# color the background 
			Game.WIN.fill((178, 39, 155))

			# set text for main screen
			self.draw_text(Game.WIN, "pixFighter", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, 80)
			self.draw_text(Game.WIN, "Press enter to start the game", [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/2) + 100, 20)

			# updates display
			pygame.display.update()


	# main execute method
	def execute(self): 
		"""
		Main method for execution of the game
		"""
		# call load functions
		self.init()
		self.load() 
		pygame.init() 

		self.sounds.background_music()

		while self.run: 
			if self.state == State.TITLE: 
				self.main_title()
			else:
				if self.state == State.LVL1: 
					self.isplaying = True
					self.create_bandits(1)
					self.main()
				elif self.state == State.LVL2: 
					self.isplaying = True
					self.create_bandits(2)
					self.main()
				elif self.state == State.LVL3:
					self.isplaying = True 
					self.create_bandits(3)
					self.main()
				elif self.state == State.LVL4: 
					self.isplaying = True
					self.create_bandits(4)
					self.main() 
				elif self.state == State.LVL5: 
					self.isplaying = True
					self.create_bandits(5)
					self.main()
				elif self.state == State.LVL6: 
					self.isplaying = True
					self.create_bandits(6)
					self.main()
				elif self.state == State.LVL7: 
					self.isplaying = True
					self.create_bandits(7)
					self.main()
				elif self.state == State.LVL8: 
					self.isplaying = True
					self.create_bandits(8)
					self.main()
				elif self.state == State.LVL9: 
					self.isplaying = True
					self.create_bandits(9)
					self.main()
				elif self.state == State.LVL10: 
					self.isplaying = True
					self.create_bandits(10)
					self.main()
				elif self.state == State.LVL11: 
					self.isplaying = True
					self.create_bandits(11)
					self.main() 
				elif self.state == State.GAME_OVER: 
					# color the background 
					Game.WIN.fill((178, 39, 155))

					# set text for main screen
					self.draw_text(Game.WIN, "GAME OVER", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, 80)

					# updates display
					pygame.display.update()



if __name__ == "__main__": 
	game = Game() 

	game.execute()