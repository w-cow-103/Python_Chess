# By submitting this assignment, I agree to the following:
# “Aggies do not lie, cheat, or steal, or tolerate those who do”
# “I have not given or received any unauthorized aid on this assignment”
#
# Name: Will Cowden, Brandon Valdez, Zach Barnhart, Justin Leidelmeyer
# Section: 102-508
# Assignment: Project
# Date: 27 November 2018

#To-Do
    #Fix Bishop being able to hop pieces
    #Fix queen being able to hop pieces
    #Fix the backspace mechanic
    #Castling
    #Detect Check
    #Ends if CheckMate or if King is Killed

import pygame, sys, random, time
from math import*
all = []

pygame.init()
screen = pygame.display.set_mode((800,800))
myfont = pygame.font.SysFont('freesansbold.ttf', 110)

#prints out the current chessboard
def endGame(team):
    if (team == 0):
        for x in range (20):
            print("White Team Wins!!!!!!!!!!")
    else:
        for x in range (20):
            print("Black Team Wins!!!!!!!!!!")
    sys.exit(0)

def boardprint(board):
    row = 8
    print('\n')
    for x in board:
        for y in x:
            print(y, end="")
        print(" ",row)
        row-=1
    print("\nABCDEFGH")

def drawBoard(screenobject):
    pygame.draw.rect(screen, (153, 0, 0), (0, 0, 800, 800))
    pygame.draw.rect(screen, (153, 76, 0), (30, 30, 740, 740))
    pygame.draw.rect(screen, (255, 128, 0), (40, 40, 720, 720))
    for x in range(8):
        for y in range(8):
            tempX = x*90 + 40
            tempY = y*90 + 40
            if (x+y)%2==0:
                pygame.draw.rect(screen, (204, 204, 0), (tempX,tempY, 90, 90))

def drawPawn(screenobject, color1,x,y):
    if color1 == 1:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    textsurface = myfont.render('P', False, color)
    screen.blit(textsurface, (x+20, y+15))
    #pygame.draw.rect(screen, color, (x+20, y+20, 50, 50))

def drawBishop(screenobject,color1,x,y):
    if color1 == 1:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    textsurface = myfont.render('B', False, color)
    screen.blit(textsurface, (x+20, y+15))

def drawRook(screenobject,color1,x,y):
    if color1 == 1:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    textsurface = myfont.render('R', False, color)
    screen.blit(textsurface, (x+20, y+15))

def drawKing(screenobject,color1,x,y):
    if color1 == 1:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    textsurface = myfont.render('K', False, color)
    screen.blit(textsurface, (x+20, y+15))

def drawQueen(screenobject,color1,x,y):
    if color1 == 1:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    textsurface = myfont.render('Q', False, color)
    screen.blit(textsurface, (x+20, y+15))

def drawKnight(screenobject,color1,x,y):
    if color1 == 1:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    textsurface = myfont.render('N', False, color)
    screen.blit(textsurface, (x+20, y+15))

def drawCursor(screenobkect,x,y):
    color = (204,229,255)
    s = pygame.Surface((70,70))
    s.set_alpha(200)
    s.fill((255,255,255))
    screen.blit(s,(x*90+50,y*90+50))

def setCursor(screenobject,x,y,val):
    color = (204,255,204)
    s = pygame.Surface((70,70))
    s.set_alpha(val)
    s.fill((255,255,255))
    screen.blit(s,(x*90+50,y*90+50))

def canKill(team,board,x,y):
    piece = board[y][x]
    if (piece == "."):
        return False
    if (piece.isupper() and team == 1):
        return True
    if (not piece.isupper() and team == 0):
            return True
    return False

def checkRook(board,newX,newY,oldX,oldY):
    if (newX == oldX):
        print("vert")
        mx = max(newY,oldY)
        mn = min(newY,oldY)
        for y in range(mn+1,mx):
            print(board[y][newX]," ",y)
            if board[y][newX] != '.':
                return False
        return True

    elif (oldY == newY):
        print("Horz")
        mx = max(newX, oldX)
        mn = min(newX, oldX)
        for x in range(mn + 1, mx):
            print(board[newY][x]," ",x)
            if board[newY][x] != '.':
                return False
        return True
    else:
        return False



