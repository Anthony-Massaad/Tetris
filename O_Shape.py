import pygame
from Shape import Shape


class OShape(Shape):
    def __init__(self, display):
        self.surface = display
        self.color = (255, 0, 0)
        self.landed = False
        self.shape = [
            (self.surface, self.color, [431, 1, 29, 29]),
            (self.surface, self.color, [461, 1, 29, 29]),
            (self.surface, self.color, [431, 31, 29, 29]),
            (self.surface, self.color, [461, 31, 29, 29]),
        ]
        self.pivot = pygame.draw.rect(self.shape[3][0], self.shape[3][1], self.shape[3][2]).topleft

    def verticalMovement(self, board):
        if not self.boundCheckingBottom(board) and not self.landed and not self.collision(board):
            for items in self.shape:
                items[2][1] += 30
            self.pivot = (self.pivot[0], self.pivot[1] + 30)

    def draw(self, board):
        for surf, color, dsp in self.shape:
            pygame.draw.rect(surf, color, dsp)
        self.controls(board)
        self.shadowPlacement(board)

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
        elif keys[pygame.K_DOWN] and not self.boundCheckingBottom(board) and not self.collision(
                board) and not self.landed:
            for items in self.shape:
                items[2][1] += 30
            self.pivot = (self.pivot[0], self.pivot[1] + 30)

    def boundCheckingLeft(self, board):
        for items in self.shape:
            if 221 <= items[2][0] <= 251:  # bound on the left hand side of the board
                return True
            x = items[2][0]
            y = items[2][1]
            row, col = self.getIndex(x, y)
            if board[row][col - 1] is not None:
                return True
        return False

    def boundCheckingRight(self, board):
        for items in self.shape:
            if 671 <= items[2][0] <= 701:  # Bound on the right side of the board
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
            if board[row + 1][col] is not None:
                for squares in self.shape:
                    row, col = self.getIndex(squares[2][0], squares[2][1])
                    board[row][col] = squares
                self.landed = True
                return True
        return False

    def rotate(self, board):
        pass

    def getIndex(self, x, y):
        return abs((y - 1) // 30), abs((x - 251) // 30)

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
        if first is True:
            copyShape = [
                (self.surface, self.color, [90, 88, 29, 29]),
                (self.surface, self.color, [120, 88, 29, 29]),
                (self.surface, self.color, [90, 118, 29, 29]),
                (self.surface, self.color, [120, 118, 29, 29]),
            ]
        elif second is True:
            copyShape = [
                (self.surface, self.color, [90, 250, 29, 29]),
                (self.surface, self.color, [120, 250, 29, 29]),
                (self.surface, self.color, [90, 280, 29, 29]),
                (self.surface, self.color, [120, 280, 29, 29]),
            ]
        elif third is True:
            copyShape = [
                (self.surface, self.color, [90, 412, 29, 29]),
                (self.surface, self.color, [120, 412, 29, 29]),
                (self.surface, self.color, [90, 442, 29, 29]),
                (self.surface, self.color, [120, 442, 29, 29]),
            ]

        for surf, color, dsp in copyShape:
            pygame.draw.rect(surf, color, dsp)
