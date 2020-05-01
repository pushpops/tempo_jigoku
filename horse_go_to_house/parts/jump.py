import pygame
from pygame.locals import *

i = 0.0
a = [i]

for j in range(10):
	i += 0.5
	a.append(i)

WIDTH = 700
HEIGHT = 500
FPS = 30
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('jump')

IMAGEDICT = {'back': pygame.image.load('back.png'),
			'walkr': pygame.image.load('walkright.png'),
			'walkl': pygame.image.load('walkleft.png'),
			'stop': pygame.image.load('stop.png'),
    		'run1': pygame.image.load('run1.png'),
    		'run2': pygame.image.load('run2.png'),
    		'red': pygame.image.load('red.png'),
    		'white': pygame.image.load('white.png'),
    		'yellow': pygame.image.load('yellow.png'),
    		'mole': pygame.image.load('mole.png'),
    		'fail': pygame.image.load('fail.png'),
    		'cloud': pygame.image.load('cloud.png'),
    		'bird': pygame.image.load('bird.png'),
    		'house': pygame.image.load('house.png'),
    		}

state = 'run'
jumpy = 0
jumpt = 0

pygame.init()
while True:
	DISPLAYSURF.blit(IMAGEDICT['back'],(0,0))
	for event in pygame.event.get():		
		if event.type == KEYDOWN:
			state = 'jump'
		elif event.type == QUIT:
			pygame.quit()
			sys.exit()

	if state == 'jump':
		DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0-jumpy))
		jumpy = -14400*((jumpt-0.083)**2)+80
		jumpt += 0.02
		if jumpt >= 0.166:
			jumpt = 0
			jumpy = 0
			state = 'run'
	elif state == 'run':
		DISPLAYSURF.blit(IMAGEDICT['run2'],(0,0))
	
	pygame.display.update()
	fpsClock.tick(FPS)
