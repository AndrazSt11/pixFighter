import pygame
import os
from Player import Player
from Bandit import Bandit
from Physics import Physics 
from Sounds import Sounds


clock = pygame.time.Clock()

# this creates main surface (new window of this width and heigth)
WIDTH, HEIGTH = 900, 500
WHITE = (255, 255 ,255) 
FPS = 60

# data storing
assets = {}
data = {} 


WIN = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("pixFighter")


# declare player
player = Player(0, 380, "Player", 100)

# declare bandit 
bandits = [Bandit(700, 380, "Bandit1", 100), Bandit(600, 380, "Bandit2", 100)] 

# declare sounds object
sounds = Sounds()


def init():
	"""
	Loads default positions of elements 
	"""
	# background
	data['ground_heigth'] = [0, 0]
	data['hill_position'] = [0, 100]
	data['floor_position'] = [0, 350]

	# player 
	data['player_position'] = [0, 360]


def load():
	"""
	Function that loads all the images needed for game
	"""

	# background lvl_1
	assets["lvl1_back"] = pygame.image.load("./textures/Background/bg0.png").convert()
	assets["lvl1_back"] = pygame.transform.scale(assets["lvl1_back"], (900, 500))


	assets["lvl1_mountain"] = pygame.image.load("./textures/Background/bg2.png")
	assets["lvl1_mountain"] = pygame.transform.scale(assets["lvl1_mountain"], (900, 500))


	assets["lvl1_hill"] = pygame.image.load("./textures/Background/bg3.png")
	assets["lvl1_hill"] = pygame.transform.scale(assets["lvl1_hill"], (900, 400))


	assets["lvl1_floor"] = pygame.image.load("./textures/Background/bg4.png")
	assets["lvl1_floor"] = pygame.transform.scale(assets["lvl1_floor"], (900, 150))


def draw_background():
	"""
	It draws background to the window
	"""

	# background
	WIN.blit(assets["lvl1_back"], [0, 0])
	WIN.blit(assets["lvl1_mountain"], data['ground_heigth'])
	WIN.blit(assets["lvl1_hill"], data['hill_position'])
	WIN.blit(assets["lvl1_floor"], data['floor_position'])


def draw_player(action, flip, animation_cooldown): 
	"""
	Function that updates and draws player on the canvas
	:param action: type of action that we are preforming (idle, run, attack)
	:param flip: boolean to check if image is fliped 
	:param animation_cooldown: integer for animation cooldown
	"""
	player.update(action, flip, animation_cooldown)
	WIN.blit(player.image, [player.x, player.y])


def draw_bandit(player): 
	"""
	It draws bandits on screen
	:param player: a player that is in the game
	"""
	for bandit in bandits:
		bandit.update(player)
		WIN.blit(bandit.image, [bandit.x, bandit.y]) 

def draw_player_health(): 
	"""
	Function, that draws health of a player on the screen
	""" 
	font = pygame.font.Font('freesansbold.ttf', 20)
	text = font.render(f'Health: {round(player.hp, 0)}', True, [255, 255, 255],None)
	textRect = text.get_rect() 
	textRect.center = (100, 50) 
	WIN.blit(text, textRect)


def main(): 
	"""
	Main function 
	"""

	# type of animation 
	animation_action = "idle" 

	# animation cooldown
	animation_cooldown = 200

	# boolean for fliping character
	flip = False

	# boolean for running game
	run = True

	# call load functions
	init()
	load() 
	pygame.init()

	while run: 

		# insures that program runs 60FPS
		clock.tick(FPS)

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 

			if event.type == pygame.QUIT: 
				run = False  

			if event.type == pygame.KEYDOWN:
				
				# move left 
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					player.index = 0
					player.control_position(-5, 0)
					animation_action = "run"
					animation_cooldown = 150
					flip = True

				# move right
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					player.index = 0
					player.control_position(5, 0)
					animation_action = "run" 
					animation_cooldown = 150
					flip = False 

				# jump
				if event.key == pygame.K_UP or event.key == ord('w'): 
					player.index = 0
					player.is_jumping = True
					animation_action = "jump" 
					animation_cooldown = 250

				# attack
				if event.key == ord('k'):
					animation_action = "attack" 
					animation_cooldown = 90 
					player.attack(bandits)
					sounds.hit_sound()


			if event.type == pygame.KEYUP:

				if event.key == pygame.K_LEFT or event.key == ord('a'):
					player.control_position(5, 0)
					player.index = 0 
					animation_action = "idle"

				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					player.control_position(-5, 0)
					player.index = 0
					animation_action = "idle"

				if event.key == pygame.K_UP or event.key == ord('w'):
					player.index = 0
					animation_action = "idle"

				if event.key == ord('k'):
					player.index = 0
					animation_action = "idle"
					animation_cooldown = 200 

		# check if player is_jumping boolean is True
		if player.is_jumping:
			player.jumping()

		# draws background
		draw_background()

		# draws player
		player.update_movement()
		draw_player(animation_action, flip, animation_cooldown) 

		for bandit in bandits: 
			# move bandits until they reach the player
			if not (bandit.x <= (player.x + 30) and bandit.x >= player.x - 30):
				bandit.move_towards_player(player) 

			if bandit.hp <= 0: 
				sounds.body_hit_sound()
				bandits.remove(bandit)

		# draw health of a player 
		draw_player_health()

		# draws bandit
		draw_bandit(player) 

		# updates display
		pygame.display.update()

	pygame.quit() 


if __name__ == "__main__": 
	main()