import time
import sys
import pygame
import random
import tkinter as tk

from Player import Player
from Bandit import Bandit
from Sounds import Sounds 
from Platform import Platform
from Portal import Portal
from Physics import Physics
from Health import Health
from Button import Button
from Checkbox import Checkbox

from enum import Enum
from os import path

# vector
vec = pygame.math.Vector2

# physics
physics = Physics()

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
	INTRO_TEXT2 = "No foreigners are allowed, so everyone that sees you is attacking you."
	INTRO_TEXT3 = "You have to fight back if you want to survive!" 
	INTRO_TEXT4 = "But remember, you'll have to be very careful! The enemies are very powerful," 
	INTRO_TEXT5 = "so you'll have to be very strong to get them all to get out of Emiphia." 
	INTRO_TEXT6 = "Do it as fast as you can to gain more poins. GOOD LUCK!"


	def __init__(self): 

		# resolution 
		root = tk.Tk()

		screen_height = root.winfo_screenheight()

		# change size of window
		if screen_height <= 1080: 
			self.res = 1 
		else: 
			self.res = 1.8 

		# fit to resolution
		Game.WIDTH *= self.res
		Game.HEIGTH *= self.res

		# game window
		Game.WIN = pygame.display.set_mode((Game.WIDTH, Game.HEIGTH))
		pygame.display.set_caption("pixFighter")

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
		self.player = Player(70, 100, self.res, "Player", 100)
		self.pl_vl = 0

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

		# boolean for help
		self.help = False 

		# music paused
		self.music_paused = False 

		# buttons
		self.back = Button(780*self.res, 20*self.res, self.res, 'Back') 
		self.restart = Button(780*self.res, 60*self.res, self.res, 'Restart') 
		self.end = Button(400*self.res, 400*self.res, self.res, 'End') 

		# chackbox
		my_outline_color = (78, 137, 202)
		my_check_color = (22, 61, 105)
		my_font_size = 30
		my_text_offset = (28, 1)
		my_font = "freesansbold"

		self.box = None
		self.idnum = 1 

		self.add_checkbox(Game.WIN, 785, 110, caption="Mute",
            outline_color=my_outline_color, check_color=my_check_color, font_size=my_font_size, font_color=Game.WHITE,
            text_offset=my_text_offset, font=my_font)


	# ------------------- load methods -------------------------------
	def init(self):
		"""
		Method for loading default positions of elements 
		"""
		# background
		self.data['ground_heigth'] = [0, 0]
		self.data['hill_position'] = [0, 100*self.res]
		self.data['floor_position'] = [0, 350*self.res]

		# player 
		self.data['player_position'] = [0, 360*self.res]


	def load(self):
		"""
		Method that loads all the images needed for game
		"""

		# start background 
		self.assets["start"] = pygame.image.load("./textures/Background/Start.jpg").convert()
		self.assets["start"] = pygame.transform.scale(self.assets["start"], (900*self.res, 500*self.res))


		# background lvl 1-3
		self.assets["lvl1_back"] = pygame.image.load("./textures/Background/bg0.png").convert()
		self.assets["lvl1_back"] = pygame.transform.scale(self.assets["lvl1_back"], (900*self.res, 500*self.res))


		self.assets["lvl1_mountain"] = pygame.image.load("./textures/Background/bg2.png")
		self.assets["lvl1_mountain"] = pygame.transform.scale(self.assets["lvl1_mountain"], (900*self.res, 500*self.res))


		self.assets["lvl1_hill"] = pygame.image.load("./textures/Background/bg3.png")
		self.assets["lvl1_hill"] = pygame.transform.scale(self.assets["lvl1_hill"], (900*self.res, 400*self.res))


		self.assets["lvl1_floor"] = pygame.image.load("./textures/Background/bg4.png")
		self.assets["lvl1_floor"] = pygame.transform.scale(self.assets["lvl1_floor"], (900*self.res, 150*self.res)) 

		self.assets["lvl1_floorPL"] = pygame.image.load("./textures/Background/bg4.png")
		self.assets["lvl1_floorPL"] = pygame.transform.scale(self.assets["lvl1_floorPL"], (150*self.res, 150*self.res)) 


		# background lvl 4-7
		self.assets["lvl2_back"] = pygame.image.load("./textures/Background2/sky.png").convert()
		self.assets["lvl2_back"] = pygame.transform.scale(self.assets["lvl2_back"], (900*self.res, 500*self.res))


		self.assets["lvl2_mountain"] = pygame.image.load("./textures/Background2/glacial_mountains.png")
		self.assets["lvl2_mountain"] = pygame.transform.scale(self.assets["lvl2_mountain"], (900*self.res, 500*self.res))


		self.assets["lvl2_hill"] = pygame.image.load("./textures/Background2/cloud_lonely.png")
		self.assets["lvl2_hill"] = pygame.transform.scale(self.assets["lvl2_hill"], (900*self.res, 400*self.res))


		self.assets["lvl2_floor"] = pygame.image.load("./textures/Background2/clouds_mg_3.png")
		self.assets["lvl2_floor"] = pygame.transform.scale(self.assets["lvl2_floor"], (900*self.res, 150*self.res)) 


		self.assets["lvl2_floorPL"] = pygame.image.load("./textures/Background2/clouds_mg_3.png")
		self.assets["lvl2_floorPL"] = pygame.transform.scale(self.assets["lvl2_floorPL"], (150*self.res, 150*self.res)) 


		# background lvl 8-10
		self.assets["lvl3_back"] = pygame.image.load("./textures/Background3/back.png").convert()
		self.assets["lvl3_back"] = pygame.transform.scale(self.assets["lvl3_back"], (900*self.res, 500*self.res))


		self.assets["lvl3_floor"] = pygame.image.load("./textures/Background3/floor.png")
		self.assets["lvl3_floor"] = pygame.transform.scale(self.assets["lvl3_floor"], (900*self.res, 450*self.res))  


		self.assets["lvl3_floorPL"] = pygame.image.load("./textures/Background3/lvl3_platform.png")
		self.assets["lvl3_floorPL"] = pygame.transform.scale(self.assets["lvl3_floorPL"], (150*self.res, 50*self.res))

		# load health image 
		self.assets["health"] = pygame.image.load("./textures/Health/Health.png")
		self.assets["health"] = pygame.transform.scale(self.assets["health"], (50*self.res, 50*self.res)) 

		# load portal image 
		self.assets["portal"] = pygame.image.load("./textures/Portals/portal.png")
		self.assets["portal"] = pygame.transform.scale(self.assets["portal"], (150*self.res, 150*self.res))

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

	#---------------------- checkbox ------------------------------------
	def add_checkbox(self, surface, x, y, color=(230, 230, 230), caption="", outline_color=(0, 0, 0), check_color=(0, 0, 0), font_size=22, font_color=(0, 0, 0), text_offset=(28, 1), font='freesansbold'):
		"""
		Method for adding checkboxes
		:param surface: game window, 
        :param x: x coordinate of checkbox, 
        :param y: y coordinate of chekbox, 
        :param idnum: id of checkbox, 
        :param color: color of checkbox, 
        :param caption: caption of checkbox, 
        :param outline_color: outline color of checkbox, 
        :param check_color: color of a checkbox when it's checked, 
        :param font_size: size of a caption, 
        :param font_color: color of a caption, 
        :param text_offset: distance between checkbox and caption, 
        :param font: font used in caption
		"""
		self.idnum+=1

		box = Checkbox(surface, x, y, self.res, self.idnum, color, caption,
            outline_color, check_color, font_size, font_color, text_offset, font)

		self.box = box 


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
			self.bandits.append(Bandit(random.randint(100, 800), 420, health, speed, power, self.res, is_light)) 


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
			Game.WIN.blit(self.assets["lvl1_floorPL"], [150*self.res, 240*self.res])
			Game.WIN.blit(self.assets["lvl1_floorPL"], [450*self.res, 190*self.res]) 

			# create portal
			if self.current_level == 3 and len(self.bandits) == 0:
				Game.WIN.blit(self.assets["portal"], [450*self.res, 170*self.res])

		elif self.current_level > 3 and self.current_level <= 7:
			Game.WIN.blit(self.assets["lvl2_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl2_mountain"], self.data['ground_heigth'])
			Game.WIN.blit(self.assets["lvl2_hill"], self.data['hill_position'])
			Game.WIN.blit(self.assets["lvl2_floor"], self.data['floor_position']) 
			Game.WIN.blit(self.assets["lvl2_floorPL"], [100*self.res, 195*self.res])
			Game.WIN.blit(self.assets["lvl2_floorPL"], [590*self.res, 215*self.res]) 

			# add sprite for health
			if self.current_level == 5 and len(self.healths) != 0: 
				Game.WIN.blit(self.assets["health"], [620*self.res, 275*self.res]) 

			# create portal
			if self.current_level == 7 and len(self.bandits) == 0:
				Game.WIN.blit(self.assets["portal"], [590*self.res, 200*self.res])

		else: 
			Game.WIN.blit(self.assets["lvl3_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl3_floor"], [0, 80*self.res]) 
			Game.WIN.blit(self.assets["lvl3_floorPL"], [590*self.res, 315*self.res])
			Game.WIN.blit(self.assets["lvl3_floorPL"], [200*self.res, 275*self.res]) 

			# add sprite for health
			if self.current_level == 8 and len(self.healths) != 0: 
				Game.WIN.blit(self.assets["health"], [230*self.res, 240*self.res]) 

			# create portal
			if self.current_level == 10 and len(self.healths) != 0: 
				Game.WIN.blit(self.assets["health"], [620*self.res, 280*self.res]) 

		# draw buttons
		self.back.draw_button(Game.WIN) 
		self.restart.draw_button(Game.WIN) 

		self.box.render_checkbox()


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
		self.draw_text(Game.WIN, f'Health: {round(self.player.hp, 0)}', [255, 255, 255], 450*self.res, 30*self.res, round(30*self.res))
		self.draw_text(Game.WIN, f'Points: {round(self.player.points, 0)}', [255, 255, 255], 90*self.res, 40*self.res, round(20*self.res))
		self.draw_text(Game.WIN, f'Highscore: {round(self.highscore, 0)}', [255, 255, 255], 100*self.res, 70*self.res, round(20*self.res))
		self.draw_text(Game.WIN, 'Press h for help', [255, 255, 255], 810*self.res, 150*self.res, round(20*self.res))


	def draw_text(self, surface, text, color, x, y, font_size): 
		"""
		Method for drawing text on screen
		:param surface: 
		:param text: text that we are drawing 
		:param color: color of the text 
		:param x: x position of the text 
		:param y: y position of the text
		""" 
		font = pygame.font.SysFont('freesansbold', font_size+10)
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
						sys.exit()

				# color the background 
				Game.WIN.fill((215, 157, 207))

				# set text for main screen
				self.draw_text(Game.WIN, "GAME OVER", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, round(80*self.res)) 
				self.draw_text(Game.WIN, "Points: {}".format(self.player.points), [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/3) + 80*self.res, round(30*self.res)) 

				# set the button on the screen
				self.end.draw_button(Game.WIN) 

				# updates display
				pygame.display.update()
			else: 
				# back to TITLE state
				self.game_over = False 
				self.isplaying = False 
				self.end.clicked = False 

				# player data
				self.player.pos = vec(70, 100) 
				self.player.acc = vec(0, 0) 
				self.player.index = 0 
				self.animation_action = "idle" 

				# platforms
				self.platforms.empty()
				self.platforms.add(Platform(0, 380*self.res, Game.WIDTH, 40*self.res))
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
						sys.exit()

				# color the background 
				Game.WIN.fill((43, 178, 70))

				# set text for main screen
				self.draw_text(Game.WIN, "WINNER!", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, round(80*self.res)) 
				self.draw_text(Game.WIN, "Points: {}".format(self.player.points), [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/3) + 80*self.res, round(30*self.res)) 
				self.draw_text(Game.WIN, "TIME BONUS: {}".format(round(extra)), [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/3) + 160*self.res, round(40*self.res)) 

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
			self.pl_vl = 0
			
			# if we click x the game quits
			if event.type == pygame.QUIT: 
				self.write_hs()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				
				# move left 
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					self.player.index = 0 

					# needed for event handling
					if self.pl_vl == 0:
						self.pl_vl = -8*self.res
					
					self.player.control_position(self.pl_vl)
					self.player.vl = -0.12
					self.animation_action = "run"
					self.animation_cooldown = 150
					self.flip = True

				# move right
				elif event.key == pygame.K_RIGHT or event.key == ord('d'): 
					self.player.index = 0

					# needed for event handling
					if self.pl_vl == 0: 
						self.pl_vl = 8*self.res
					
					self.player.control_position(self.pl_vl)
					self.player.vl = -0.12
					self.animation_action = "run" 
					self.animation_cooldown = 150
					self.flip = False 

				# jump
				elif event.key == pygame.K_UP or event.key == ord('w'): 
					self.sounds.jump_sound()
					self.player.index = 0
					self.player.is_jumping = True
					self.animation_action = "jump" 
					self.animation_cooldown = 250

				# attack
				elif event.key == ord('k'):
					self.animation_action = "attack" 
					self.animation_cooldown = 90 
					self.player.attack(self.bandits)
					self.sounds.hit_sound() 

				# help
				elif event.key == ord('h'):
					self.help = True

		
			if event.type == pygame.KEYUP:
				
				# on key ups stop player movement 
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					# needed for event handling
					if self.pl_vl == -8*self.res:
						self.pl_vl = -8*self.res
					else:
						self.pl_vl = 8*self.res

					self.player.control_position(self.pl_vl)
					self.player.vl = 0

				elif event.key == pygame.K_RIGHT or event.key == ord('d'): 
					# needed for event handling
					if self.pl_vl == 8*self.res:
						self.pl_vl = 8*self.res
					else:
						self.pl_vl = -8*self.res
						
					self.player.control_position(self.pl_vl)
					self.player.vl = 0

				elif event.key == ord('k'):
					self.animation_cooldown = 200 

				# help
				elif event.key == ord('h'):
					self.help = False

				# check if any key on a keyboard is pressed, to set sprite movement to idle
				keys = pygame.key.get_pressed() 

				if True not in keys:
					self.player.index = 0 
					self.animation_action = "idle" 
			
			# check if checkbox is pressed
			if event.type == pygame.MOUSEBUTTONDOWN:
				self.box.update_checkbox(event)
			self.pl_vl = 0


	def get_events_title(self):
		"""
		Method for event managing
		"""

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 
			
			# if we click x the game quits
			if event.type == pygame.QUIT: 
				self.write_hs()
				sys.exit()

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
			if not (bandit.pos.x <= (self.player.pos.x + 30*self.res) and bandit.pos.x >= self.player.pos.x - 30*self.res):
				dx, dy = self.player.pos.x - bandit.pos.x, self.player.pos.y - bandit.pos.y
				# check for direction of player
				if dx > 0:
					bandit.acc = vec(bandit.velocity, 0)
				else:
					bandit.acc = bandit.acc = vec(-bandit.velocity, 0)

				# move bandits until they reach the player
				bandit.move_towards_player(self.player, Game.WIDTH) 
			else:
				# bandits jump if player is on platform
				if not (bandit.pos.y <= self.player.pos.y + 30*self.res) and self.player.is_jumping == False: 
					bandit.jumping()

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

		self.player.vel = vec(0, 0)
		self.player.index = 0 
		self.animation_action = "idle"

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

						self.platforms.empty()
						self.platforms.add(Platform(0, 380*self.res, Game.WIDTH, 40*self.res))

						self.state = State.LVL1 
						self.current_level = 0 
						self.isplaying = False
						
						self.player.points = 0 
						self.player.extra_p = 300
						self.player.pos = vec(70, 100)

					# check if player is_jumping boolean is True
					if self.player.is_jumping:
						self.player.jumping() 

					# check for platforms (jump only if the player is falling)
					if self.player.vel.y > 0:
						hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
						if hits:
							self.player.pos.y = hits[0].rect.top
							self.player.vel.y = 0 

					for bandit in self.bandits:
						if bandit.vel.y > 0:
							hits = pygame.sprite.spritecollide(bandit, self.platforms, False)
							if hits:
								bandit.pos.y = hits[0].rect.top
								bandit.vel.y = 0 

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

					# check if music checkbox is checked/unchecked and mute/unmute
					if self.box.checked and self.music_paused == False: 
						self.sounds.pause_music()
						self.music_paused = True
					if not self.box.checked and self.music_paused == True: 
						self.sounds.unpause_music() 
						self.music_paused = False

					# draws player
					self.player.update_movement(Game.WIDTH)
					self.draw_player(self.animation_action, self.flip, self.animation_cooldown) 

					# bandit update
					self.bandit_update()

					# draws bandit
					self.draw_bandit(self.player)  

					# draws data of a player 
					self.draw_player_data() 

					# draw help
					if self.help:
						self.draw_text(Game.WIN, "Help:", [255, 255, 255], 850*self.res, 370*self.res, round(23*self.res))
						self.draw_text(Game.WIN, "Movement: arrows", [255, 255, 255], 793*self.res, 410*self.res, round(20*self.res))
						self.draw_text(Game.WIN, "Attack: k", [255, 255, 255], 840*self.res, 440*self.res, round(20*self.res))

					# updates display
					pygame.display.update() 
				
				else:
					self.write_hs()
					self.state = State.TITLE
					self.isplaying = False

					self.player.pos = vec(70, 100)

					self.platforms.empty()
					self.platforms.add(Platform(0, 380*self.res, Game.WIDTH, 40*self.res))
			
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

			# background image
			Game.WIN.blit(self.assets["start"], [0, 0])

			# set text for main screen
			self.draw_text(Game.WIN, "pixFighter", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7, round(80*self.res))

			self.draw_text(Game.WIN, Game.INTRO_TEXT1, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 80*self.res, round(20*self.res)) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT2, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 120*self.res, round(20*self.res))
			self.draw_text(Game.WIN, Game.INTRO_TEXT3, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 160*self.res, round(20*self.res)) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT4, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 200*self.res, round(20*self.res)) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT5, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 240*self.res, round(20*self.res)) 
			self.draw_text(Game.WIN, Game.INTRO_TEXT6, [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 280*self.res, round(20*self.res)) 

			self.draw_text(Game.WIN, "Arrows: move, K: attack", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/7 + 340*self.res, round(25*self.res))

			self.draw_text(Game.WIN, "Press enter to start the game", [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/2) + 220*self.res, round(20*self.res))

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
		floor = Platform(0, 380*self.res, Game.WIDTH, 40*self.res)
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
				self.pl_vl = 0
				self.player.acc = vec(0, 0)
			# level states
			else:
				if self.state == State.LVL1: 
					# create platforms for this level
					platform2 = Platform(150*self.res, 250*self.res, 25*self.res, 150*self.res) 
					platform3 = Platform(450*self.res, 200*self.res, 25*self.res, 150*self.res) 

					# adds platforms to group
					self.platforms.add(platform2)
					self.platforms.add(platform3)

					# set data
					self.player.start_time = time.time()
					self.player.extra_p = 300
					self.player.points = 0 

					# create bandits and run level
					self.create_bandits(1, 100, (2, 4), 1)

					self.isplaying = True
					self.main()
				elif self.state == State.LVL2: 
					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1) 

					self.isplaying = True
					self.main()
				elif self.state == State.LVL3: 
					# create a portal
					portal1 = Portal(450*self.res, 180*self.res, self.res)
					self.portals.add(portal1)

					# create bandits and run level
					self.create_bandits(3, 100, (2, 5), 1) 

					self.isplaying = True 
					self.main()
				elif self.state == State.LVL4: 
					# remove old platforms
					self.platforms.remove(platform2)
					self.platforms.remove(platform3) 

					# create platforms for this level
					platform4 = Platform(100*self.res, 200*self.res, 25*self.res, 150*self.res) 
					platform5 = Platform(590*self.res, 220*self.res, 25*self.res, 150*self.res) 

					# add platforms to group
					self.platforms.add(platform4)
					self.platforms.add(platform5)  

					# player falls
					self.player.pos = vec(70, 100)

					# create bandits and run level
					self.create_bandits(2, 100, (2, 3), 1)
					self.create_bandits(2, 150, (3, 7), 1.2, False)

					self.isplaying = True
					self.main() 
				elif self.state == State.LVL5: 
					# add health 
					hl1 = Health(620*self.res, 215*self.res, self.res)
					self.healths.add(hl1)

					# create bandits and run level
					self.create_bandits(2, 100, (2, 4), 1.2)
					self.create_bandits(3, 200, (3, 7), 1.3, False)

					self.isplaying = True
					self.main()
				elif self.state == State.LVL6: 
					# removes health from group
					self.healths.remove(hl1)

					# create bandits and run level
					self.create_bandits(3, 100, (2, 4), 1.2)
					self.create_bandits(3, 200, (3, 7), 1.3, False)

					self.isplaying = True
					self.main()
				elif self.state == State.LVL7: 
					# create a portal
					portal2 = Portal(590*self.res, 200*self.res, self.res)
					self.portals.add(portal2)

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.2)
					self.create_bandits(5, 200, (3, 8), 1.3, False)

					self.isplaying = True 
					self.main()
				elif self.state == State.LVL8: 
					# add health 
					hl2 = Health(230*self.res, 180*self.res, self.res)
					self.healths.add(hl2)

					# remove current platforms
					self.platforms.remove(platform4)
					self.platforms.remove(platform5) 

					# add new platforms
					platform6 = Platform(200*self.res, 180*self.res, 25*self.res, 150*self.res) 
					platform7 = Platform(590*self.res, 220*self.res, 25*self.res, 150*self.res)
					self.platforms.add(platform6)
					self.platforms.add(platform7) 

					# player falls
					self.player.pos = vec(70, 100)

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.2)
					self.create_bandits(6, 200, (3, 6), 1.3, False)

					self.isplaying = True
					self.main()
				elif self.state == State.LVL9: 
					# removes healths from group
					self.healths.remove(hl2) 

					# create bandits and run level
					self.create_bandits(2, 100, (2, 5), 1.4)
					self.create_bandits(7, 200, (3, 6), 1.5, False)

					self.isplaying = True
					self.main()
				elif self.state == State.LVL10: 
					# add health 
					hl3 = Health(620*self.res, 220*self.res, self.res)
					self.healths.add(hl3)

					# create bandits and run level
					self.create_bandits(4, 100, (2, 5), 1.4)
					self.create_bandits(6, 200, (3, 6), 1.6, False)

					self.isplaying = True
					self.main()
				elif self.state == State.LVL11: 
					# remove health from group
					self.healths.remove(hl3)

					# create bandits and run level
					self.create_bandits(11, 200, (3, 6), 2, False)

					self.isplaying = True
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