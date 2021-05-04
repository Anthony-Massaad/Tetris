import pygame
from Shape import Shape


class IShape(Shape):
    def __init__(self, display):
        self.surface = display
        self.shape = []
        self.color = (0, 222, 255)
        self.landed = False
        for i in range(4):
            self.shape.append((self.surface, self.color, [251 + (30*(i+5)), 1, 29, 29]))
        self.pivot = pygame.draw.rect(self.shape[1][0], self.shape[1][1], self.shape[1][2]).topright

    def draw(self, board):
        for surf, color, dsp in self.shape:
            pygame.draw.rect(surf, color, dsp)
        self.controls(board)
        self.shadowPlacement(board)

    def boundCheckingLeft(self, board):
        for items in self.shape:
            if 221 <= items[2][0] <= 251: # bound on the left hand side of the board
                return True
            x = items[2][0]
            y = items[2][1]
            row, col = self.getIndex(x,y)
            if board[row][col-1] is not None:
                return True
        return False

    def boundCheckingRight(self, board):
        for items in self.shape:
            if 671 <= items[2][0] <= 701: #Bound on the right side of the board
                return True
            x = items[2][0]
            y = items[2][1]
            row, col = self.getIndex(x, y)
            if board[row][col + 1] is not None:
                return True
        return False

    def boundCheckingBottom(self, board):
        for items in self.shape:
            if 751 <= items[2][1] <= 781:
                for squares in self.shape:
                    row, col = self.getIndex(squares[2][0], squares[2][1])
                    board[row][col] = squares
                self.landed = True
                return True
        return False

    def collision(self, board):
        for items in self.shape:
            x = items[2][0]
            y = items[2][1]
            row, col = self.getIndex(x, y)
            if board[row+1][col] is not None:
                for squares in self.shape:
                    row, col = self.getIndex(squares[2][0], squares[2][1])
                    board[row][col] = squares
                self.landed = True
                return True
        return False

    def controls(self, board):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not self.boundCheckingLeft(board) and not self.landed:
            for items in self.shape:
                items[2][0] -= 30
            self.pivot = (self.pivot[0] - 30, self.pivot[1])
        elif keys[pygame.K_RIGHT] and not self.boundCheckingRight(board) and not self.landed:
            for items in self.shape:
                items[2][0] += 30
            self.pivot = (self.pivot[0] + 30, self.pivot[1])
        elif keys[pygame.K_DOWN] and not self.boundCheckingBottom(board) and not self.collision(board) and not self.landed:
            for items in self.shape:
                items[2][1] += 30
            self.pivot = (self.pivot[0], self.pivot[1] + 30)

    def verticalMovement(self, board):
        if not self.boundCheckingBottom(board) and not self.landed and not self.collision(board):
            for items in self.shape:
                items[2][1] += 30
            self.pivot = (self.pivot[0], self.pivot[1] + 30)

    def getIndex(self, x, y):
        return ((y - 1) // 30), ((x - 251) // 30)

    def rotate(self, board):
        if not self.boundCheckingBottom(board) and not self.collision(board):
            #First check if rotaion request intersects with other blocks
            for items in self.shape:
                oldX = items[2][0] - 1
                possibleX = ((self.pivot[0] + self.pivot[1]) - items[2][1]) + 1
                possibleY = oldX - self.pivot[0] + self.pivot[1]
                row, col = self.getIndex(possibleX, possibleY)
                try:
                    if board[row][col] is not None:
                        return
                except:
                    pass

            #Main Rotation
            for items in self.shape:
                oldX = items[2][0] - 1
                items[2][0] = ((self.pivot[0] + self.pivot[1]) - items[2][1]) + 1
                items[2][1] = oldX - self.pivot[0] + self.pivot[1]
                while True:
                    row, col = self.getIndex(items[2][0], items[2][1])
                    if col > 14:
                        for squares in self.shape:
                            squares[2][0] -= 30
                        self.pivot = (self.pivot[0] - 30, self.pivot[1])
                    elif col < 0:
                        for squares in self.shape:
                            squares[2][0] += 30
                        self.pivot = (self.pivot[0] + 30, self.pivot[1])
                    else:
                        break

    def shadowPlacement(self, board):
        # **DeepCopy Doesn't work for pygame surface so working around it was necessary**
        shadowShape = []
        for surf, color, dsp in self.shape:
            shadowShape.append((surf, color, dsp.copy()))
        move = True
        while move is True:
            for squares in shadowShape:
                if 751 <= squares[2][1] <= 781:
                    move = False
                    break
                row, col = self.getIndex(squares[2][0], squares[2][1])
                if board[row + 1][col] is not None:
                    move = False
                    break
            if move is True:
                for squares in shadowShape:
                    squares[2][1] += 30
        for surf, color, dsp in shadowShape:
            pygame.draw.rect(surf, color, dsp, 1)


    def drawNext(self, first, second, third):
        copyShape = []
        for surf, color, dsp in self.shape:
            copyShape.append((surf, color, dsp.copy()))
        if first is True:
            for i, squares in enumerate(copyShape):
                squares[2][0] = 35 + (30 * (i + 1))
                squares[2][1] = 88
        elif second is True:
            for i, squares in enumerate(copyShape):
                squares[2][0] = 35 + (30 * (i + 1))
                squares[2][1] = 250
        elif third is True:
            for i, squares in enumerate(copyShape):
                squares[2][0] = 35 + (30 * (i + 1))
                squares[2][1] = 412

        for surf, color, dsp in copyShape:
            pygame.draw.rect(surf, color, dsp)




