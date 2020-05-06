class ScoreMaker:
	notes = [] #音符リスト
	is_hardle = [] #ハードルかどうかのリスト
	init = 4.00 #音源の最初からの経過時間

	#n 繰り返し数
	#p 直前のパターン1,2,3
	def swing1(self,n,p):
		if p == 1:	#最初
			t = self.init
			self.is_hardle.append(False)
		elif p == 2:
			t = self.notes[-5]+2.0
			self.is_hardle.append(False)
		elif p == 3:
			t = self.notes[-1]+0.5
			self.is_hardle.append(False)

		for j in range(n):
			self.notes.append(t)
			self.notes.append(t+0.333)
			t += 0.5
			self.is_hardle.append(False)

	#swing2は1の後ろにだけくる
	def swing2(self,n,p):
		t = self.notes[-2]		
		for j in range(n):
			t += 0.5
			self.notes.append(t)
			self.is_hardle.append(True)
			self.notes.append(t+0.333)
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
		#全てaの配列を作成する
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

sm = ScoreMaker()
sm.make()
