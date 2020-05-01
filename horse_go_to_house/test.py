import pygame
from pygame.locals import *
from pandas.core.common import flatten
import csv
import sys

def main():
	WIDTH = 700
	HEIGHT = 500
	FPS = 60
	fpsClock = pygame.time.Clock()
	DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
	pygame.display.set_caption('test')
	
	IMAGEDICT = {'back': pygame.image.load('pic/back.png'),
				'walkr': pygame.image.load('pic/walkright.png'),
				'walkl': pygame.image.load('pic/walkleft.png'),
				'stop': pygame.image.load('pic/stop.png'),
	    		'run1': pygame.image.load('pic/run1.png'),
	    		'run2': pygame.image.load('pic/run2.png'),
	    		'red': pygame.image.load('pic/red.png'),
	    		'white': pygame.image.load('pic/white.png'),
	    		'yellow': pygame.image.load('pic/yellow.png'),
	    		'mole': pygame.image.load('pic/mole.png'),
	    		'fail': pygame.image.load('pic/fail.png'),
	    		'cloud': pygame.image.load('pic/cloud.png'),
	    		'bird': pygame.image.load('pic/bird.png'),
	    		'house': pygame.image.load('pic/house.png'),
	    		}
	index = -1 #TIMING's index

	TIMING = []	#correct timing　of jump
	csv_file = open("answer.csv", "r", encoding="Shift_jis")
	TIMING_READER = csv.reader(csv_file, skipinitialspace=True)
	for timing in TIMING_READER:
		TIMING.append(timing)
	TIMING = list(flatten(TIMING))

	state = 'run1'
	jumpy = 0
	jumpt = 0
	x = 0
	time = 0

	block = []				#hurdles
	for i in range(20):
		block.append(1000+i*500)
	
	pygame.mixer.quit()
	pygame.mixer.pre_init(buffer=64)
	pygame.init()

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	music = pygame.mixer.Sound("se/horse.wav")
	correct = pygame.mixer.Sound("se/correct.wav")
	correct.set_volume(0.2)
	fail = pygame.mixer.Sound("se/fail.wav")
	music.play(loops=0)
	
	font = pygame.font.Font(None, 30) #フォントの設定

	while True:
		DISPLAYSURF.blit(IMAGEDICT['back'],(0,0))
		for event in pygame.event.get():		
			if event.type == KEYDOWN:
				index += 1
				if event.key == K_SPACE:	
					state = 'jump'
					time = music.get_length()	#音楽の再生時間を取得
					print(time)	#手動入力したtimeを出力
					fail.play()
				elif event.key == K_f or event.key == K_j:
					time = music.get_length()	#音楽の再生時間を取得
					print(time)	#手動入力したtimeを出力
					correct.play()
					if state == 'run1':
						state = 'run2'
					elif state == 'run2':
						state = 'run1'
					pygame.event.clear() 
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()

		if state == 'run1':	
			DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0))
		elif state == 'run2':
			DISPLAYSURF.blit(IMAGEDICT['run2'],(0,0))
		if state == 'jump':
			DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0-jumpy))
			jumpy = -14400*((jumpt-0.083)**2)+100
			jumpt += 0.02
			if jumpt >= 0.166:
				jumpt = 0
				jumpy = 0
				state = 'run1'
#左上テキストの表示
		text = font.render(str(time), True, (0,0,0)) #テキストの設定 str(time-1)	
		screen.blit(text, [0,0]) #テキストの表示
#判定の表示
		'''
		if abs(float(TIMING[index])-time) < 0.1:
			judgement = font.render("perfect!", True, (0,0,0))			
		elif abs(float(TIMING[index])-time) > 0.1:
			judgement = font.render("bad", True, (0,0,0))
		screen.blit(judgement, [200,220])
		'''
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


if __name__ == "__main__":
    main()