def checkBishop(board,newX,newY,oldX,oldY):
    if (abs(oldX-newX) != abs(oldY-newY)):
        print("No Diag")
        return False
    mnX = min(newX,oldX)
    mxX = max(newX,oldX)
    mnY = min(newY,oldY)
    mxY = max(newY,oldY)
    for x,y in zip(range(mnX+1,mxX),range(mnY+1,mxY)):
        print(board[y][x])
        if (board[y][x] != "."):
            return False
    return True

def checkMove(board,newX,newY,oldX,oldY,turn):
    piece = board[oldY][oldX]
    if (turn):
        if (piece.isupper()):
            return False
    else:
        if (piece.islower()):
            return False
    newP = board[newY][newX]
    if (newP != '.'):
        if (piece.isupper() and newP.isupper()):
            return False
        if not((piece.isupper() or newP.isupper())):
            return False
    Piece = piece.upper()
    #print(Piece)
    #Pawn
    if (Piece == "P"):
        #print(6)
        #print("one up:",board[newY + 1][newX])
        if (piece == "p" and oldY == 6 and newY==4):
            #print(7)
            if newY==4 and board[newY][newX] == '.' and board[newY+1][newX] == '.' and newX==oldX:
                print("White Pawn Up 2")
                return True
        elif (piece == "P" and oldY == 1 and newY == 3):
            #print(8)
            if newY==3 and board[newY][newX] == '.' and board[newY-1][newX] == '.' and newX==oldX:
                print("Black Pawn down 2")
                return True
        elif (piece == "p" and board[newY][newX] == '.' and (oldY-newY)==1 and newX==oldX):
            print("White Pawn Up 1")
            return True
        elif (piece == "P" and board[newY][newX] == '.' and (newY-oldY)==1 and newX==oldX):
            print("Black pawn down 1")
            return True
        elif (piece == "p" and canKill(1,board,newX,newY) and abs(newX-oldX)==1 and (oldY-newY)==1):
            print("White Pawn kill")
            return True
        elif (piece == "P" and canKill(0,board,newX,newY) and abs(newX-oldX)==1 and (oldY-newY)==-1):
            print("Black Pawn kill")
            return True

    elif (Piece == "N"):
        if ((abs(oldY-newY)==2 and abs(newX-oldX)==1) or (abs(oldY-newY)==1 and abs(newX-oldX)==2)):
            return True

    elif (Piece == "K"):
        if (abs(oldY-newY)<=1 and abs(oldX-newX)<=1):
            return True

    elif (Piece == "R"):
        if (checkRook(board,newX,newY,oldX,oldY)):
            return True

    elif (Piece == "B"):
        if (checkBishop(board,newX,newY,oldX,oldY)):
            return True

    elif (Piece == "Q"):
        if (checkBishop(board,newX,newY,oldX,oldY) or (checkRook(board,newX,newY,oldX,oldY))):
            return True

    else:
        return False

def movePiece(board,newX,newY,oldX,oldY):
    if (board[newY][newX] == "K"):
        endGame(0)
    if (board[newY][newX] == "k"):
        endGame(1)
    board[newY][newX] = board[oldY][oldX]
    board[oldY][oldX] = '.'










#Sets up the chess board
board = [ ['.'] * 8 for i in range(8)]

board[0] = "R N B Q K B N R".split(" ")
board[1] = "P P P P P P P P".split(" ")

