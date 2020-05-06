import pygame
from pygame.locals import *
import pandas as pd
import csv
import sys
import random

class Hardle:
	pic = ''
	x = 700
	def __init__(self, pic):
		self.pic = pic
	def move(self):
		self.x -= 24
		return self.x

class ScoreMaker:
	notes = [] #音符リスト
	is_hardle = [] #ハードルかどうかのリスト
	init = 4.00 #音源の最初からの経過時間

	#n 繰り返し数
	#p 直前のパターン1,2,3
	def swing1(self,n,p):
		if p == 1:	#最初
			t = self.init
		elif p == 2:
			t = self.notes[-5]+2.0
		elif p == 3:
			t = self.notes[-1]+0.5
		for j in range(n):
			self.notes.append(t)
			self.is_hardle.append(False)
			self.notes.append(t+0.333)
			t += 0.5
			self.is_hardle.append(False)

	#swing2は1の後ろにだけくる
	def swing2(self,n,p):
		t = self.notes[-2]		
		for j in range(n):
			t += 0.5
			self.notes.append(t)
			self.is_hardle.append(False)
			self.notes.append(t+0.333)
			self.is_hardle.append(True)
			for k in range(3):
				t += 0.5
				self.notes.append(t+0.333) 
				self.is_hardle.append(True)

	#swing3は2の後ろにだけくる
	def swing3(self,n,p):
		t = self.notes[-5]+1.5
		for j in range(n):
			for k in range(4):
				t += 0.5
				self.notes.append(t)
				self.is_hardle.append(True)

	def make(self):
		#全てswing1パターンの配列を作成
		#swing1(notes,21*4+3,1)

		#ゲームに使う配列を作成する
		self.swing1(36,1)
		self.swing2(1,1)
		self.swing1(12,2)
		self.swing2(1,1)
		self.swing1(8,2)
		self.swing2(2,1)
		self.swing1(8,2)
		self.swing2(1,1)
		self.swing3(1,2) #第3引数に意味はないが書式合わせ
		self.swing1(6,3)
		self.notes.append(47.0+self.init)
		self.is_hardle.append(False)
		#print(self.notes)

		return self.notes, self.is_hardle

