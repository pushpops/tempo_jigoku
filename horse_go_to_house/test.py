import pygame
from pygame.locals import *
from pandas.core.common import flatten
import csv
import sys

class Hardles:
	pic = ''
	x = 700
	def __init__(self, pic):
		self.pic = pic
	def show():
		DISPLAYSURF.blit(IMAGEDICT[self.pic],(x,0))
		x -= 24
		return x

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
	    		'bad': pygame.image.load('pic/fail.png'),
	    		'cloud': pygame.image.load('pic/cloud.png'),
	    		'bird': pygame.image.load('pic/bird.png'),
	    		'house': pygame.image.load('pic/house.png'),
	    		}
	J = 0 #index for judge with TIMING
	S = 0 #index for set hardle pictures with TIMING
	INPUT = []	#input data from player
	TIMING = []	#correct timing　of notes and jump
	csv_file = open("answer.csv", "r", encoding="Shift_jis")
	TIMING_READER = csv.reader(csv_file, skipinitialspace=True)
	for timing in TIMING_READER:
		TIMING.append(timing)
	TIMING = list(flatten(TIMING))
	
	hardles = []
	state = 'stop'
	jumpy = 0
	jumpt = 0
	time = 0
	pic = ''
	dist = 0.0
	
	#initialise
	pygame.mixer.quit()
	pygame.mixer.pre_init(buffer=64)
	pygame.init()

	#load SE
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.mixer.music.load("se/horse.wav")
	correct = pygame.mixer.Sound("se/correct.wav")
	correct.set_volume(0.2)
	fail = pygame.mixer.Sound("se/fail.wav")
	pygame.mixer.music.play()
	
	#setting Fonts
	font = pygame.font.Font(None, 30)

	#main game loop
	while True:
		DISPLAYSURF.blit(IMAGEDICT['back'],(0,0)) #draw background
		
		#draw hardles on the ground
		for s in range(S,len(TIMING))
			if TIMING[s]#がハードルだったら(あとでラベル付け作業)
				time = pygame.mixer.music.get_pos()/1000 #get bgm's play time
				if TIMING[s]-time<0.66
					switch (rand = randint(0,3))
						case 0:pic = 'red'
						case 1:pic = 'white'
						case 2:pic = 'yellow'
						case 3:pic = 'mole'
						default: print("error: hardle was'nt chosen properly")
					hardle.append(Hardle(pic))
			else: S = s + 1
		##################対話モードで要確認#########################
		if hardles: #ハードルが空でなかったら
			for h in len(hardles):
				if hardles[ob].show() < -100:
					del hardles[ob]
						
		#draw objects in the sky
		
	
		#get key event, set state, and play SE
		for event in pygame.event.get():		
			if event.type == KEYDOWN:
				if event.key == K_SPACE:	
					state = 'jump'
					time = pygame.mixer.music.get_pos()/1000	#get bgm's play time
					#print(time)	#手動入力したtimeを出力
					fail.play()
				elif event.key == K_f or event.key == K_j:
					time = pygame.mixer.music.get_pos()/1000	#get bgm7s play time
					#print(time)	#手動入力したtimeを出力
					correct.play()
					if state == 'run1':
						state = 'run2'
					elif state == 'run2':
						state = 'run1'
					pygame.event.clear() 
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()
		
		#show judgement
		for j in range(J,len(TIMING))
			dist = abs(float(TIMING[j])-time)
			if dist < 0.05:
				judgement = "Perfect!"
				INPUT[j] = time
				J = j+1
				break
			elif dist >= 0.05 and dist < 0.08:
				judgement = "Good!"
				INPUT[j] = time
				J = j+1
				break
			elif dist >= 0.08 and dist <= 0.25:
				judgement = "Bad"
				INPUT[j] = time
				if state = 'jump':
					state = 'badjump':
				J = j+1
				break
			#調べているTIMINGと入力のtimeが遠すぎたら探索を続ける
				
				 	
		screen.blit(font.render(judgement, True, (0,0,0)), [240,220])

		#show characters
		if state == 'jump' or state == 'badjump':
			if state == 'badjump':
				DISPLAYSURF.blit(IMAGEDICT['bad'],(0,0-jumpy))
			else:	
				DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0-jumpy))
			jumpy = -14400*((jumpt-0.083)**2)+100
			jumpt += 0.02
			if jumpt >= 0.166:
				jumpt = 0
				jumpy = 0
				state = 'run1'
		elif state == 'run1' or state == 'run2' or state == 'bad':
			DISPLAYSURF.blit(IMAGEDICT[state],(0,0))
		else: print(error: state is not proper.)
			
		#左上テキストの表示
		#text = font.render(str(time), True, (0,0,0)) #テキストの設定
		#screen.blit(text, [0,0]) #テキストの表示
		
		#prepare for the next frame
		pygame.display.update()
		fpsClock.tick_busy_loop(FPS)

if __name__ == "__main__":
    main()
