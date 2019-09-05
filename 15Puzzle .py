import random
import pygame
import time
#Can be changed according to user's choice:
ROWLEN=0
N=ROWLEN+1
#CONSTANTS
BLOCK=111
SPACE=9
WIDTH = BLOCK*9
HEIGHT = BLOCK*9
#max values for recrods (Smaller is better, so I chose very high numbers)
record3 = 2**14
record4 = 2**14
record5 = 2**14
#Creates board with ROWLEN*ROWLEN size:
board=[]
def create_board(ROWLEN):
	global N
	for i in range(N+1):
		board.append([])
	for i in range(N+1):
		board[0].append(0)
	cnt=1
	for i in range(1,N):
		board[i].append(0)
		for j in range(1,N):
			board[i].append(cnt)
			cnt+=1
		board[i].append(0)	
	for i in range(N+1):
		board[N].append(0)	
	board[ROWLEN][ROWLEN]="_"						
#prints the board
def print_board(board): 
	for row in range(1,N):
		lista=[]
		for col in range(1,N):
			lista.append(board[row][col])
		print lista				
#The function checks if the player finished to rearrange the board:				
def win(board):
	cnt=1
	flag=True
	for row in range(1,N):
		for col in range(1,N):
			if board[row][col]!=cnt and cnt<ROWLEN*ROWLEN:
				flag=False
			cnt+=1		
	return flag	

#The function checks if a given place is empty	
def empty(row,col,board):
	if board[row][col]=="_":
		return True
	return False
#finds the empty cell:
def findEmpty(board):
	for i in range(1,N):
		for j in range(1,N):
			if empty(i,j,board):
				emptRow=i
				emptCol=j
	return emptRow,emptCol			
		
#The function checks if the player pressed on a valid number:			
def valid(num,board):
	nums=[]
	for row in range(1,N):
		for col in range(1,N):
			if empty(row,col,board):
				if (num==board[row-1][col] or num==board[row+1][col] or \
				    num==board[row][col+1] or num==board[row][col-1]):
					if num!=0:
						return True
					else:
						return False
				else:
					return False
	return "Not Valid!"	
#The functions swaps the places of num and "_":	
def moveIt(num,row,col,board):
	board[row][col]=num
	if num==board[row-1][col]:
		board[row-1][col]="_"
	elif num==board[row+1][col]:
		board[row+1][col]="_"
	elif num==board[row][col+1]:
		board[row][col+1]="_"
	elif num==board[row][col-1]:
		board[row][col-1]="_"
	else:
		pass
		
#If the move is valid, moves the square to empty place:							
def move(num,board):
	flag=False
	if valid(num,board):
		for row in range(1,N):
			for col in range(1,N):
				if empty(row,col,board):
					flag=True
					moveIt(num,row,col,board) 
					break
				if flag:
					break	
			if flag:
				break									
	else:
		print num," Is not valid!"
#The function creates list of the possible moves at a given board:	
def validNums(board):
	nums=[]
	for i in range(1,ROWLEN*ROWLEN+1):
		if valid(i,board):
			nums.append(i)
	return nums	
#returns list of the possible directions that the empty cell can move to	
def directions(board):
	dire=[]
	emptRow,emptCol=findEmpty(board)
	nums=validNums(board)	
	for num in nums:
		if board[emptRow][emptCol-1]==num:
			dire.append(1)
		elif board[emptRow][emptCol+1]==num:
			dire.append(3)
		elif board[emptRow+1][emptCol]==num:		
			dire.append(2)
		elif board[emptRow-1][emptCol]==num:	
			dire.append(4)
	return dire	
#Refreshes the screen:	
def refresh():
	pygame.display.flip()		
#draws the board (graphiclly):
def drawBoard(board):
	countRow=0
	for row in board:
		countCol=0
		if countRow>0 and countRow<N:
			for col in row:
				if countCol>0 and countCol<N:
					if board[countCol][countRow]=="_":
						screen.blit(emptyCell,(BLOCK*countRow,BLOCK*countCol))						
					else:
						imag=nameToImage[board[countCol][countRow]]
						screen.blit(imag,(BLOCK*countRow,BLOCK*countCol))
						refresh()
				countCol+=1	
		countRow+=1		
#The function randomise the board:	
def random_board(level,board):
	num=0
	for i in range(level):
		nums=validNums(board)
		if num!=0:
			nums.remove(num)
		direct=random.randint(0,len(nums)-1)
		num=nums[direct]
		move(nums[direct],board)
		drawBoard(board)
		time.sleep(0.000001)
#The functions gets wanted level and randomise the board accordingly:
def level(level):
	random_board(level,board)
#Checks if the move from keyboard is valid and then move it:
def key_move(key, board):
	dire=directions(board)
	emptRow,emptCol = findEmpty(board)
	if key in dire:
		if key==1:
			move(board[emptRow][emptCol-1],board)
		elif key==2:
			move(board[emptRow+1][emptCol],board)
		elif key==3:
			move(board[emptRow][emptCol+1],board)
		elif key==4:
			move(board[emptRow-1][emptCol],board)
