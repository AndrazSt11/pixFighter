import time
import pygame
import random
from Player import Player
from Bandit import Bandit
from Physics import Physics 
from Sounds import Sounds 
from Platform import Platform
from enum import Enum 
from Button import Button
from os import path


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

		# list of platforms
		self.platforms = pygame.sprite.Group()

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

		# background lvl 1-3
		self.assets["lvl1_back"] = pygame.image.load("./textures/Background/bg0.png").convert()
		self.assets["lvl1_back"] = pygame.transform.scale(self.assets["lvl1_back"], (900, 500))


		self.assets["lvl1_mountain"] = pygame.image.load("./textures/Background/bg2.png")
		self.assets["lvl1_mountain"] = pygame.transform.scale(self.assets["lvl1_mountain"], (900, 500))


		self.assets["lvl1_hill"] = pygame.image.load("./textures/Background/bg3.png")
		self.assets["lvl1_hill"] = pygame.transform.scale(self.assets["lvl1_hill"], (900, 400))


		self.assets["lvl1_floor"] = pygame.image.load("./textures/Background/bg4.png")
		self.assets["lvl1_floor"] = pygame.transform.scale(self.assets["lvl1_floor"], (900, 150)) 

		self.assets["lvl1_floorPL"] = pygame.image.load("./textures/Background/bg4.png") # test platforms
		self.assets["lvl1_floorPL"] = pygame.transform.scale(self.assets["lvl1_floorPL"], (150, 150)) 

		self.assets["lvl1_floorPL2"] = pygame.image.load("./textures/Background/bg4.png") # test platforms
		self.assets["lvl1_floorPL2"] = pygame.transform.scale(self.assets["lvl1_floorPL2"], (150, 150)) 


		# background lvl 4-7
		self.assets["lvl2_back"] = pygame.image.load("./textures/Background2/sky.png").convert()
		self.assets["lvl2_back"] = pygame.transform.scale(self.assets["lvl2_back"], (900, 500))


		self.assets["lvl2_mountain"] = pygame.image.load("./textures/Background2/glacial_mountains.png")
		self.assets["lvl2_mountain"] = pygame.transform.scale(self.assets["lvl2_mountain"], (900, 500))


		self.assets["lvl2_hill"] = pygame.image.load("./textures/Background2/cloud_lonely.png")
		self.assets["lvl2_hill"] = pygame.transform.scale(self.assets["lvl2_hill"], (900, 400))


		self.assets["lvl2_floor"] = pygame.image.load("./textures/Background2/clouds_mg_3.png")
		self.assets["lvl2_floor"] = pygame.transform.scale(self.assets["lvl2_floor"], (900, 150)) 


		# background lvl 8-10
		self.assets["lvl3_back"] = pygame.image.load("./textures/Background3/back.png").convert()
		self.assets["lvl3_back"] = pygame.transform.scale(self.assets["lvl3_back"], (900, 500))


		self.assets["lvl3_floor"] = pygame.image.load("./textures/Background3/floor.png")
		self.assets["lvl3_floor"] = pygame.transform.scale(self.assets["lvl3_floor"], (900, 450))  


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
		# save highscore to file
		"""
		Method for saving highscore to file
		"""
		with open('{}'.format(Game.HS_FILE), 'w') as f:
			f.truncate(0) 
			f.write(str(self.highscore))



	#-------------------- create bandit method ---------------------------
	def create_bandits(self, num):
		"""
		Method for creating bandits
		"""
		for i in range(num): 
			self.bandits.append(Bandit(random.randint(100, 800), 380, 100)) 


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
			Game.WIN.blit(self.assets["lvl1_floorPL"], [150, 250]) 
			Game.WIN.blit(self.assets["lvl1_floorPL2"], [350, 180])

		elif self.current_level > 3 and self.current_level <= 7:
			Game.WIN.blit(self.assets["lvl2_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl2_mountain"], self.data['ground_heigth'])
			Game.WIN.blit(self.assets["lvl2_hill"], self.data['hill_position'])
			Game.WIN.blit(self.assets["lvl2_floor"], self.data['floor_position']) 

		else: 
			Game.WIN.blit(self.assets["lvl3_back"], [0, 0])
			Game.WIN.blit(self.assets["lvl3_floor"], [0, 80]) 

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
			Game.WIN.blit(bandit.image, [bandit.x, bandit.y]) 


	def draw_player_data(self): 
		"""
		Method, that draws health of a player on the screen
		""" 
		font = pygame.font.Font('freesansbold.ttf', 20)
		health = font.render(f'Health: {round(self.player.hp, 0)}', True, [255, 255, 255],None) 
		points = font.render(f'Points: {round(self.player.points, 0)}', True, [255, 255, 255],None) 
		highscore = font.render(f'Highscore: {round(self.highscore, 0)}', True, [255, 255, 255],None)

		textRect = health.get_rect() 
		pointsRect = points.get_rect() 
		highscoreRect = highscore.get_rect()

		textRect.center = (100, 50) 
		pointsRect.center = (100, 80) 
		highscoreRect.center = (100, 110)
		Game.WIN.blit(health, textRect)
		Game.WIN.blit(points, pointsRect)  
		Game.WIN.blit(highscore, highscoreRect)


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
					self.player.control_position(-5)
					self.player.vl = -0.12
					self.animation_action = "run"
					self.animation_cooldown = 150
					self.flip = True

				# move right
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					self.player.index = 0
					self.player.control_position(5)
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


			if event.type == pygame.KEYUP:

				if event.key == pygame.K_LEFT or event.key == ord('a'):
					self.player.control_position(5)
					self.player.vl = 0
					self.player.index = 0 
					self.animation_action = "idle"

				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					self.player.control_position(-5)
					self.player.vl = 0
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
			if not (bandit.x <= (self.player.pos.x + 30) and bandit.x >= self.player.pos.x - 30):
				bandit.move_towards_player(self.player) 

			# check if bandit is dead
			if bandit.hp <= 0: 
				self.player.points += 10 
				if self.player.points > self.highscore: # check if current points are higher than highscore
					self.highscore += 10 # update high score
				self.sounds.body_hit_sound()
				self.bandits.remove(bandit) 

		if len(self.bandits) == 0: 
			self.isplaying = False 

			# check if we killed all enemies in all levels
			if self.state == State.LVL11:
				self.finish = True
				# get elapsed time
				now = time.time() 
				elapsed = now - self.player.start_time 

				# extra points for faster finishing
				self.player.extra_p -= (int(elapsed)*0.5) 
				if self.player.extra_p < 0:
					self.player.extra_p = 0 
					
				# extra points
				if (self.player.points + self.player.extra_p) > self.highscore:
					self.highscore = round(self.player.points + self.player.extra_p) 

				self.state = State.FINISH 
			
			else:
				# update to new level
				self.state = self.levels[self.current_level]
				self.current_level += 1
				#self.levels = self.levels[self.current_level]


	#------------------------ main state loop methods ---------------------------
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

					# check if player is_jumping boolean is True
					if self.player.is_jumping:
						self.player.jumping() 


					# check for platforms
					hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
					if hits:
						self.player.pos.y = hits[0].rect.top
						self.player.vel.y = 0

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
					self.write_hs()
					self.state = State.TITLE
					self.isplaying = False
			
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
			Game.WIN.fill((178, 39, 155))

			# set text for main screen
			self.draw_text(Game.WIN, "pixFighter", [255, 255, 255], Game.WIDTH/2, Game.HEIGTH/3, 80)
			self.draw_text(Game.WIN, "Press enter to start the game", [255, 255, 255], Game.WIDTH/2, (Game.HEIGTH/2) + 100, 20)

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
		p1 = Platform(0, 380, Game.WIDTH, 40)
		p2 = Platform(150, 250, 25, 150) 
		p3 = Platform(350, 190, 25, 150)
		self.platforms.add(p1)
		self.platforms.add(p2)
		self.platforms.add(p3)

		pygame.init() 

		self.sounds.background_music()

		while self.run: 
			if self.state == State.TITLE: 
				self.current_level = 0
				self.back.clicked = False 
				self.bandits = []
				self.main_title()
			else:
				if self.state == State.LVL1: 
					self.player.start_time = time.time()
					self.player.extra_p = 300
					self.player.points = 0
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
					self.write_hs()
					self.draw_game_over() 
				elif self.state == State.FINISH: 
					self.write_hs()
					self.draw_win(self.player.extra_p)


if __name__ == "__main__": 
	game = Game() 

	game.execute()