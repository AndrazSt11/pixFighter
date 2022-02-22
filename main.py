import time
import pygame
import random

from Player import Player
from Bandit import Bandit
from Sounds import Sounds 
from Platform import Platform
from Portal import Portal
from Health import Health
from Button import Button

from enum import Enum
from os import path

# vector
vec = pygame.math.Vector2

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

	# high score file 
	HS_FILE = "highscore.txt" 

	# intro text
	INTRO_TEXT1 = "You've found yourself in a strange place called Emiphia."
	INTRO_TEXT2 = "No foreigners are allowed, so everyone that sees you is attacking you,"
	INTRO_TEXT3 = "so you have to fight back if you want to survive." 
	INTRO_TEXT4 = "But remember, you'll have to be very careful! The enemies are very powerful," 
	INTRO_TEXT5 = "so you'll have to be very strong to get them all to get out of Emiphia." 
	INTRO_TEXT6 = "Do it as fast as you can to gain more poins. GOOD LUCK!"

	# game window
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
		self.highscore = 0

		# declare player
		self.player = Player(70, 100, "Player", 100)

		# list of bandits 
		self.bandits = [] 

		# sprite groups
		self.platforms = pygame.sprite.Group() 
		self.healths = pygame.sprite.Group() 
		self.portals = pygame.sprite.Group()

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

		# boolean game over 
		self.game_over = False 

		# boolean win
		self.finish = False 

		# buttons
		self.back = Button(780, 20, 'Back') 
		self.restart = Button(780, 60, 'Restart') 
		self.end = Button(400, 400, 'End')


	# ------------------- load methods -------------------------------
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

		# start background 
		self.assets["start"] = pygame.image.load("./textures/Background/Start.jpg").convert()
		self.assets["start"] = pygame.transform.scale(self.assets["start"], (900, 500))


		# background lvl 1-3
		self.assets["lvl1_back"] = pygame.image.load("./textures/Background/bg0.png").convert()
		self.assets["lvl1_back"] = pygame.transform.scale(self.assets["lvl1_back"], (900, 500))


		self.assets["lvl1_mountain"] = pygame.image.load("./textures/Background/bg2.png")
		self.assets["lvl1_mountain"] = pygame.transform.scale(self.assets["lvl1_mountain"], (900, 500))


		self.assets["lvl1_hill"] = pygame.image.load("./textures/Background/bg3.png")
		self.assets["lvl1_hill"] = pygame.transform.scale(self.assets["lvl1_hill"], (900, 400))


		self.assets["lvl1_floor"] = pygame.image.load("./textures/Background/bg4.png")
		self.assets["lvl1_floor"] = pygame.transform.scale(self.assets["lvl1_floor"], (900, 150)) 

		self.assets["lvl1_floorPL"] = pygame.image.load("./textures/Background/bg4.png")
		self.assets["lvl1_floorPL"] = pygame.transform.scale(self.assets["lvl1_floorPL"], (150, 150)) 


		# background lvl 4-7
		self.assets["lvl2_back"] = pygame.image.load("./textures/Background2/sky.png").convert()
		self.assets["lvl2_back"] = pygame.transform.scale(self.assets["lvl2_back"], (900, 500))


		self.assets["lvl2_mountain"] = pygame.image.load("./textures/Background2/glacial_mountains.png")
		self.assets["lvl2_mountain"] = pygame.transform.scale(self.assets["lvl2_mountain"], (900, 500))


		self.assets["lvl2_hill"] = pygame.image.load("./textures/Background2/cloud_lonely.png")
		self.assets["lvl2_hill"] = pygame.transform.scale(self.assets["lvl2_hill"], (900, 400))


		self.assets["lvl2_floor"] = pygame.image.load("./textures/Background2/clouds_mg_3.png")
		self.assets["lvl2_floor"] = pygame.transform.scale(self.assets["lvl2_floor"], (900, 150)) 


		self.assets["lvl2_floorPL"] = pygame.image.load("./textures/Background2/clouds_mg_3.png")
		self.assets["lvl2_floorPL"] = pygame.transform.scale(self.assets["lvl2_floorPL"], (150, 150)) 


		# background lvl 8-10
		self.assets["lvl3_back"] = pygame.image.load("./textures/Background3/back.png").convert()
		self.assets["lvl3_back"] = pygame.transform.scale(self.assets["lvl3_back"], (900, 500))


		self.assets["lvl3_floor"] = pygame.image.load("./textures/Background3/floor.png")
		self.assets["lvl3_floor"] = pygame.transform.scale(self.assets["lvl3_floor"], (900, 450))  


		self.assets["lvl3_floorPL"] = pygame.image.load("./textures/Background3/lvl3_platform.png")
		self.assets["lvl3_floorPL"] = pygame.transform.scale(self.assets["lvl3_floorPL"], (150, 50))

		# load health image 
		self.assets["health"] = pygame.image.load("./textures/Health/Health.png")
		self.assets["health"] = pygame.transform.scale(self.assets["health"], (50, 50)) 

		# load portal image 
		self.assets["portal"] = pygame.image.load("./textures/Portals/portal.png")
		self.assets["portal"] = pygame.transform.scale(self.assets["portal"], (150, 150))

		# load highscore from file 
		self.load_hs()


	def load_hs(self):
		"""
		Method for loading old highscore to file
		"""
		# load highscore from file 
		with open('{}'.format(Game.HS_FILE), 'r') as f:
			try:
				self.highscore = int(f.read())
			except: 
				self.highscore = 0 


	def write_hs(self): 
		"""
		Method for saving highscore to file
		"""
		with open('{}'.format(Game.HS_FILE), 'w') as f:
			f.truncate(0) 
			f.write(str(self.highscore))


	#-------------------- create bandit method ---------------------------
	def create_bandits(self, num, health, speed, power, is_light=True):
		"""
		Method for creating bandits
		:param num: number of bandits 
		:param health: health of each bandit
		:param speed: tuple of range for speed 
		:param power: power of a bandit
		:param is_light: boolean parameter for types of bandits
		"""
		for i in range(num): 
			self.bandits.append(Bandit(random.randint(100, 800), 380, health, speed, power, is_light)) 


	#-------------------- draw methods ------------------------------------
	def draw_background(self):
		"""
		Method for drawing background to the window
		"""

		# background for each level 
		if self.current_level <= 3: 
			Game.WIN.blit(self.assets["lvl1_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl1_mountain"], self.data['ground_heigth'])
			Game.WIN.blit(self.assets["lvl1_hill"], self.data['hill_position'])
			Game.WIN.blit(self.assets["lvl1_floor"], self.data['floor_position']) 
			Game.WIN.blit(self.assets["lvl1_floorPL"], [150, 240])
			Game.WIN.blit(self.assets["lvl1_floorPL"], [450, 190]) 

			if self.current_level == 3 and len(self.bandits) == 0:
				Game.WIN.blit(self.assets["portal"], [450, 170])

		elif self.current_level > 3 and self.current_level <= 7:
			Game.WIN.blit(self.assets["lvl2_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl2_mountain"], self.data['ground_heigth'])
			Game.WIN.blit(self.assets["lvl2_hill"], self.data['hill_position'])
			Game.WIN.blit(self.assets["lvl2_floor"], self.data['floor_position']) 
			Game.WIN.blit(self.assets["lvl2_floorPL"], [100, 195])
			Game.WIN.blit(self.assets["lvl2_floorPL"], [590, 215]) 

			if self.current_level == 5 and len(self.healths) != 0: 
				Game.WIN.blit(self.assets["health"], [620, 275]) 

			if self.current_level == 7 and len(self.bandits) == 0:
				Game.WIN.blit(self.assets["portal"], [590, 200])

		else: 
			Game.WIN.blit(self.assets["lvl3_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl3_floor"], [0, 80]) 
			Game.WIN.blit(self.assets["lvl3_floorPL"], [590, 315])
			Game.WIN.blit(self.assets["lvl3_floorPL"], [200, 275]) 

			if self.current_level == 8 and len(self.healths) != 0: 
				Game.WIN.blit(self.assets["health"], [230, 240]) 

			if self.current_level == 10 and len(self.healths) != 0: 
				Game.WIN.blit(self.assets["health"], [620, 280]) 

		# draw buttons
		self.back.draw_button(Game.WIN) 
		self.restart.draw_button(Game.WIN)


	def draw_player(self, action, flip, animation_cooldown): 
		"""
		Method that updates and draws player on the canvas
		:param action: type of action that we are preforming (idle, run, attack)
		:param flip: boolean to check if image is fliped 
		:param animation_cooldown: integer for animation cooldown
		"""
		self.player.update(action, flip, animation_cooldown)
		Game.WIN.blit(self.player.image, [self.player.pos.x, self.player.pos.y])


	def draw_bandit(self, player): 
		"""
		Method for drawing bandits on screen
		:param player: a player that is in the game
		"""
		for bandit in self.bandits:
			bandit.update(player)
			Game.WIN.blit(bandit.image, [bandit.pos.x, bandit.pos.y]) 


	def draw_player_data(self): 
		"""
		Method, that draws health of a player on the screen
		""" 
		font = pygame.font.Font('freesansbold.ttf', 20)
		health = font.render(f'Health: {round(self.player.hp, 0)}', True, [255, 255, 255],None) 
		points = font.render(f'Points: {round(self.player.points, 0)}', True, [255, 255, 255],None) 
		highscore = font.render(f'Highscore: {round(self.highscore, 0)}', True, [255, 255, 255],None) 

		# movement 
		movement = font.render("Movement: arrows", True, [255, 255, 255],None) 
		attack = font.render("Attack: k", True, [255, 255, 255],None)

		textRect = health.get_rect() 
		pointsRect = points.get_rect() 
		highscoreRect = highscore.get_rect() 
		movementRect = movement.get_rect() 
		attackRect = attack.get_rect()

		# set coordinates
		textRect.center = (100, 50) 
		pointsRect.center = (100, 80) 
		highscoreRect.center = (100, 110) 
		movementRect.center = (100, 170)
		attackRect.center = (100, 200)

		# draw on screen
		Game.WIN.blit(health, textRect)
		Game.WIN.blit(points, pointsRect)  
		Game.WIN.blit(highscore, highscoreRect) 
		Game.WIN.blit(movement, movementRect) 
		Game.WIN.blit(attack, attackRect)


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

	
	def draw_game_over(self): 
		"""
		Method for game over state
		"""
		while self.game_over:

			if self.end.clicked == False:
				# inside this for loop we check for different events that occur in pygame
				for event in pygame.event.get(): 
					
					# if we click x the game quits
					if event.type == pygame.QUIT: 
						pygame.quit()

				# color the background 
				Game.WIN.fill((215, 157, 207))

				# set text for main screen
				self.draw_text(Game.WIN, "GAME OVER", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, 80) 
				self.draw_text(Game.WIN, "Points: {}".format(self.player.points), [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/3) + 80, 30) 

				# set the button on the screen
				self.end.draw_button(Game.WIN) 

				# updates display
				pygame.display.update()
			else: 
				# back to TITLE state
				self.game_over = False 
				self.isplaying = False 
				self.end.clicked = False
				self.state = State.TITLE 


	def draw_win(self, extra): 
		"""
		Method for win state
		"""
		while self.finish:

			if self.end.clicked == False:
				# inside this for loop we check for different events that occur in pygame
				for event in pygame.event.get(): 
					
					# if we click x the game quits
					if event.type == pygame.QUIT: 
						pygame.quit()

				# color the background 
				Game.WIN.fill((43, 178, 70))

				# set text for main screen
				self.draw_text(Game.WIN, "WINNER!", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, 80) 
				self.draw_text(Game.WIN, "Points: {}".format(self.player.points), [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/3) + 80, 30) 
				self.draw_text(Game.WIN, "TIME BONUS: {}".format(round(extra)), [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/3) + 160, 40) 

				# set the button on the screen
				self.end.draw_button(Game.WIN) 

				# updates display
				pygame.display.update()
			else: 
				# back to TITLE state
				self.finish = False 
				self.isplaying = False 
				self.end.clicked = False
				self.state = State.TITLE


	#----------------------- event methods ------------------------------
	def get_events(self):
		"""
		Method for event managing
		"""

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 
			
			# if we click x the game quits
			if event.type == pygame.QUIT: 
				self.write_hs()
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				
				# move left 
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					self.player.index = 0
					self.player.control_position(-7)
					self.player.vl = -0.12
					self.animation_action = "run"
					self.animation_cooldown = 150
					self.flip = True

				# move right
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					self.player.index = 0
					self.player.control_position(7)
					self.player.vl = -0.12
					self.animation_action = "run" 
					self.animation_cooldown = 150
					self.flip = False 

				# jump
				if event.key == pygame.K_UP or event.key == ord('w'): 
					self.sounds.jump_sound()
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

			else:
				if event.type == pygame.KEYUP:
					
					# on key ups stop player movement 
					if event.key == pygame.K_LEFT or event.key == ord('a'):
						self.player.control_position(7)
						self.player.vl = 0

					if event.key == pygame.K_RIGHT or event.key == ord('d'):
						self.player.control_position(-7)
						self.player.vl = 0

					if event.key == ord('k'):
						self.animation_cooldown = 200 

				# check if any key on a keyboard is pressed, to set sprite movement to idle
				keys = pygame.key.get_pressed() 

				if True not in keys:
					self.player.index = 0 
					self.animation_action = "idle" 


	def get_events_title(self):
		"""
		Method for event managing
		"""

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 
			
			# if we click x the game quits
			if event.type == pygame.QUIT: 
				self.write_hs()
				pygame.quit()

			if event.type == pygame.KEYUP:
				
				# on enter press start the game
				if event.key == pygame.K_RETURN: 
					self.state = self.levels[0] 
					self.current_level += 1
					self.player.hp = 100 
					self.player.points = 0 
					self.player.extra_p = 300 
					self.isplaying = True


	#--------------------------- update methods ---------------------------------
	def bandit_update(self): 
		"""
		Method for updating bandits
		"""
		for bandit in self.bandits: 
			# move bandits until they reach the player
			if not (bandit.pos.x <= (self.player.pos.x + 30) and bandit.pos.x >= self.player.pos.x - 30):
				bandit.move_towards_player(self.player) 

			# check if bandit is dead
			if bandit.hp <= 0: 
				self.player.points += 10 
				if self.player.points > self.highscore: # check if current points are higher than highscore
					self.highscore += 10 # update high score
				self.sounds.body_hit_sound()
				self.bandits.remove(bandit) 

		if len(self.bandits) == 0: 

			# check if we killed all enemies in all levels
			if self.state == State.LVL11:
				self.isplaying = False 
				self.finish = True
				# get elapsed time
				now = time.time() 
				elapsed = now - self.player.start_time 

				# extra points for faster finishing
				self.player.extra_p -= (int(elapsed)*0.1) 
				if self.player.extra_p < 0:
					self.player.extra_p = 0 
					
				# extra points
				if (self.player.points + self.player.extra_p) > self.highscore:
					self.highscore = round(self.player.points + self.player.extra_p) 

				self.state = State.FINISH 
			
			else:
				if self.current_level in [3, 7]:
					# check if player gets health and update it
					hits = pygame.sprite.spritecollide(self.player, self.portals, True)
					if hits:
						self.sounds.teleport_sound()
						self.isplaying = False 
						self.state = self.levels[self.current_level]
						self.current_level += 1
				else:
					self.isplaying = False 
					# update to new level
					self.state = self.levels[self.current_level]
					self.current_level += 1


	#------------------------ main state loop methods ---------------------------
	def main(self): 
		"""
		Main playing method
		"""

		pygame.event.clear()

		while self.isplaying: 

			# insures that program runs 60FPS
			Game.clock.tick(Game.FPS)

			# event manager function
			self.get_events() 

			if self.player.hp > 0: 

				if self.back.clicked == False: 
					
					# reset all settings to 0
					if self.restart.clicked == True:
						self.write_hs()
						self.player.hp = 100 
						self.bandits = []
						self.state = State.LVL1 
						self.current_level = 0 
						self.isplaying = False
						self.player.points = 0 
						self.player.extra_p = 300
						self.player.pos = vec(70, 100)
						self.player.vel = vec(0, 0)

					# check if player is_jumping boolean is True
					if self.player.is_jumping:
						self.player.jumping() 


					# check for platforms (jump only if the player is falling)
					if self.player.vel.y > 0:
						hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
						if hits:
							self.player.pos.y = hits[0].rect.top
							self.player.vel.y = 0 

					# check if player gets health and update it
					hits = pygame.sprite.spritecollide(self.player, self.healths, True)
					if hits:
						hlth = self.player.hp + 30
						if hlth > 100:
							self.player.hp = 100
						else:
							self.player.hp = hlth 
						self.sounds.healup_sound()

					# draws background
					self.draw_background()

					# draws player
					self.player.update_movement(Game.WIDTH)
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
					self.write_hs()
					self.state = State.TITLE
					self.isplaying = False
					self.player.pos = vec(70, 100)
					self.player.vel = vec(0, 0)
			
			else: 
				self.isplaying = False
				self.game_over = True
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
			#Game.WIN.fill((178, 39, 155))
			Game.WIN.blit(self.assets["start"], [0, 0])

			# set text for main screen
			self.draw_text(Game.WIN, "pixFighter", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7, 80)

			self.draw_text(Game.WIN, Game.INTRO_TEXT1, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 100, 20) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT2, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 140, 20)
			self.draw_text(Game.WIN, Game.INTRO_TEXT3, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 180, 20) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT4, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 220, 20) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT5, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 260, 20) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT6, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 300, 20)

			self.draw_text(Game.WIN, "Press enter to start the game", [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/2) + 200, 20)

			# updates display
			pygame.display.update()


	def execute(self): 
		"""
		Main method for execution of the game
		"""
		# call load functions
		self.init()
		self.load() 

		# create platforms
		floor = Platform(0, 380, Game.WIDTH, 40)
		self.platforms.add(floor)

		pygame.init() 
		
		# start background music
		self.sounds.background_music()

		while self.run: 
			# menu state
			if self.state == State.TITLE: 
				self.current_level = 0
				self.back.clicked = False 
				self.bandits = []
				self.main_title()
			# level states
			else:
				if self.state == State.LVL1: 
					# create platforms for this level
					platform2 = Platform(150, 250, 25, 150) 
					platform3 = Platform(450, 200, 25, 150) 

					# adds platforms to group
					self.platforms.add(platform2)
					self.platforms.add(platform3)

					# set data
					self.player.start_time = time.time()
					self.player.extra_p = 300
					self.player.points = 0
					self.isplaying = True 

					# create bandits and run level
					self.create_bandits(1, 100, (2, 4), 1)
					self.main()
				elif self.state == State.LVL2: 
					self.isplaying = True 

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.2)
					self.main()
				elif self.state == State.LVL3:
					self.isplaying = True 

					# create a portal
					portal1 = Portal(450, 180)
					self.portals.add(portal1)

					# create bandits and run level
					self.create_bandits(3, 100, (2, 5), 1.2)
					self.main()
				elif self.state == State.LVL4: 
					# remove old platforms
					self.platforms.remove(platform2)
					self.platforms.remove(platform3) 

					# create platforms for this level
					platform4 = Platform(100, 200, 25, 150) 
					platform5 = Platform(590, 220, 25, 150) 

					# add platforms to group
					self.platforms.add(platform4)
					self.platforms.add(platform5) 

					# player falls
					self.player.pos = vec(70, 100)
					self.player.vel = vec(0, 0)

					self.isplaying = True

					# create bandits and run level
					self.create_bandits(2, 100, (2, 3), 1.2)
					self.create_bandits(2, 150, (2, 5), 1.3, False)
					self.main() 
				elif self.state == State.LVL5: 
					# add health 
					hl1 = Health(620, 215)
					self.healths.add(hl1)

					self.isplaying = True

					# create bandits and run level
					self.create_bandits(2, 100, (2, 4), 1.2)
					self.create_bandits(3, 200, (2, 5), 1.3, False)
					self.main()
				elif self.state == State.LVL6:  
					# removes health from group
					self.healths.remove(hl1)

					self.isplaying = True

					# create bandits and run level
					self.create_bandits(3, 100, (2, 4), 1.2)
					self.create_bandits(3, 200, (2, 5), 1.3, False)
					self.main()
				elif self.state == State.LVL7: 
					self.isplaying = True 

					# create a portal
					portal2 = Portal(590, 200)
					self.portals.add(portal2)

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.2)
					self.create_bandits(5, 200, (3, 5), 1.3, False)
					self.main()
				elif self.state == State.LVL8: 
					# add health 
					hl2 = Health(230, 180)
					self.healths.add(hl2)

					# remove current platforms
					self.platforms.remove(platform4)
					self.platforms.remove(platform5) 

					# add new platforms
					platform6 = Platform(200, 180, 25, 150) 
					platform7 = Platform(590, 220, 25, 150)
					self.platforms.add(platform6)
					self.platforms.add(platform7) 

					# player falls
					self.player.pos = vec(70, 100)
					self.player.vel = vec(0, 0)

					self.isplaying = True

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.2)
					self.create_bandits(6, 200, (3, 6), 1.3, False)
					self.main()
				elif self.state == State.LVL9: 
					# removes healths from group
					self.healths.remove(hl2) 

					self.isplaying = True

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.2)
					self.create_bandits(7, 200, (3, 6), 1.4, False)
					self.main()
				elif self.state == State.LVL10: 
					# add health 
					hl3 = Health(620, 220)
					self.healths.add(hl3)

					self.isplaying = True

					# create bandits and run level
					self.create_bandits(4, 100, (2, 5), 1.4)
					self.create_bandits(6, 200, (3, 7), 1.7, False)
					self.main()
				elif self.state == State.LVL11: 
					# remove health from group
					self.healths.remove(hl1)
					self.isplaying = True

					# create bandits and run level
					self.create_bandits(11, 200, (3, 7), 1.7, False)
					self.main() 
				elif self.state == State.GAME_OVER: 
					self.write_hs()
					self.draw_game_over() 
				elif self.state == State.FINISH: 
					self.write_hs()
					self.draw_win(self.player.extra_p)


if __name__ == "__main__": 
	game = Game() 

	game.execute()