import pygame
from pygame.locals import *

WIDTH = 700
HEIGHT = 500
FPS = 30
fpsClock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('judge')

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

state = 'run1'
jumpy = 0
jumpt = 0
x = 0
block = []
for i in range(20):
	block.append(1000+i*500)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
music = pygame.mixer.Sound("horse.wav")
collect = pygame.mixer.Sound("collect.wav")
fail = pygame.mixer.Sound("fail.wav")
music.play(loops=-1)

while True:
	DISPLAYSURF.blit(IMAGEDICT['back'],(0,0))
	for event in pygame.event.get():				
		pygame.event.clear() #pump()?
		pressed = pygame.key.get_pressed()
		if pressed[K_SPACE]:
			state = 'jump'
			pygame.draw.ellipse(screen, (0,0,255), pygame.Rect(400,250,100,100), 0)
		elif pressed[K_f] or pressed[K_j]:
			pygame.draw.ellipse(screen, (255,0,0), pygame.Rect(300,250,100,100), 0)
			if state == 'run1':			
				state = 'run2'
			elif state == 'run2':
				state = 'run1'

		elif event.type == QUIT:
			pygame.quit()
			sys.exit()

	if state == 'run1':	
		DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0))
	elif state == 'run2':
		DISPLAYSURF.blit(IMAGEDICT['run2'],(0,0))
	if state == 'jump':
		DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0-jumpy))
		jumpy = -14400*((jumpt-0.083)**2)+100  #0.083 100
		jumpt += 0.02
		if jumpt >= 0.166:
			jumpt = 0
			jumpy = 0
			state = 'run1'    
	
	x -= 720/FPS 
	for i in range(3):
		DISPLAYSURF.blit(IMAGEDICT['red'],(x+block[i],0))	

	pygame.draw.line(screen, (255,255,255), (100,0), (100,500))
	pygame.draw.line(screen, (255,255,255), (200,0), (200,500))
	pygame.draw.line(screen, (255,255,255), (300,0), (300,500))
	pygame.draw.line(screen, (255,255,255), (400,0), (400,500))
	pygame.draw.line(screen, (255,255,255), (500,0), (500,500))

	pygame.display.update()
	fpsClock.tick_busy_loop(FPS)