def main():
	WIDTH = 700
	HEIGHT = 500
	FPS = 30
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
	INPUT = [0]*170	#input data from player
	JUDGE = ['']*170
	DIST = [0]*170
	sm = ScoreMaker()
	cx = 0 #cloud's x
	TIMING, IS_HARDLE = sm.make()
	
	hardles = []
	state = 'run1'
	jumpy = 0
	jumpt = 0
	time = 0
	time0 = 0
	pic = ''
	dist = 0.0
	judgement = ''
	
	#initialise
	pygame.mixer.quit()
	pygame.mixer.pre_init(buffer=64)
	pygame.init()

	#load SE
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.mixer.music.load("se/horse.wav")
	correct = pygame.mixer.Sound("se/correct.wav")
	correct.set_volume(0.2)
	jump = pygame.mixer.Sound("se/Motion-pop15-1.wav")
	fail = pygame.mixer.Sound("se/fail.wav")
	pygame.mixer.music.play()
	
	#setting Fonts
	font = pygame.font.Font(None, 30)

	#main game loop
	while True:
		DISPLAYSURF.blit(IMAGEDICT['back'],(0,0)) #draw background
		
		#draw hardles on the ground
		if IS_HARDLE[S]:
			time0 = pygame.mixer.music.get_pos()/1000 #get bgm's play time
			if TIMING[S]-time0<0.66:
				rand = random.randint(0,4)
				if rand == 0 or rand == 4:
					pic = 'red'
				elif rand == 1:
					pic = 'white'
				elif rand == 2:
					pic = 'yellow'
				elif rand == 3:
					pic = 'mole'
				else: print("error: hardle was'nt chosen properly")
				hardles.append(Hardle(pic))
				S += 1
		elif S+1 < len(IS_HARDLE):
			S += 1
		if hardles: #空でなかったら
			for h in range(len(hardles)):
				#hardles内のオブジェクトのxをを進める
				DISPLAYSURF.blit(IMAGEDICT[hardles[h].pic],(hardles[h].move(),0))
			if hardles[0].x < -70:
				del hardles[0]
						
		#draw objects in the sky
		DISPLAYSURF.blit(IMAGEDICT['cloud'],(cx,0))
		cx -= 3
		if cx < -130:
			cx = 700
		#get key event, set state, play SE, and judge
		for event in pygame.event.get():		
			if event.type == KEYDOWN:
				time = pygame.mixer.music.get_pos()/1000	#get bgm's play time
				if event.key == K_SPACE:	
					state = 'jump'
					jump.play()
				elif event.key == K_f or event.key == K_j:
					correct.play()
					if state == 'run1':
						state = 'run2'
					elif state == 'run2' or state == 'stop':
						state = 'run1'
					pygame.event.clear()
				
				#show judgement
				for j in range(J,len(TIMING)):
					dist = abs(TIMING[j]-time)
					if dist < 0.05:
						judgement = "Perfect!"
						JUDGE[j] = judgement
						INPUT[j] = time
						DIST[j] = dist
						if state == 'run1':
							state == 'run2'
						else: state = 'run1'
						J = j+1
						break
					elif dist >= 0.05 and dist < 0.08:
						judgement = "Good!"
						JUDGE[j] = judgement
						INPUT[j] = time
						DIST[j] = dist
						if state == 'run1':
							state == 'run2'
						else: state = 'run1'
						J = j+1
						break
					elif dist >= 0.08 and dist <= 0.25:
						judgement = "Bad"
						JUDGE[j] = judgement
						DIST[j] = dist
						INPUT[j] = time
						if state == 'jump':
							state = 'badjump'
						else: state = 'bad'
						fail.play()
						J = j+1
						break
					#調べているTIMINGと入力のtimeが遠すぎたら探索を続ける	
			elif event.type == QUIT:
				pygame.quit()
				sys.exit()
		#判定結果を表示		
		screen.blit(font.render(judgement, True, (0,0,0)), [240,220])
			#print(state)
		'''
		#show judgement
		for j in range(J,len(TIMING)):
			dist = abs(TIMING[j]-time)
			if dist < 0.05:
				judgement = "Perfect!"
				JUDGE[j] = judgement
				INPUT[j] = time
				DIST[j] = dist
				if state == 'run1':
					state == 'run2'
				else: state = 'run1'
				J = j+1
				break
			elif dist >= 0.05 and dist < 0.08:
				judgement = "Good!"
				JUDGE[j] = judgement
				INPUT[j] = time
				DIST[j] = dist
				if state == 'run1':
					state == 'run2'
				else: state = 'run1'
				J = j+1
				break
			elif dist >= 0.08 and dist <= 0.25:
				judgement = "Bad"
				JUDGE[j] = judgement
				DIST[j] = dist
				INPUT[j] = time
				if state == 'jump':
					state = 'badjump'
				else: state = 'bad'
				fail.play()
				J = j+1
				break
			#調べているTIMINGと入力のtimeが遠すぎたら探索を続ける			
				 	
		screen.blit(font.render(judgement, True, (0,0,0)), [240,220])
		'''
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
		elif state == 'run1' or state == 'run2' or state == 'bad' or state == 'stop':
			DISPLAYSURF.blit(IMAGEDICT[state],(0,0))
		else: print("error: state is not proper.")
			
		#左上テキストの表示
		text = font.render(str(time), True, (0,0,0)) #テキストの設定
		screen.blit(text, [0,0]) #テキストの表示
		
		if pygame.mixer.music.get_pos()/1000 > 54.00:
			break
		#prepare for the next frame
		pygame.display.update()
		fpsClock.tick_busy_loop(FPS)
	'''
	pd.set_option('display.max_rows', 200)
	df = pd.DataFrame({
				 	   'timing': TIMING,
				 	   'input': INPUT,
				 	   'distance': DIST,
			 	   		'judge': JUDGE,
			 	   		'is_hardles': IS_HARDLE
			 	   		})
	print(df)
	'''
if __name__ == "__main__":
    main()
