import Connect4_Ai
import math
import time

# CONSTANTS
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

ROW_COUNT = 6
COLUMN_COUNT = 7

WINDOW_LENGTH = 4

class Grid:
    def __init__(self):
        self.num = 1
        self.grid = [[0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0]]
        self.gameOver = False

    def Drop(self, column):
        i = 0
        for i in range(6):
           if self.grid[column][i] != 0:
                self.grid[column][i-1] = self.num
                break
           elif i == 5:
                self.grid[column][i] = self.num
                
    def CheckDiagonal(self, row, column, inrow, left):#left = -1, right = 1, up 1, down -1
        column += left
        row -= 1

        if column < 7 and row < 6:
            if self.grid[column][row] == self.num:
                inrow += 1
                if inrow == 4:
                    self.gameOver = True
                else:
                    self.CheckDiagonal(row, column, inrow, left)


    def CheckVertical(self, row, column, inrow):
        row -= 1
        if row != -1:
            if self.grid[column][row] == self.num:
                inrow += 1
                if inrow == 4:
                    self.gameOver = True
                else:
                    self.CheckVertical(row, column, inrow)


    def CheckHorizontal(self, row, column, inrow):
        column += 1
        if column != 7:
            if self.grid[column][row] == self.num:
                inrow += 1
                if inrow == 4:
                    self.gameOver = True
                else:
                    self.CheckHorizontal(row, column, inrow)


    #def PieceWinCheck(self):
    #    for i in range(7):
     #       for u in range (6):
      #          if self.grid[i][u] == self.num:
       #             self.CheckDiagonal(u, i, 1, -1)
        #            self.CheckDiagonal(u, i, 1, 1)
         #           self.CheckHorizontal(u, i, 1)
          #          self.CheckVertical(u, i, 1)

    
    def SwapTurn(self):
        if self.num == 1:
            self.num = 2
        else:
            self.num = 1

    def Display(self):
        grid = self.grid
        print(grid[0][0], grid[1][0], grid[2][0], grid[3][0], grid[4][0], grid[5][0], grid[6][0])
        print(grid[0][1], grid[1][1], grid[2][1], grid[3][1], grid[4][1], grid[5][1], grid[6][1])
        print(grid[0][2], grid[1][2], grid[2][2], grid[3][2], grid[4][2], grid[5][2], grid[6][2])
        print(grid[0][3], grid[1][3], grid[2][3], grid[3][3], grid[4][3], grid[5][3], grid[6][3])
        print(grid[0][4], grid[1][4], grid[2][4], grid[3][4], grid[4][4], grid[5][4], grid[6][4])
        print(grid[0][5], grid[1][5], grid[2][5], grid[3][5], grid[4][5], grid[5][5], grid[6][5])

    def Turn(self, column):
        self.Drop(column)
        self.Display()
        self.gameOver = Connect4_Ai.PieceWinCheck(self.grid, self.num)
        if self.gameOver == True:
            readableWinner = ""
            if self.num == 1:
                readableWinner = "Player"
            elif self.num == 2:
                readableWinner = "Ai"

            print("##############################")
            print("The ", readableWinner, " has won")
            print("##############################")
            self.Display()
            
        #else:
            #self.SwapTurn() #removed to change how turns are handled
            #self.Turn() #removed to change how turns are handled

    def Gameplay(self, approxRunTime):
        runTime = 0
        depth = 6

        while self.gameOver == False:
            #player 1 turn (Human)
            print("Player 1's Turn")
            self.num = 1

            #validate human inputs
            column = int(input("select a column 1-7: "))
            while self.ValidatePlayerTurn(column) == False:
                column = int(input("select a column 1-7: "))
            columnIndex = column - 1

            self.Turn(columnIndex)

            #player 2's turn (AI)
            if self.gameOver == False:
                
                print("Player 2's Turn")
                print("Ai is thinking with a depth of "+str(depth))
                self.num=2 

                #AI Decision with timer
                start = time.time()
                column = Connect4_Ai.minimax(self.grid, depth,-math.inf, math.inf, True)[0]
                end = time.time()
                runTime = end - start
                #output a few stats 
                print("MinMax Algorithm took "+str(runTime)+"s to run at a depth of "+str(depth))
                #print("Ratio of Ai wins/Player Wins "+str(aiWinNum)+"/"+str(p1WinNum))
                #print("Ratio: "+str(aiWinNum/p1WinNum))

                #tune depth to in
                # crease accuracy as runtime decreases
                if runTime < approxRunTime - 2.5:
                    depth += 1
                    print("Depth increased to "+str(depth))
                elif runTime > approxRunTime + 2.5 and runTime > 6:
                    depth -= 1
                    print("Depth decreased to "+str(depth))

                self.Turn(column)  
                print("The AI has played column "+str(column+1))

    def ValidatePlayerTurn(self,column):
        columnIndex = column - 1
        #checks for blank input
        if column == None:
            print("please input a number: ")
            return False
        
        #checks for vaild column number
        column = int(column)
        if column < 1 or column > 7:
            print("number must be between 1-7")
            return False

        #checks column isnt full
        grid = self.grid

        if grid[columnIndex][0] == 0:
            return True
        else:
            print("The selected row is full")
            return False

  
game = Grid()
game.Display()
game.Gameplay(10) #lower numbers are easier, higher numbers are harder