board[6] = "p p p p p p p p".split(" ")
board[7] = "r n b q k b n r".split(" ")
board2 = board
#boardprint(board)
all.append(board)
#Gets info from players and moves piece to desired locaton\
'''
while (True):
    print("\tUse the A-H,1-8 for the location of the pieces")
    print('\ttype "end" if you want to exit program')
    col = str(input("What is the column of piece you want to move? Ex.A-H : "))
    if (col.capitalize() == "End"):
        break
    row = int(input("What is the row of the piece you want to move? Ex.1-8 :"))
    colNum = ord(col.capitalize()) -65
    colNum = colNum
    row = 8 - row
    print("\n")
    #Checks to see if a piece is at location
    if (board[row][colNum] == '.'):
        print("Invalid move!!! No piece exists at that location")
        break

    col2 = str(input("What is the column of the location you want to move to? Ex.A-H : "))
    row2 = int(input("What is the row of the location you want to move to? Ex.1-8 :"))
    colNum2 = (ord(col2.capitalize()) -65)
    row2 = 8 - row2

    temp = board[row][colNum]
    board[row][colNum] = '.'
    board[row2][colNum2] = temp

    boardprint(board)
'''
print("How many players? 1 or 2")
player = int(input())
posX = 0
posY = 0
setX = 0
setY = 0
newX = 0
newY = 0
#False means White, True means Black
turn = True
reset = False
pieceSet = False
# Actual Run
while True:
    drawBoard(screen)
    for r in range(8):
        for c in range(8):
            if (board[r][c] == '.'):
                continue;
            if (board[r][c] == 'p'):
                drawPawn(screen,0,c*90+40,r*90+40)
            if (board[r][c] == 'P'):
                drawPawn(screen,1,c*90+40,r*90+40)
            if (board[r][c] == 'r'):
                drawRook(screen,0,c*90+40,r*90+40)
            if (board[r][c] == 'R'):
                drawRook(screen,1,c*90+40,r*90+40)
            if (board[r][c] == 'n'):
                drawKnight(screen,0,c*90+40,r*90+40)
            if (board[r][c] == 'N'):
                drawKnight(screen,1,c*90+40,r*90+40)
            if (board[r][c] == 'b'):
                drawBishop(screen,0,c*90+40,r*90+40)
            if (board[r][c] == 'B'):
                drawBishop(screen,1,c*90+40,r*90+40)
            if (board[r][c] == 'k'):
                drawKing(screen,0,c*90+40,r*90+40)
            if (board[r][c] == 'K'):
                drawKing(screen,1,c*90+40,r*90+40)
            if (board[r][c] == 'q'):
                drawQueen(screen,0,c*90+40,r*90+40)
            if (board[r][c] == 'Q'):
                drawQueen(screen,1,c*90+40,r*90+40)
    drawCursor(screen,posX,posY)
    if pieceSet == True:
        setCursor(screen,setX,setY,200)

    #events = pygame.event.get()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_UP:
                print("Up arrow pressed")
                if (posY != 0):
                    posY-=1

            elif event.key == pygame.K_DOWN:
                print("Down arrow pressed")
                if (posY!=7):
                    posY+=1

            elif event.key == pygame.K_LEFT:
                print("Left arrow pressed")
                if (posX != 0):
                    posX-=1

            elif event.key == pygame.K_RIGHT:
                print("Right arrow pressed")
                if (posX != 7):
                    posX+=1

            elif event.key == pygame.K_BACKSPACE:
                print("Last move")
                board = all[-1]
                print(board)
                
            elif event.key == pygame.K_SPACE:
                print("Space pressed")
                #print(posX, " , ",posY)
                print("Current Piece:",board[posY][posX])

                if (board[posY][posX] == '.' and not pieceSet):
                    continue
                if (posX == setX and posY == setY):
                    pieceSet = False
                    reset = True
                    continue
                '''
                temp = board[setY][setX]
                print(temp)
                print(temp.isupper())
                print(turn)
                if (temp.isupper() != turn):
                    print(2)
                    break
                '''
                if (pieceSet):
                    if (checkMove(board,posX,posY,setX,setY,turn)):
                        print(5)
                        movePiece(board,posX,posY,setX,setY)
                        turn = not turn
                        reset = True
                        continue
                    #print(4)
                print(3)
                pieceSet = True
                setCursor(screen,posX,posY,0)
                setX = posX
                setY = posY

            elif (reset):
                setX = 0
                setY = 0
                reset = False
                pieceSet = False
                #setCursor(screen,-10,-10)
            print("----")

    #print(turn)
    if (player == 1 and not turn):
        move = False
        #print("run")
        while (True):
            #print("running")
            ranX = int(random.randint(0,7))
            #print(ranX)
            ranY = int(random.randint(0,7))
            #print(ranY)
            #print("(",ranX,",",ranY,")")
            temp = board[ranY][ranX]
            if (temp.isupper() and temp != "."):
                for x in range(10):
                    t1 = int(random.randint(0,7))
                    t2 = int(random.randint(0,7))
                    if (t1 == ranX and t2 == ranY):
                        continue
                    if (checkMove(board,t1,t2,ranX,ranY,turn)):
                        movePiece(board,t1,t2,ranX,ranY)
                        turn = not turn
                        reset = True
                        move = True
                        break
            if (move):
                break


            
    pygame.display.flip()
    time.sleep(.01)






