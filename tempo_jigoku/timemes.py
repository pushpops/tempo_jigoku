a = [] #リスト
#n 繰り返し数
#b 直前のパターン1,2,3

def swing1(a,n,b):
	if b == 1:	#最初
		i = 0.0
	elif b == 2:
		i = a[-5]+2.0
	elif b == 3:
		i = a[-1]+0.5

	for j in range(n):
		a.append(i)
		a.append(i+0.333)
		i += 0.5
	return a

#swing2は1の後ろにだけくる
def swing2(a,n,b):
	i = a[-2]
	
	for j in range(n):
		i += 0.5
		a.append(i)
		a.append(i+0.333)
		for k in range(3):
			i += 0.5
			a.append(i+0.333)
		
	return a 

#swing3は2の後ろにだけくる
def swing3(a,n,b):
	i = a[-5]+1.5
	for j in range(n):
		for k in range(4):
			i += 0.5
			a.append(i)

def main():
	swing1(a,36,1)
	swing2(a,1,1)
	swing1(a,12,2)
	swing2(a,1,1)
	swing1(a,8,2)
	swing2(a,2,1)
	swing1(a,8,2)
	swing2(a,1,1)
	swing3(a,1,2)#第3引数に意味はないが書式合わせ
	swing1(a,6,3)
	a.append(47.0)
	print(a)

if __name__ == '__main__':
	main()