import pygame
from pygame.locals import *
import pandas as pd
import csv
import sys
import random
import time as tm
import math

WIDTH = 700
HEIGHT = 500
FPS = 30
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
BGCOLOR = BLACK
class Hardle:
	pic = ''
	x = WIDTH
	def __init__(self, pic,speed):
		self.pic = pic
		self.speed = speed
	def move(self):
		self.x -= self.speed
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

	#swing2は1の後ろにだけくるとする
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

	#swing3は2の後ろにだけくるとする
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
	global IMAGEDICT,FPSCLOCK,TIMING,IS_HARDLE,screen,font,BASICFONT
	#initialise
	pygame.mixer.quit()
	pygame.mixer.pre_init(buffer=64)
	pygame.init()

	FPSCLOCK = pygame.time.Clock()
	
	pygame.display.set_caption('HORSE GOES HOME')
	sm = ScoreMaker()
	TIMING, IS_HARDLE = sm.make()
	
	IMAGEDICT = {'field': pygame.image.load('pic/field.png'),
				'title': pygame.image.load('pic/title.png'),
				'back': pygame.image.load('pic/back.png'),
				'back2': pygame.image.load('pic/back2.png'),
				'stone': pygame.image.load('pic/stone.png'),
				'walkr': pygame.image.load('pic/walkright.png'),
				'walkl': pygame.image.load('pic/walkleft.png'),
				'stop': pygame.image.load('pic/stop.png'),
	    		'run1': pygame.image.load('pic/run1.png'),
	    		'run2': pygame.image.load('pic/run2.png'),
	    		'smile': pygame.image.load('pic/smile.png'),
	    		'red': pygame.image.load('pic/red.png'),
	    		'white': pygame.image.load('pic/white.png'),
	    		'yellow': pygame.image.load('pic/yellow.png'),
	    		'mole': pygame.image.load('pic/mole.png'),
	    		'bad': pygame.image.load('pic/fail.png'),
	    		'cloud': pygame.image.load('pic/cloud.png'),
	    		'bird': pygame.image.load('pic/bird.png'),
	    		'home': pygame.image.load('pic/house.png'),
	    		'howtoplay': pygame.image.load('pic/howtoplay.png'),
	    		'crun1R': pygame.transform.scale(pygame.image.load('pic/callotrun1.png'), (int(WIDTH*0.8), int(HEIGHT*0.8))),
	    		'crun2R': pygame.transform.scale(pygame.image.load('pic/callotrun2.png'), (int(WIDTH*0.8), int(HEIGHT*0.8)))
	    		}
	IMAGEDICT['crun1L'] = pygame.transform.flip(IMAGEDICT['crun1R'], True, False)
	IMAGEDICT['crun2L'] = pygame.transform.flip(IMAGEDICT['crun2R'], True, False)

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	font = pygame.font.Font(None, 30)
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	RESULT = []
	cx = 0
	while True:
		showStartScreen()
		RESULT,cx,cityx = runGame()
		showEndEvent(RESULT,cx,cityx)

def showStartScreen():
	CHOICE = pygame.mixer.Sound("se/Onmtp-Inspiration08-3.wav")
	CHOICE.set_volume(0.5)
	pygame.mixer.music.load("se/1840.wav")
	pygame.mixer.music.set_volume(0.2)
	pygame.mixer.music.play(loops=-1)
	titley = 0
	horsey = 0
	horsex = 0
	im = 'crun1R'
	speed = 5
	noise = 0
	Key = ''
	while True:
		DISPLAYSURF.blit(IMAGEDICT['field'],(0,0))
		DISPLAYSURF.blit(IMAGEDICT['title'],(0,titley-30))
		DISPLAYSURF.blit(IMAGEDICT[im],(horsex,horsey))

		drawPressKeyMsgS()
		Key = checkForKeyPress()
		if Key == 'howToPlay':
			howToPlay()
		elif Key == 'runGame':
			CHOICE.play()
			return
			
		pygame.display.update()
		FPSCLOCK.tick(FPS)
		titley = 7*math.sin(pygame.time.get_ticks()/600)
		horsey = 10*math.sin(pygame.time.get_ticks()/150)+noise
		horsex += speed

		if horsex % 60 == 0:
			if speed > 0:
				if im == 'crun1R':
					im = 'crun2R'
				else: im = 'crun1R'
			elif im == 'crun1L':
				im = 'crun2L'
			else: im = 'crun1L'
		if horsex < -500 or horsex > WIDTH-100:
			speed = -speed
			noise = random.randint(100,200)

