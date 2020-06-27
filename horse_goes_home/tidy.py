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
	global IMAGEDICT,FPSCLOCK,TIMING,IS_HARDLE,CORRECT,JUMP,FAIL,MISS,screen,font,BASICFONT,RESULT
	#initialise
	pygame.mixer.quit()
	pygame.mixer.pre_init(buffer=64)
	pygame.init()

	FPSCLOCK = pygame.time.Clock()
	
	pygame.display.set_caption('tidy')
	sm = ScoreMaker()
	TIMING, IS_HARDLE = sm.make()
	
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

	pygame.mixer.music.load("se/horse.wav")
	CORRECT = pygame.mixer.Sound("se/correct.wav")
	CORRECT.set_volume(0.2)
	JUMP = pygame.mixer.Sound("se/Motion-pop15-1.wav")
	FAIL = pygame.mixer.Sound("se/fail.wav")
	MISS = pygame.mixer.Sound("se/match4.wav")
	MISS.set_volume(0.3)
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	font = pygame.font.Font(None, 30)
	BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
	while True:
		showStartScreen()
		RESULT = runGame()
		showEndEvent(RESULT)

def runGame():
	j = 0 #index for judge with TIMING
	s = 0 #index for set hardle pictures with TIMING
	INPUT = [0]*170	#input data from player
	JUDGE = ['']*170
	DIST = [0]*170
	cx = 0 #cloud's x
	hardles = []
	image = IMAGEDICT['stop']
	jump = dict(y = 0, t = 0, jumping = False)
	time = 0
	time0 = 0
	dist = 0.0
	judgement = ''
	score = 0.0

	pygame.mixer.music.play()	
	#setting Fonts

	#main game loop
	while True:
		DISPLAYSURF.blit(IMAGEDICT['back'],(0,0)) #draw background
			
		#draw hardles on the ground
		s, hardles = drawHardle(s,hardles)

		#draw objects in the sky
		cx = drawCloud(cx)
		time = pygame.mixer.music.get_pos()/1000	#get bgm's play time
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
		screen.blit(font.render(judgement, True, (0,0,0)), [240,220])
		#キャラクターを描画
		image,jump = drawCharacter(image,jump)
		
		#プレイ終了
		if pygame.mixer.music.get_pos()/1000 > 54.00:
			for result in zip(TIMING,INPUT,DIST,JUDGE):
				print(result)
			return JUDGE
		#prepare for the next frame
		pygame.display.update()
		FPSCLOCK.tick_busy_loop(FPS)

def terminate():
    pygame.quit()
    sys.exit()

def calculater(JUDGE):
	score = 0
	for str in JUDGE:
		if str == 'Perfect!':
			score += 3
		elif str == 'Good!':
			score += 3*0.7
		elif str == 'Bad':
			score += 3*0.1
		elif str == 'Miss':
			score += -3*0.1

	score = round((score/(len(JUDGE)*3))*100,3)
	return score

def showEndEvent(JUDGE):
	score = calculater(JUDGE)
	print(score)
	while True:
		screen.blit(font.render(str(score), True, (0,0,0)), [100,100])
		if checkForKeyPress():
			pygame.event.get() # clear event queue
			return
		pygame.display.update()
		FPSCLOCK.tick(FPS)

def showStartScreen():
    titleFont = pygame.font.Font('freesansbold.ttf', 100)
    titleSurf1 = titleFont.render('Tempo Jigoku', True, WHITE, DARKGREEN)
    titleSurf2 = titleFont.render('Tempo Jigoku', True, GREEN)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BGCOLOR)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WIDTH / 2, HEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WIDTH / 2, HEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def drawPressKeyMsg():
    pressKeySurf = BASICFONT.render('Press a key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WIDTH - 200, HEIGHT - 30)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

def missed(J,time,INPUT,JUDGE,DIST,image,judgement):
	if time-TIMING[J]>0.25:
		if INPUT[J]==0:
			judgement = "Miss"
			JUDGE[J] = judgement
			DIST[J] = None
			INPUT[J] = None
			image = IMAGEDICT['bad']
			MISS.play()
			J += 1
	return J,INPUT,JUDGE,DIST,image,judgement

def drawHardle(S,hardles):
	if IS_HARDLE[S]:
		time0 = pygame.mixer.music.get_pos()/1000 #get bgm's play time
		if TIMING[S]-time0<0.60: #ハードル設定した音符が流れる0.6秒前に準備する
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
	elif S + 1 < len(IS_HARDLE):
		S += 1
	if hardles: #空でなかったら
		for h in range(len(hardles)):
			#hardles内のオブジェクトのxをを進める
			DISPLAYSURF.blit(IMAGEDICT[hardles[h].pic],(hardles[h].move(),0))
		if hardles[0].x < -70:
			del hardles[0]
	return S,hardles


def drawCloud(cx):
	DISPLAYSURF.blit(IMAGEDICT['cloud'],(cx,0))
	cx -= 3
	if cx < -130:
		cx = 700
	return cx

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
		elif 0.05 <= dist < 0.07 and correctJump:
			judgement = "Good!"
			JUDGE[j] = judgement
			INPUT[j] = time
			DIST[j] = dist
			CORRECT.play()
			J = j+1
			break
		elif 0.07 <= dist <= 0.25 or not correctJump:
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
	JUMPRATE = 10
	JUMPHEIGHT = 100
	if jump['jumping']: #ジャンプしている
		jump['y'] = math.sin((math.pi / float(JUMPRATE)) * jump['t']) * JUMPHEIGHT
		jump['t'] += 1
		if jump['t'] >= JUMPRATE:
			jump['t'] = 0
			jump['y'] = 0
			jump['jumping'] = False
		if image == IMAGEDICT['bad']:
			DISPLAYSURF.blit(image,(0,0-jump['y']))
		else:
			DISPLAYSURF.blit(IMAGEDICT['run1'],(0,0-jump['y']))
	else:DISPLAYSURF.blit(image,(0,0)) #ジャンプしていない
	return image,jump
	


if __name__ == "__main__":
    main()