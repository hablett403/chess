'''
Stores all the information about a game's current state. It will also be responsible for determining valid moves at a determined state.
'''



class GameState():
    def __init__(self):
        # board is 2d 8x8 list with two characters, 
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP","bP","bP","bP","bP","bP","bP","bP"],
            ["--","--","--","--","--","--","--","--" ],
            ["--","--","--","--","--","--","--","--" ],
            ["--","--","--","--","--","--","--","--" ],
            ["--","--","--","--","--","--","--","--" ],
            ["wP","wP","wP","wP","wP","wP","wP","wP" ],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.moveFunctions = {
            "P" : self.getPawnMoves,
            "R" : self.getRookMoves,
            "N" : self.getKnightMoves,
            "B" : self.getBishopMoves,
            "Q" : self.getQueenMoves,
            "K" : self.getKingMoves
        }
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkmate = False
        self.stalemate = False

    def makeMove(self, move):
        '''
        Takes a move and executes it - does not work for castling, pawn promotion and en passant
        '''
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        #update king's location:
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

    def undoMove(self):
        if len(self.moveLog) != 0 :
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove #switch move back
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)


    def getValidMoves(self):
        #1) Generate all possible moves
        possibleMoves = self.getAllPossibleMoves()
        #2) For each move, actually make the move
        #we iterate over backwards since we are potentially removing elements
        for i in range(len(possibleMoves) - 1, -1, -1 ):
            self.makeMove(possibleMoves[i])
            self.whiteToMove = not self.whiteToMove
        #3) Generate all of the opponent's moves
        #4) If any move attacks the king, it's not a valid move
            if self.inCheck():
                possibleMoves.remove(possibleMoves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(possibleMoves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        return possibleMoves # will be changed later 
    
    def inCheck(self):
        #determine if the current player is in check
        if self.whiteToMove:
            return self.sqUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.sqUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def sqUnderAttack(self, row, col):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == row and move.endCol == col:
                return True
        return False


    def getAllPossibleMoves(self):
        '''
        Generates all possible moves to be considered for leaving the kind in check. 
        '''
        possibleMoves = []
        for row in range(8):
            for col in range(8):
                color, piece = self.board[row][col]
                if(color == "w" and self.whiteToMove) or (color == "b" and not self.whiteToMove):
                    self.moveFunctions[piece](row, col, possibleMoves)
        return possibleMoves


    def getPawnMoves(self, row, col, possibleMoves):
        if self.whiteToMove:
            if self.board[row - 1][col] == "--": #to move forward 1 if unimpeded
                possibleMoves.append(Move((row, col), (row - 1, col), self.board))
                if row == 6 and self.board[row - 2][col] == "--":
                    possibleMoves.append(Move((row, col), (row - 2, col), self.board))
            if col >= 1 and self.board[row - 1][col - 1][0] == "b":
                possibleMoves.append( Move((row, col), (row - 1, col - 1), self.board) )
            if col <= 6 and self.board[row - 1][col + 1][0] == "b":
                possibleMoves.append( Move((row, col), (row - 1, col + 1), self.board) )

        if not self.whiteToMove:
            if self.board[row + 1][col] == "--": #to move forward 1 if unimpeded
                possibleMoves.append(Move((row, col), (row + 1, col), self.board))
                if row == 1 and self.board[row + 2][col] == "--":
                    possibleMoves.append(Move((row, col), (row + 2, col), self.board))
            if col >= 1 and self.board[row + 1][col - 1][0] == "w":
                possibleMoves.append( Move((row, col), (row + 1, col - 1), self.board) )
            if col <= 6 and self.board[row + 1][col + 1][0] == "w":
                possibleMoves.append( Move((row, col), (row + 1, col + 1), self.board) )           


    def getRookMoves(self, row, col, possibleMoves):
        colour = self.board[row][col][0]

        #move right
        r_col = col
        while r_col != 7:
            r_col += 1
            if self.board[row][r_col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (row, r_col), self.board) )
                if self.board[row][r_col][0] != "-":
                    break

        #move left
        l_col = col
        while l_col != 0:
            l_col -= 1
            if self.board[row][l_col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (row, l_col), self.board) )
                if self.board[row][l_col][0] != "-":
                    break
        #move down
        d_row = row
        while d_row != 7:
            d_row += 1
            if self.board[d_row][col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (d_row, col), self.board) )
                if self.board[d_row][col][0] != "-":
                    break

        #move up
        u_row = row
        while u_row != 0:
            u_row -= 1
            if self.board[u_row][col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (u_row, col), self.board) )  
                if self.board[u_row][col][0] != "-":
                    break


    def getBishopMoves(self, row, col, possibleMoves):
        colour = self.board[row][col][0]

        #move up-right
        u_row, r_col = row, col
        while u_row != 0 and r_col != 7:
            u_row -= 1
            r_col += 1
            if self.board[u_row][r_col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (u_row, r_col), self.board) )
                if self.board[u_row][r_col][0] != "-":
                    break
        #move down-right
        d_row, r_col = row, col
        while d_row != 7 and r_col != 7:
            d_row += 1
            r_col += 1
            if self.board[d_row][r_col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (d_row, r_col), self.board) )
                if self.board[d_row][r_col][0] != "-":
                    break
        #move down-left
        d_row, l_col = row, col
        while d_row != 7 and l_col != 0:
            d_row += 1
            l_col -= 1
            if self.board[d_row][l_col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (d_row, l_col), self.board) )
                if self.board[d_row][l_col][0] != "-":
                    break
        #move up-left
        u_row, l_col = row, col
        while u_row != 0 and l_col != 0:
            u_row -= 1
            l_col -= 1
            if self.board[u_row][l_col][0] == colour:
                break
            else:
                possibleMoves.append( Move((row, col), (u_row, l_col), self.board) )
                if self.board[u_row][l_col][0] != "-":
                    break
    def getQueenMoves(self, row, col, possibleMoves):
        self.moveFunctions["B"](row, col, possibleMoves)
        self.moveFunctions["R"](row, col, possibleMoves)

    def getKingMoves(self, row, col, possibleMoves):
        colour = self.board[row][col][0]
        for r in [-1, 0, 1]:
            for c in [-1, 0, 1]:
                if 0 <= row + r <= 7 and 0 <= col + c <= 7 and not(r==0 and c==0):
                    if self.board[row + r][col + c][0] != colour:
                        possibleMoves.append( Move((row, col), (row + r, col + c), self.board) )
                        

    def getKnightMoves(self, row, col, possibleMoves):
        colour = self.board[row][col][0]
        for r,c in [(-2, 1), (-1, 2), (1, 2), (2, 1),
                    (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            if 0 <= row + r <=7 and 0 <= col + c <= 7 and self.board[row + r][col + c][0] != colour:
                possibleMoves.append( Move((row, col), (row + r, col + c), self.board) )










class Move():

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    #We want to convert from our notation to rank file notation
    rankstoRows = {"1" : 7, "2" : 6, "3" : 5, "4" : 4, 
                    "5" : 3, "6" : 2, "7" : 1, "8" : 0}
    rowsToRanks = {v : k for k,v in rankstoRows.items()}

    filesToCols = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, 
                    "e" : 4, "f" : 5, "g" : 6, "h" : 7}

    colsToFiles = {v : k for k, v in filesToCols.items()}

    #returns the chess notation for a move we do, e.g. a8f2 is a move from a8 to f2
    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    
    def __eq__(self, other): #so that the engine can tell if two moves are the same, not literally the same object
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __repr__(self):
        #return f"[({self.startRow}, {self.startCol}), ({self.endRow}, {self.endCol})]"
        return self.getChessNotation()
