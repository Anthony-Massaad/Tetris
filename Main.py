import pygame
import I_Shape, O_Shape, L_Shape, J_Shape, T_Shape, Z_Shape, S_Shape
import time
import random
pygame.init()
GAME_WIDTH = 700
GAME_HEIGHT = 780
TETRIS_WIDTH = 450
display = pygame.display.set_mode((GAME_WIDTH + 1, GAME_HEIGHT + 1))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
board = [[None for i in range(15)] for j in range(26)]
# Start Coordinates For board. Goes by (row, Col)
# Each Square will be approx 30x30 on board, but real is 29x29 to fit inside square of board
# (0,5),(0,6),(0,7),(0,8) <- I shape
# (0,6), (1,6), (2,6), (2,7) <- L Shape
# (0,6), (1,6), (2,6), (2,5) <- J Shape
# (0,5), (0,6), (1,6), (0,7) <- T Shape
# (0,6), (0,7), (1,6), (1,7) <- O Shape
# (0,6), (0,7), (1,7), (1,8) <- Z Shape
# (0,6), (0,7), (1,6), (1,5) <- S Shape
# Math coordinates for squares x and y
# x = 251 + (30 * col)
# y = 1 + (30 * row)
# For rotation, use linear algebra rotation formula to determine a general formula for all shapes
# in accordance to its pivot of rotation


def new_shape():
    """
    Method to generate a new shape
    :return: New Shape, and will never hit the return None 
    """
    ran = random.randrange(7)
    if ran == 0:
        return I_Shape.IShape(display)
    elif ran == 1:
        return O_Shape.OShape(display)
    elif ran == 2:
        return L_Shape.LShape(display)
    elif ran == 3:
        return J_Shape.JShape(display)
    elif ran == 4:
        return T_Shape.TShape(display)
    elif ran == 5:
        return Z_Shape.ZShape(display)
    elif ran == 6:
        return S_Shape.SShape(display)
    return None


def drawGird():
    """
    Method that draws the game grid for a 30x30 square
    """
    ROWS = 26
    COLS = 15
    distance = GAME_HEIGHT / ROWS
    distanceCol = TETRIS_WIDTH / COLS
    for i in range(ROWS + 1):
        pygame.draw.line(display, WHITE, (250, i * distance), (GAME_WIDTH, i * distance))
    for i in range(COLS + 1):
        pygame.draw.line(display, WHITE, (250 + i*distanceCol, 0), (250 + i*distanceCol, GAME_HEIGHT))


# Draws everything needed on the board
def draw():
    global score
    display.fill(BLACK)
    drawGird()
    currentShape.draw(board)
    # Draw the next Shape at the according Spot
    # Booleans goes: First, Second, third
    firstNextShape.drawNext(True, False, False)
    secondNextShape.drawNext(False, True, False)
    thirdNextShape.drawNext(False, False, True)
    display.blit(displayNextTxt, (80, 5))
    display.blit(displayScoreTxt, (62, 580))
    value = font.render(str(score), True, WHITE)
    display.blit(value, (100, 670))

    # Draw Squares on the board
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] is not None:
                square = board[row][col]
                pygame.draw.rect(square[0], square[1], square[2])

    pygame.display.update()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
last_time_ms = int(round(time.time()*1000)) # Start Timer in realtime
font = pygame.font.SysFont('Arial', 40)
currentShape = new_shape()
firstNextShape = new_shape()
secondNextShape = new_shape()
thirdNextShape = new_shape()
next_txt = "NEXT:"
displayNextTxt = font.render(next_txt, True, WHITE)
score_txt = "SCORE: "
displayScoreTxt = font.render(score_txt, True, WHITE)
score = 0
run = True
timerDuaration = 500
keepPlaying = True
while run:
    pygame.time.delay(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                currentShape.rotate(board)

    # Timer to check every half a second, in order to move the shape down by default then reset
    diff_time_ms = int(round(time.time() * 1000)) - last_time_ms
    if diff_time_ms >= timerDuaration:
        currentShape.verticalMovement(board)
        last_time_ms = int(round(time.time() * 1000))

    # If the Shape Lands
    if currentShape.landed is True:
        # checks if the user lost the game by checking the first row
        for lastColIndex in range(len(board[0])):
            if board[0][lastColIndex] is not None:
                keepPlaying = False
                break

        # checks if the user got a full row filled
        for row in range(len(board)):
            fill = 0
            for col in range(len(board[row])):
                if board[row][col] is None:
                    break
                fill += 1
            # if So, begin to up the score, set that row to None and shift everything down by 1 from that row towards row 0
            if fill == len(board[row]):
                score += 10

                if 100 <= score < 200:
                    timerDuaration = 400
                elif 200 <= score < 300:
                    timerDuaration = 300
                elif 300 <= score < 400:
                    timerDuaration = 200
                elif score >= 400:
                    timerDuaration = 100

                for col in range(len(board[row])):
                    board[row][col] = None
                for i in range(row - 1, 0, -1):
                    for j in range(len(board[i])):
                        if board[i][j] is not None:
                            item = board[i][j]
                            item[2][1] += 30
                            board[i + 1][j] = item
                            board[i][j] = None

        # If the player hasn't lost, continue drawing shapes
        if keepPlaying is True:
            currentShape = firstNextShape
            firstNextShape = secondNextShape
            secondNextShape = thirdNextShape
            thirdNextShape = new_shape()
    draw()

pygame.quit()