def checkForKeyPress():
	for event in pygame.event.get(): # clear event queue 
		if event.type == KEYUP:
			if event.key == K_SPACE:
				return 'runGame'
			elif event.key == K_RETURN:
				return 'howToPlay'
			elif event.key == K_x:
				return 'x'
			elif event.key == K_ESCAPE:
				terminate()
		elif event.type == QUIT:
			terminate()
	return 

def drawPressKeyMsgS():
    pressSpaceSurf = BASICFONT.render('Press SPACE to play.', True, DARKGRAY)
    pressSpaceRect = pressSpaceSurf.get_rect()
    pressSpaceRect.topleft = (WIDTH - 200, HEIGHT - 30)
    DISPLAYSURF.blit(pressSpaceSurf, pressSpaceRect)

    pressEnterSurf = BASICFONT.render('Press ENTER to see how to play.', True, DARKGRAY)
    pressEnterRect = pressEnterSurf.get_rect()
    pressEnterRect.topleft = (20, HEIGHT - 30)
    DISPLAYSURF.blit(pressEnterSurf, pressEnterRect)

def drawPressKeyMsgE():
    pressKeySurf = BASICFONT.render('Press SPACE to go to the Title.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (20, HEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def howToPlay():
	im = 'run1'
	jump = dict(x = 350, y = 0, defY = 50, height = 3, t = 0, jumping = True)
	count = 0
	while True:
		count += 1
		if count % 20 == 0:
			im = 'run2'
			count = 0
			if jump['jumping'] == False:
				jump['jumping'] = True
		elif count % 10 == 0:
			im = 'run1'
			
		DISPLAYSURF.blit(IMAGEDICT['howtoplay'],(0,0))
		DISPLAYSURF.blit(IMAGEDICT[im],(-50,50))
		_, jump = drawCharacter(IMAGEDICT['run1'],jump)
		refreshFrame()

		if checkForKeyPress():
			pygame.event.get()
			return

def showEndEvent(RESULT,cx,cityx):
	im = 'walkr'
	image = IMAGEDICT[im]
	homex = WIDTH+200
	scorefont = pygame.font.Font(None, 90)
	score = list(map(calculate,RESULT))
	score = round((sum(score)/(len(score)*3))*100,3)
	drumtime = 0
	DRUMLEN = (DRUM.get_length()-3.000)*1000 # millisecond
	WALK = 15*14

	for i in range(WALK):
		if i % 15 == 0:
			if im == 'walkl':
				im = 'walkr'
			else: im = 'walkl'
		elif i == WALK-1:
			im = 'stop'
		cx -= 0.3
		cityx -= 0.3
		homex -= 2.4
		DISPLAYSURF.blit(IMAGEDICT['back'],(0,0))
		DISPLAYSURF.blit(IMAGEDICT['cloud'],(cx,0))
		DISPLAYSURF.blit(IMAGEDICT['back2'],(cityx,0))
		DISPLAYSURF.blit(IMAGEDICT['back2'],(cityx+WIDTH,0))
		DISPLAYSURF.blit(IMAGEDICT['home'],(homex,-10))
		DISPLAYSURF.blit(IMAGEDICT[im],(0,0))
		refreshFrame()
		if i == 15*6:
			DRUM.play()
			drumtime = pygame.time.get_ticks()

	score = 85.345
	while drumtime+DRUMLEN-pygame.time.get_ticks()>0:
		screen.blit(scorefont.render(str(score)+'%', True, (0,0,0)), [70,50])
		refreshFrame()
	
	if score >= 80:
		pygame.time.wait(1000)
		CLEAR.play()
		DISPLAYSURF.blit(IMAGEDICT['smile'],(0,0))
		refreshFrame()
		
	pygame.event.clear() # clear event queue
	drawPressKeyMsgE()
	while True:
		if checkForKeyPress():
			pygame.event.get() # clear event queue
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)


