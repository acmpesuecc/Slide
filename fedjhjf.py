import pygame
import sys
import random
from pygame.locals import *

# declarations
BWIDTH = BHEIGHT = 4  # number of columns n rows in the board, will have to change in case of diff types of boards
TSIZE = 60  # tile size
WWIDTH = 840  # window width
WHEIGHT = 680  # window height
FPS = 150  # slide speed
BLANK = None

# colours
#                 R    G    B
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BEIGE = (223, 180, 143)
DARKTURQUOISE = (3, 54, 73)
PASTELBLUE = (131, 190, 215)
GREEN = (0, 255, 187)
PASTELPINK = (255, 192, 245)
GREEN = (41, 210, 80)
MAROON = (127, 31, 69)
COBALTBLUE = (83, 9, 255)
OLIVEGREEN = (23, 57, 28)
TEAL = (85, 210, 190)
CYAN = (108, 232, 240)
BROWN = (129, 74, 60)
SAND = (255, 198, 131)

# all button stuff
BGCOLOR = 
TILECOLOR = MAROON
TC = WHITE
BORDERCOLOR = DARKTURQUOISE
FONTSIZE = 25
BUTTONCOLOR = WHITE
BUTTONTC = BLACK
MESSAGECOLOR = BLACK

# board margins
XMARGIN = int((WWIDTH - (TSIZE * BWIDTH + (BWIDTH - 1))) / 2)
YMARGIN = int((WHEIGHT - (TSIZE * BHEIGHT + (BHEIGHT - 1))) / 2)

# action commands
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

# timer
screen = pygame.display.set_mode((WWIDTH - 100, WHEIGHT - 100))
clock = pygame.time.Clock()

# button setup


def main():

    global CLOCK, surfdisplay, BASICFONT, SURF_RESET, RECT_RESET, SURF_NEW, RECT_NEW, SURF_SOLVE, RECT_SOLVE, RECT_QUIT, SURF_QUIT

    pygame.init()
    CLOCK = pygame.time.Clock()

    surfdisplay = pygame.display.set_mode((WWIDTH, WHEIGHT), pygame.RESIZABLE)

    pygame.display.set_caption('Slide Puzzle')

    BASICFONT = pygame.font.Font('HKGrotesk-Regular.ttf', FONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    SURF_RESET, RECT_RESET = makeText('Reset', TC, TILECOLOR, WWIDTH - 120, WHEIGHT - 120)
    SURF_NEW, RECT_NEW = makeText('New Game', TC, TILECOLOR, WWIDTH - 120, WHEIGHT - 90)
    SURF_QUIT, RECT_QUIT = makeText('End Game', TC, TILECOLOR, WWIDTH - 120, WHEIGHT - 30)
    SURF_SOLVE, RECT_SOLVE = makeText('Solve', TC, TILECOLOR, WWIDTH - 120, WHEIGHT - 60)

    mainBoard, solutionSeq = generateNewPuzzle(80)

    SOLVEDBOARD = getStartingBoard()  # board in starting.

    allMoves = []  # list of moves made from the solved configuration

    # main game loop
    while True:

        Move = None  # the direction, if any, a tile should slide

        msg = ''  # contains the message to show in the upper left corner.

        if mainBoard == SOLVEDBOARD:

            msg = 'Solved!'

            drawBoard(mainBoard, msg)

            checkForQuit()

        # actions n outcomes sync
        for event in pygame.event.get():  # event handling loop

            if event.type == VIDEORESIZE:
                drawBoard(mainBoard, '')
            elif event.type == MOUSEBUTTONUP:

                spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

                if (spotx, spoty) == (None, None):  # check if the user clicked on an option button

                    if RECT_RESET.collidepoint(event.pos):  # clicked on Reset button
                        resetAnimation(mainBoard, allMoves)
                        allMoves = []

                    elif RECT_NEW.collidepoint(event.pos):  # clicked on New Game button
                        mainBoard, solutionSeq = generateNewPuzzle(80)
                        allMoves = []

                    elif RECT_SOLVE.collidepoint(event.pos):  # clicked on Solve button
                        resetAnimation(mainBoard, solutionSeq + allMoves)
                        allMoves = []

                    elif RECT_QUIT.collidepoint(event.pos):  # clicked on the End Game button
                        terminate()
                else:    # check if the clicked tile was next to the blank spot

                    blankx, blanky = getBlankPosition(mainBoard)

                    if spotx == blankx + 1 and spoty == blanky:
                        Move = LEFT

                    elif spotx == blankx - 1 and spoty == blanky:
                        Move = RIGHT

                    elif spotx == blankx and spoty == blanky + 1:
                        Move = UP

                    elif spotx == blankx and spoty == blanky - 1:
                        Move = DOWN

            elif event.type == KEYUP:  # check if the user pressed a key to slide a tile

                if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):

                    Move = LEFT

                elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):

                    Move = RIGHT

                elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):

                    Move = UP

                elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):

                    Move = DOWN

        if Move:

            slideAnimation(mainBoard, Move, 'Click tile or press arrow keys to slide.', 8)  # show slide on screen

            makeMove(mainBoard, Move)

            allMoves.append(Move)  # record the slide

        pygame.display.update()

        CLOCK.tick(60)

