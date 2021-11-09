import pygame
import os
from Player import Player
from Bandit import Bandit


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


def init():
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


def draw_player(action, flip): 
	player.update(action, flip)
	WIN.blit(player.image, [player.x, player.y])


def draw_bandit(): 

	for bandit in bandits:
		bandit.update()
		WIN.blit(bandit.image, [bandit.x, bandit.y])


def main(): 

	# type of animation 
	animation_action = "idle" 

	flip = False

	run = True

	init()
	load()

	while run: 

		# insures that program runs 60FPS
		clock.tick(FPS)

		# inside this for loop we check for different events that occur in pygame
		for event in pygame.event.get(): 

			if event.type == pygame.QUIT: 
				run = False  

			if event.type == pygame.KEYDOWN:
            
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					player.control_position(-5, 0)
					animation_action = "run"
					flip = True
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					player.control_position(5, 0)
					animation_action = "run" 
					flip = False


			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == ord('a'):
					player.control_position(5, 0) 
					player.index = 0
					animation_action = "idle" 
				if event.key == pygame.K_RIGHT or event.key == ord('d'):
					player.control_position(-5, 0)
					player.index = 0
					animation_action = "idle"

		# draws backgroun
		draw_background()

		# draws player
		player.update_movement()
		draw_player(animation_action, flip)

		# draws bandit
		draw_bandit()

		# updates display
		pygame.display.update()

	pygame.quit() 


if __name__ == "__main__": 
	main()