def runGame():
	global CORRECT,JUMP,FAIL,MISS,CLEAR,DRUM
	j = 0 			#index for judge with TIMING
	s = 0 			#index for set hardle pictures with TIMING
	INPUT = [0]*170	#input data from player
	JUDGE = ['']*170
	DIST = [0]*170
	cx = 500 #cloud's x
	cityx = 0 #city's x
	hardles = []
	image = IMAGEDICT['stop']
	jump = dict(x = 0, y = 0, defY = 0, height = 100, t = 0, jumping = False)
	time = 0
	time0 = 0
	dist = 0.0
	judgement = ''
	score = 0.0

	
	CORRECT = pygame.mixer.Sound("se/correct.wav")
	CORRECT.set_volume(0.1)
	JUMP = pygame.mixer.Sound("se/Motion-pop15-1.wav")
	FAIL = pygame.mixer.Sound("se/fail.wav")
	FAIL.set_volume(0.3)
	MISS = pygame.mixer.Sound("se/match4.wav")
	MISS.set_volume(0.2)
	DRUM = pygame.mixer.Sound("se/Quiz-Results01-2.wav")
	CLEAR = pygame.mixer.Sound("se/Shortbridge02-1.wav")
	pygame.mixer.music.load("se/horse.wav")

	pygame.mixer.music.set_volume(1.2)
	pygame.mixer.music.play()
	#main game loop
	while True:	
		time = pygame.mixer.music.get_pos()/1000	#get bgm's play time

		#draw background objects
		DISPLAYSURF.blit(IMAGEDICT['back'],(0,0)) #draw background
		DISPLAYSURF.blit(IMAGEDICT['cloud'],(cx,0))	
		DISPLAYSURF.blit(IMAGEDICT['back2'],(cityx,0))
		DISPLAYSURF.blit(IMAGEDICT['back2'],(cityx+WIDTH,0))
		if time > 4.0:	
			cx = moveCloud(cx)
			cityx = moveCity(cityx)
		
		#draw hardles on the ground
		s, hardles = drawHardle(s,hardles)
		
		#get key event, set image, play SE, and judge
		for event in pygame.event.get():					
			if event.type == KEYDOWN:	
				if event.key == K_SPACE:
					jump['jumping'] = True
					JUMP.play()
					#判定	
					j,INPUT,JUDGE,DIST,image,judgement = judge(j,time,INPUT,JUDGE,DIST,image,judgement,jump)
					if image == IMAGEDICT['bad'] and judgement != "Bad":
						image = IMAGEDICT['run1']
				elif event.key == K_f or event.key == K_j:
					if image == IMAGEDICT['stop'] or image == IMAGEDICT['run2'] or image == IMAGEDICT['bad']:
						image = IMAGEDICT['run1']
					elif image == IMAGEDICT['run1']:
						image = IMAGEDICT['run2']
					#判定
					j,INPUT,JUDGE,DIST,image,judgement = judge(j,time,INPUT,JUDGE,DIST,image,judgement,jump)							
				elif event.key == K_ESCAPE:
					terminate()
			elif event.type == QUIT:
				terminate()

		#音符を見逃したか判定
		if j < len(TIMING):
			j,INPUT,JUDGE,DIST,image,judgement = missed(j,time,INPUT,JUDGE,DIST,image,judgement)

		#判定結果を表示	
		screen.blit(font.render(judgement, True, (0,0,0)), [260,250])
		#キャラクターを描画
		image,jump = drawCharacter(image,jump)
		
		#prepare for the next frame
		pygame.display.update()
		FPSCLOCK.tick_busy_loop(FPS)

		#プレイ終了
		if time > 51.20:
			return JUDGE,cx,cityx

def terminate():
    pygame.quit()
    sys.exit()

