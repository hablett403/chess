'''
Main Driver File. Handles userinput and displays current GameState object
'''

import pygame as pyg


from chessEngine import GameState
from chessEngine import Move

WIDTH = HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = WIDTH//DIMENSION
MAX_FPS = 15

pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
images = {}

def get_images():
    for piece in pieces:
        images[piece] = pyg.transform.scale(pyg.image.load(piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))




def drawBoard(screen):
    colours = [pyg.Color("white"), pyg.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            colour = colours[(r+c) % 2]
            pyg.draw.rect(screen, colour, pyg.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
           piece =  board[r][c]
           if piece != "--":
              screen.blit(images[piece], pyg.Rect(c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawGameState(screen, gs):
    '''
    Responsible for all the graphics with a current game state
    '''
    drawBoard(screen) #draw squares on the board
    drawPieces(screen, gs.board) # draw pieces on top of those squares

def main():
    pyg.init()
    pyg.display.set_caption("Hamish's Chess Game")
    screen = pyg.display.set_mode((WIDTH, HEIGHT))
    clock = pyg.time.Clock()
    screen.fill(pyg.Color("white"))

    gs = GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made


    get_images()
    running = True
    sqSelected = () # row col tuple keeping track of last click
    playerClicks = [] #keeps track of player clicks (two tuples)
    while running:
        for e in pyg.event.get():
            if e.type == pyg.QUIT:
                running = False

            # mouse handler
            elif e.type == pyg.MOUSEBUTTONDOWN:
                location = pyg.mouse.get_pos() #location of mouse
                col = location[0] // SQUARE_SIZE
                row = location[1]// SQUARE_SIZE
                if sqSelected == (row, col): #the user clicks the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #after 2nd class
                    move = Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    #reset user clicks
                        sqSelected = ()
                        playerClicks = []
                    else:
                        playerClicks = [sqSelected]

            # key handlers
            elif e.type == pyg.KEYDOWN:
                keys = pyg.key.get_pressed()
                if keys[pyg.K_z] and keys[pyg.K_LCTRL]:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        pyg.display.flip()





        

if __name__ == "__main__":
    main()