#Writes text to the screen:
def write(s,x,y):
	pygame.font.init()		
	myfont = pygame.font.SysFont('Comic Sans MS', 37)
	textsurface = myfont.render(s , True, (0,0,0))
	screen.blit(textsurface,(x,y))	
#Shows the images of the opening screen in the needed places
def openImages():
	for i in range(3,5):
		ima=nameToImage[i]
		screen.blit(ima,((3*i-SPACE)*(BLOCK+SPACE),BLOCK))
		screen.blit(multy, ((3*i-SPACE)*(BLOCK+SPACE)+BLOCK, BLOCK))
		screen.blit(ima,((3*i-SPACE)*(BLOCK+SPACE)+BLOCK*2, BLOCK))
	ima=nameToImage[5]
	screen.blit(ima,(0,2*BLOCK+SPACE))
	screen.blit(multy, (BLOCK, 2*BLOCK+SPACE))
	screen.blit(ima,(BLOCK*2, 2*BLOCK+SPACE))
#Creates a screen in which the level can be choosed:	
def levelScale():
	screen.blit(confirm,(BLOCK,BLOCK))
	screen.blit(scale, (BLOCK, BLOCK*3))
	screen.blit(scaleBut, (BLOCK, (BLOCK+SPACE)*3+1))
	refresh()
	global finish
	finish = False
	drag = False
	currentx = BLOCK
	x=BLOCK
	y=BLOCK*3
	while not finish:
		global currentx
		wrtLevel(x,y,currentx)
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				exit()
			if event.type==pygame.MOUSEBUTTONDOWN:
				drag = True
				x,y = pygame.mouse.get_pos()
				movingScale(x,y,currentx)

#Writes the current level to the screen while choosing:
def wrtLevel(x,y,currentx):
	screen.blit(blueCover, (BLOCK*3+2*SPACE+1, BLOCK*5))
	if rightPress(x,y, BLOCK,BLOCK*8,BLOCK*3, BLOCK*4):
		if x>BLOCK*5+SPACE*2:
			write("Current level: IMPOSSIBLE", BLOCK, BLOCK*5)
		else:
			write("Current level: "+str(x-BLOCK+1), BLOCK, BLOCK*5)
	else:
		write("Current level: "+str(currentx-BLOCK+1), BLOCK, BLOCK*5)			
	refresh()
									
#Creates the scale for level screen:
def movingScale(x,y,cur):
	global finish
	global currentx
	if rightPress(x,y,BLOCK,4*BLOCK, BLOCK, 2*BLOCK):
		clear()
		if cur>4*BLOCK+6*SPACE:
			impossible(ROWLEN)
		else:
			create_board(ROWLEN)
			level(cur-BLOCK+1)
		finish = True
	elif rightPress(x,y, BLOCK,BLOCK*7,BLOCK*3, BLOCK*4):
		screen.blit(cover, (cur, (BLOCK+SPACE)*3+1))
		screen.blit(scaleBut, (x, (BLOCK+SPACE)*3+1))
		currentx = x
		refresh()							
				
	
	
#Transforms pressed key into movement:
def keyDown(key):
	if key == 274:
		key_move(2,board)
	elif key == 273:
		key_move(4,board)
	elif key == 275:
		key_move(3,board)
	elif key == 276:
		key_move(1,board)
		
#Checks if mousePress is in a given area		
def rightPress(posx,posy,x1,x2,y1,y2):
	if posx>=x1 and posx<=x2 and posy>=y1 and posy<=y2:
		return True
	else:
		return False	
			
#Moves the board according to mouse press		
def mousePlay(posx,posy):
	posx=posx/BLOCK*BLOCK
	posy=posy/BLOCK*BLOCK
	if rightPress(posx,posy, 0,N*BLOCK,0, N*BLOCK):
		move(board[posy/BLOCK][posx/BLOCK],board)
		
#Checks mouse positions in the opening screen:
def mouseOpen(posx,posy):
	global finish
	global ROWLEN
	global N
	if rightPress(posx,posy,BLOCK*0,BLOCK*3,BLOCK,BLOCK*2) or\
	rightPress(posx,posy,(BLOCK+SPACE)*3,BLOCK*6+SPACE*3,BLOCK,BLOCK*2) or\
	rightPress(posx,posy,BLOCK*0,BLOCK*3,BLOCK*2+SPACE,BLOCK*3+SPACE):
		if rightPress(posx,posy,BLOCK*0,BLOCK*3,BLOCK,BLOCK*2):
			ROWLEN=3
			finish = True
		elif rightPress(posx,posy,(BLOCK+SPACE)*3,BLOCK*6+SPACE*3,BLOCK,BLOCK*2):
			clear()
			print 2
			ROWLEN=4
			finish = True
		elif rightPress(posx,posy,BLOCK*0,BLOCK*3,BLOCK*2+SPACE,BLOCK*3+SPACE):
			clear()
			print 3
			ROWLEN=5
			finish = True
		clear()	
		N=ROWLEN+1	
		levelScale()

		
			