def drawHardle(S,hardles):
	SPEED = 16
	mtime = pygame.mixer.music.get_pos()/1000 #get music's play time
	#make hardles ready before this time,from horse's leg to right edge is about 452 pixel
	if S<len(TIMING) and TIMING[S]-mtime<(452/(SPEED*FPS)): 
		if IS_HARDLE[S]:
			rand = random.randint(0,6)
			if rand/3 == 1:
				pic = 'red'
			elif rand/2 == 1:
				pic = 'white'
			elif rand == 0:
				pic = 'mole'
			else: pic = 'yellow'
		elif not IS_HARDLE[S]: 
			pic = 'stone'
		hardles.append(Hardle(pic,SPEED))
		S += 1
	if hardles: #空でなかったら
		for h in range(len(hardles)):
			#hardles内のオブジェクトのxをを進める
			DISPLAYSURF.blit(IMAGEDICT[hardles[h].pic],(hardles[h].move(),0))
		if hardles[0].x < -70:#ハードル画像の不透明部の幅が約70pixel
			del hardles[0]
	return S,hardles

def calculate(a_result):
	a_score = 0
	if a_result == 'Perfect!':
		a_score = 3
	elif a_result == 'Good!':
		a_score = 3*0.7
	elif a_result == 'Bad':
		a_score = 3*0.1
	elif a_result == 'Miss':
		a_score = -3*0.1
	return a_score


def refreshFrame():
	pygame.event.get() 
	pygame.display.update()
	FPSCLOCK.tick(FPS)

def moveCloud(cx):
	cx -= 0.5
	if cx < -130:
		cx = 700
	return cx

def moveCity(cityx):
	cityx -= 1
	if cityx < -WIDTH:
		cityx = 0
	return cityx

def missed(J,time,INPUT,JUDGE,DIST,image,judgement):
	if time-TIMING[J]>0.25:
		if INPUT[J]==0:
			judgement = "Miss"
			JUDGE[J] = judgement
			DIST[J] = None
			INPUT[J] = None
			image = IMAGEDICT['bad']
			#MISS.play()
			J += 1
	return J,INPUT,JUDGE,DIST,image,judgement

def judge(J,time,INPUT,JUDGE,DIST,image,judgement,jump):
	correctJump = True
	for j in range(J,len(TIMING)):
		dist = abs(TIMING[j]-time)
		if dist < 0.07:
			if IS_HARDLE[j] and not jump['jumping']:
				correctJump = False
			elif IS_HARDLE[j] and jump['jumping']:
				correctJump = True
			elif not IS_HARDLE[j] and jump['jumping']:
				correctJump = False
			elif not IS_HARDLE[j] and not jump['jumping']:
				correctJump = True

		if dist < 0.05 and correctJump:
			judgement = "Perfect!"
			JUDGE[j] = judgement
			INPUT[j] = time
			DIST[j] = dist
			CORRECT.play()
			J = j+1
			break
		elif 0.05 <= dist < 0.08 and correctJump:
			judgement = "Good!"
			JUDGE[j] = judgement
			INPUT[j] = time
			DIST[j] = dist
			CORRECT.play()
			J = j+1
			break
		elif 0.08 <= dist <= 0.25 or not correctJump:
			judgement = "Bad"
			JUDGE[j] = judgement
			DIST[j] = dist
			INPUT[j] = time
			image = IMAGEDICT['bad']
			FAIL.play()
			J = j+1
			break
		#調べているTIMINGと入力のtimeが遠すぎたら探索を続ける
		pygame.event.clear()
	return J,INPUT,JUDGE,DIST,image,judgement

def drawCharacter(image,jump):
	JUMPRATE = 8
	JUMPHEIGHT = jump['height']
	if jump['jumping']: #ジャンプしている
		jump['y'] = jump['defY']+math.sin((math.pi / float(JUMPRATE)) * jump['t']) * JUMPHEIGHT
		jump['t'] += 1
		if jump['t'] >= JUMPRATE:
			jump['t'] = 0
			jump['y'] = jump['defY']
			jump['jumping'] = False
		if image == IMAGEDICT['bad']:
			DISPLAYSURF.blit(image,(jump['x'],jump['defY']-jump['y']))
		else:
			DISPLAYSURF.blit(IMAGEDICT['run1'],(jump['x'],jump['defY']-jump['y']))
	else:DISPLAYSURF.blit(image,(jump['x'],jump['defY']))     #ジャンプしていない
	return image,jump

if __name__ == "__main__":
    main()