# defining all functions


def checkForQuit():

    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present

    for event in pygame.event.get(KEYUP):  # get all the KEYUP events

        if event.key == K_ESCAPE:  # terminate if the KEYUP event was for the Esc key
            terminate()
        pygame.event.post(event)  # put the other KEYUP event objects back


def terminate():

    pygame.quit()

    sys.exit()


def getStartingBoard():  # Return a board data structure with tiles in the solved state.

    counter = 1
    board = []
    for x in range(BWIDTH):
        column = []
        for y in range(BHEIGHT):
            column.append(counter)
            counter += BWIDTH
        board.append(column)
        counter -= BWIDTH * (BHEIGHT - 1) + BWIDTH - 1

    board[BWIDTH - 1][BHEIGHT - 1] = None
    return board


def getBlankPosition(board):  # Return the x and y of board coordinates of the blank space.

    for x in range(BWIDTH):
        for y in range(BHEIGHT):
            if board[x][y] == None:
                return (x, y)


def makeMove(board, move):  # tells the program how to move UP, DOWN, LEFT & RIGHT
    # This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]

    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]

    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]

    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):

    blankx, blanky = getBlankPosition(board)

    return (move == UP and blanky != len(board[0]) - 1) or (move == DOWN and blanky != 0) or (move == LEFT and blankx != len(board) - 1) or (move == RIGHT and blankx != 0)


def getRandomMove(board, lastMove=None):

    validMoves = [UP, DOWN, LEFT, RIGHT]

    # remove moves from the list as they are disqualified
    if lastMove == UP or not isValidMove(board, DOWN):
        validMoves.remove(DOWN)

    if lastMove == DOWN or not isValidMove(board, UP):
        validMoves.remove(UP)

    if lastMove == LEFT or not isValidMove(board, RIGHT):
        validMoves.remove(RIGHT)

    if lastMove == RIGHT or not isValidMove(board, LEFT):
        validMoves.remove(LEFT)
    # return a random move from the list of remaining moves
    return random.choice(validMoves)


def getpixelcoord(tileX, tileY):  # gives value of top left coordinates of a tile
    left = XMARGIN + (tileX * TSIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TSIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):  # from the x & y pixel coordinates, get the x & y board coordinates

    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getpixelcoord(tileX, tileY)
            tileRect = pygame.Rect(left, top, TSIZE, TSIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)

    return (None, None)


def drawTile(tilex, tiley, number, driftx=0, drifty=0):  # drawing a tile

    left, top = getpixelcoord(tilex, tiley)
    pygame.draw.rect(surfdisplay, BLACK, (left + driftx, top + drifty, TSIZE, TSIZE), border_radius=8)
    pygame.draw.rect(surfdisplay, GREEN, (left + driftx, top + drifty, TSIZE, TSIZE), 3, border_radius=8)
    textSurf = BASICFONT.render(str(number), True, TC)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TSIZE / 2) + driftx, top + int(TSIZE / 2) + drifty

    surfdisplay.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):  # creating Surface and Rect objects for some text like a text box

    textSurf = BASICFONT.render(text, True, WHITE, BGCOLOR)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def timer():
    counter, text = 0, '0'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    font = pygame.font.SysFont('Consolas', 30)
    return counter, font


def drawBoard(board, message):  # current board creation

    surfdisplay.fill(BGCOLOR)
    if message:   # message on top left corner
        textSurf, textRect = makeText(message, MESSAGECOLOR, WHITE, WWIDTH / 3, WHEIGHT / 6)
        surfdisplay.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])


def slideAnimation(board, direction, message, animationSpeed):  # tile sliding action
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1

    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1

    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky

    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = surfdisplay.copy()

    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getpixelcoord(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft, moveTop, TSIZE, TSIZE))

    for i in range(0, TSIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        surfdisplay.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)

        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)

        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)

        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()

        CLOCK.tick(FPS)

    checkForQuit()
    surfdisplay.blit(baseSurf, (0, 0))
    drawTile(blankx, blanky, board[movex][movey], 0, 0)

    pygame.display.update()

    CLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # making numSlides number of moves from solved config and animating

    sequence = []
    board = getStartingBoard()
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    lastMove = None

    for i in range(numSlides):
        move = getRandomMove(board, lastMove)
        slideAnimation(board, move, 'Generating new puzzle...', int(TSIZE / 3))
        makeMove(board, move)
        sequence.append(move)
        lastMove = move

    return (board, sequence)


def resetAnimation(board, allMoves):
    # all moves reversed... can be used for solving

    revAllMoves = allMoves[:]  # gets a copy of the list
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN

        elif move == DOWN:
            oppositeMove = UP

        elif move == RIGHT:
            oppositeMove = LEFT

        elif move == LEFT:
            oppositeMove = RIGHT

        slideAnimation(board, oppositeMove, '', int(TSIZE / 2))
        makeMove(board, oppositeMove)


if __name__ == '__main__':
    main()
