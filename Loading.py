# Imports
import pygame, time, sys, threading
import tkinter as tk

class Loading():
    pygame.init()

screen = pygame.display.set_mode((708,512))
pygame.display.set_caption("Loading...Please Wait")

CLOCK = pygame.time.Clock()

WORK = 10000000

LOADING_BG = pygame.image.load("assets/Untitled-2.png")
LOADING_BG_RECT = LOADING_BG.get_rect(center=(354,256))

# Loading Bar and variables
loading_bar = pygame.image.load("assets/Loading Bar.png")
loading_bar_rect = loading_bar.get_rect(center=(354,256))
loading_finished = False
loading_progress = 0
loading_bar_width = 7
    
def doWork():
	# Do some math WORK amount times
	global loading_finished, loading_progress

	for i in range(WORK):
		math_equation = 523687 / 789456 * 89456
		loading_progress = i 

	loading_finished = True

# Thread
threading.Thread(target=doWork).start()

# Game loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

	screen.fill("#FFFFFF")

	loading_bar_width = loading_progress / WORK * 525

	loading_bar = pygame.transform.scale(loading_bar, (int(loading_bar_width), 80))
	loading_bar_rect = loading_bar.get_rect(midleft=(100,257))

	screen.blit(LOADING_BG, LOADING_BG_RECT)
	screen.blit(loading_bar, loading_bar_rect)

	pygame.display.update()
	CLOCK.tick(60)