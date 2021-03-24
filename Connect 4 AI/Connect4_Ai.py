import math
import random
import numpy as np  

#constants to make code more readable
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

ROW_COUNT = 6
COLUMN_COUNT = 7

WINDOW_LENGTH = 4

#scoreing constants
WIN_SCORE = 1000000000
LOSE_SCORE = -100000000

FOURINROW = 100
THREEINROW = 10
TWOINROW = 3
MIDDLE_COLUMN =1

##################### min max algorithm ################################

def minimax (grid, depth, alpha, beta, isMaximisingPlayer):
    validLocations = getValidMoves(grid)

    #depth = 0 game won or no valid moves left
    if isTerminal(grid) or depth == 0: 
        if isTerminal(grid):
            if PieceWinCheck(grid, AI_PIECE):
                print("Possible AI win found")
                return(None, WIN_SCORE - depth) #subtracting depth makes AI favour a quicker win over a long one
            elif PieceWinCheck(grid, PLAYER_PIECE):
                print("Possible Player win found")
                return(None, -LOSE_SCORE + depth)
            else: #game over no more valid moves
                return (None, 0)
        else: #depth is 0 so leaf node reached
            return (None, score_position(grid,AI_PIECE)) #return score for game output
      
    if isMaximisingPlayer:
        value = -math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            tempGrid = np.copy(grid)
            Drop(tempGrid, col, AI_PIECE)
            newScore = minimax(tempGrid, depth-1, alpha, beta, False)[1]
            if newScore > value:
                value = newScore
                column = col

            #alpha pruning
            alpha = max (alpha, value)
            if alpha >= beta:
                break

        return column, value
    
    else: #minimising player
        value = math.inf
        column = random.choice(validLocations)
        for col in validLocations:
            tempGrid = np.copy(grid)
            Drop(tempGrid, col, PLAYER_PIECE)
            newScore = minimax(tempGrid, depth-1, alpha, beta, True)[1]
            if newScore < value:
                value = newScore
                column = col
            
            #beta pruning
            beta = min(beta, value)
            if alpha >= beta:
                break
        
        return column, value

#################### making moves ##########################

def Drop(grid, column, num):
        i = 0
        for i in range(6):
           if grid[column][i] != 0:
                grid[column][i-1] = num
                break
           elif i == 5:
                grid[column][i] = num
        return grid


################### finding valid moves ############################

def getValidMoves(grid):
    validLocaions=[]
    for column in range(COLUMN_COUNT):
        if IsValid(grid, column) == True:
            validLocaions.append(column)
    return validLocaions

def IsValid(grid, columnIndex):
     #checks column isnt full
        if grid[columnIndex][0] == 0: #if top empty turn is valid
            return True
        else: #else column is full and move not valid
            return False

################# evaluating board ###################

def score_position(board, piece):
	score = 0

	## Score center column
	center_array = [int(i) for i in list(board[COLUMN_COUNT//2,:])]
	center_count = center_array.count(piece)
	score += center_count * MIDDLE_COLUMN

	## Score Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[:,r])]
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[c,:])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+WINDOW_LENGTH]
			score += evaluate_window(window, piece)

	## Score postive sloped diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[c+i][r+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[c+3-i][r+i] for i in range(WINDOW_LENGTH)]
			score += evaluate_window(window, piece)

	return score


def evaluate_window(window, piece):
	score = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += FOURINROW
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		score += THREEINROW
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		score += TWOINROW

	if window.count(opp_piece) == 4:
		score -= FOURINROW
	elif window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		score -= THREEINROW
	elif window.count(opp_piece) == 2 and window.count(EMPTY) == 2:
		score -= TWOINROW
	return score

########################### Game End Conditions ##################

def isTerminal(grid): #is grid full
    return PieceWinCheck(grid, PLAYER_PIECE) or PieceWinCheck(grid, AI_PIECE) or len(getValidMoves(grid)) == 0

def PieceWinCheck(board, piece): # has someone won
	# Check vert? locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT -3):
			if board[c][r] == piece and board[c][r+1] == piece and board[c][r+2] == piece and board[c][r+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT -3):
		for r in range(ROW_COUNT):
			if board[c][r] == piece and board[c+1][r] == piece and board[c+2][r] == piece and board[c+3][r] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[c][r] == piece and board[c+1][r-1] == piece and board[c+2][r-2] == piece and board[c+3][r-3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT -3):
			if board[c][r] == piece and board[c+1][r+1] == piece and board[c+2][r+2] == piece and board[c+3][r+3] == piece:
				return True