#Creates unsolvable board:			
def impossible(size):
	create_board(size)
	board[size][size-1]=size*size-2
	board[size][size-2]=size*size-1
	drawBoard(board)
		
#Win graphics:
def winGr():
		screen.blit(img,(0,0))
		write("Number of moves: ",BLOCK,0)
		write(str(cnt),BLOCK,SPACE*4)
		screen.blit(wellDone,(BLOCK,BLOCK))
			
#Creates dictionary between numbers and image names and 
def dicImages(nameToImage):
	for i in range(1,25):
		ima="image"+str(i)
		png=str(i)+".png"
		ima = pygame.image.load(png).convert()
		nameToImage[i]=ima			
#Clears everthing from the board, keeps the background:
def clear():
	screen.blit(img,(0,0))
	refresh()
#Opening screen	
def opening():
	clear()
	openImages()
	write("Choose board size please", 111,0)
	refresh()
	finish = False
	while not finish:
		global ROWLEN
		global finish
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				posx,posy = pygame.mouse.get_pos()
				mouseOpen(posx,posy)

						
#Checks if reset is pressed and resests everything:				
def reset(posx,posy):
	global cnt
	global board
	if rightPress(posx,posy,6*BLOCK,7*BLOCK,BLOCK,2*BLOCK):
		cnt = 0
		board=[]
		opening()

def records():
	if record3>0 and record3<2**14:
		write("Record 3X3: ", BLOCK*6+SPACE, BLOCK*2)		
		write(str(record3), BLOCK*6+SPACE, BLOCK*2+4*SPACE)
	else:
		write("Record 3*3:", BLOCK*6+SPACE, BLOCK*2)
		write("No tries yet", BLOCK*6+SPACE, BLOCK*2+4*SPACE)
	if record4>0 and record4<2**14:
		write("Record 4X4:", BLOCK*6+SPACE, BLOCK*3)		
		write(str(record4), BLOCK*6+SPACE, BLOCK*3+4*SPACE)
	else:
		write("Record 4*4:", BLOCK*6+SPACE, BLOCK*3)
		write("No tries yet", BLOCK*6+SPACE, BLOCK*3+4*SPACE)
	if record5>0 and record5<2**14:
		write("Record 5X5:", BLOCK*6+SPACE, BLOCK*4)		
		write(str(record5), BLOCK*6+SPACE, BLOCK*4+4*SPACE)
	else:
		write("Record 5*5:", BLOCK*6+SPACE, BLOCK*4)
		write("No tries yet", BLOCK*6+SPACE, BLOCK*4+4*SPACE)

def newRecord(record,size):
	global record3, record4, record5
	if size==3:
		record3 = min(record3, record)
	elif size==4:
		record4 = min(record4, record)
	else:
		record5 = min(record5, record)		
		
#Record grapics + sets new records
def recGr():
	global cnt
	rec3 = record3
	rec4 = record4
	rec5 = record5
	newRecord(cnt, ROWLEN)
	winGr()	
	if rec3!=record3 or rec4!=record4 or rec5!=record5:
		screen.blit(record, (BLOCK*2, BLOCK*2+SPACE))
		write("In board " + str(ROWLEN) + "X" + str(ROWLEN), BLOCK*4+SPACE, BLOCK*2+SPACE)
		
#The game play itself, after choosing size and level:						
def game():
	global cnt
	global finish
	winn=False
	posx=0
	posy=0
	cnt  = 0
	finish = False
	while not finish:
		records()
		screen.blit(res,(BLOCK*6,BLOCK))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				cnt += 1
				x,y = pygame.mouse.get_pos()
				reset(x,y)
				mousePlay(x,y)
				clear()
				drawBoard(board)
			elif event.type == pygame.KEYDOWN:	
				key = event.key
				keyDown(key)
				drawBoard(board)
				cnt += 1	
		write("Number of moves: ",BLOCK,0)
		screen.blit(blueCover, (BLOCK, SPACE*5))
		write(str(cnt),BLOCK,SPACE*4)		
		if winn:
			time.sleep(3)
			winn=False
			reset(BLOCK*6,BLOCK)
			finish = True
		if win(board):
			recGr()
			cnt = 0
			winn=True
			
		clock.tick(REFRESH_RATE)
		refresh()
			
#MAIN:
#####
pygame.init()
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("15 Puzzle!")
record = pygame.image.load("record.png")
emptyCell = pygame.image.load('emptyCell.png')
wellDone = pygame.image.load('wellDone.png')
multy = pygame.image.load('multy.png')
imposs = pygame.image.load('impossible.png')
img = pygame.image.load('gameBoard.png')
res = pygame.image.load('reset.png')
confirm = pygame.image.load('confirm.png')
scale = pygame.image.load('Scale.png')
scaleBut = pygame.image.load('scaleButton.png')
cover = pygame.image.load('cover.png')
blueCover = pygame.image.load('blueCover.png')
clock = pygame.time.Clock()
REFRESH_RATE = 60
nameToImage={}
dicImages(nameToImage)
opening()
while True:
	game()	
	
