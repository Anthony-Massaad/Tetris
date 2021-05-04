from abc import ABC, abstractmethod
# all Shape classes inheritance and implements this abstract Shape class


class Shape(ABC):
    """
    Abstract classs with methods that all Shape classes inherence and implements
    """

    @abstractmethod
    def verticalMovement(self, board):
        """
        The Default vertical movement for all shapes
        Will shift one down almost every half a second
        :param board: The game Board
        :return: None
        """
        pass

    @abstractmethod
    def draw(self, board):
        """
        Method to Draw the Shape on the GameBoard for All Shapes
        :param board: The Game Board
        :return: None
        """
        pass

    @abstractmethod
    def controls(self, board):
        """
        for All Shapes, method to control the shape
        Right, left, and down to move the shape right, left or down
        rotation is done by pressing the up key
        :param board: the Game Baord
        :return: None
        """
        pass

    @abstractmethod
    def boundCheckingLeft(self, board):
        """
        bound checking for the left side of the board
        This ensures that any shape cannot move out of bounds on the left side of the board
        Also can't move left if it collides with an occupied space on the board (aka another square)
        :param board: the game Board
        :return: boolean. True if you can't move, False otherwise
        """
        pass

    @abstractmethod
    def boundCheckingRight(self, board):
        """
        bound checking for the right side of the board
        This ensures that any shape cannot move out of bounds on the right side of the board
        Also can't move right if it collides with an occupied space on the board (aka another square)
        :param board: the game Board
        :return: boolean. True if you can't move, False otherwise
        """
        pass

    @abstractmethod
    def boundCheckingBottom(self, board):
        """
        bound checking for the bottom side of the board
        This ensures that any shape cannot move out of bounds on the bottom side of the board
        :param board: the game Board
        :return: boolean. True if you can't move, False otherwise
        """
        pass

    @abstractmethod
    def collision(self, board):
        """
        bound checking if the shape will collide with another square on the board for vertical movement
        If true, meaning it collides and placed on the board
        otherwise, will continue to move and the user can keep controlling until collision hits True
        :param board: the game Board
        :return: boolean. True if the next movement collides with another square, otherwise False
        """
        pass

    @abstractmethod
    def rotate(self, board):
        """
        Let P be the pivot point of a square
        Using linear algebra rotation formula, the equation of rotation is,
        new_X = Px + Py - old_Y
        New_Y = old_X - Px + Py

        First the rotation checks if the ideal rotation collides with any other square on the board
        If so, it will no rotate the shape
        Otherwise, it will rotate the shape and check if it leaves the board on the right or left side
        if the square does leave the board on the right side, it will shift the shape to the left until it's good
        Same thing with the Left side, but will shift the shape to the right until it's good

        :param board: The Game board
        :return: None
        """
        pass

    @abstractmethod
    def getIndex(self, x, y):
        """
        Method to obtain the row and col given the x and y position of a square
        As Said in the Main function, for the x and y of a square it equates to 
        x = 251 + (30 * col)
        y = 1 + (30 * row)
        so rearranging, 
        row = y - 1 // 30
        col = x - 251 // 30 
        
        :param x: the square x position
        :param y: the square y position
        :return: row, col
        """
        pass

    @abstractmethod
    def shadowPlacement(self, board):
        """
        Determines the prediction placement of the current shape from where its position downwards

        :param board: the game board
        :return: None

        """
        pass

    @abstractmethod
    def drawNext(self, first, second, third):
        """
        Method to draw the shapes at a specific location on the left side of the game display according to if it's
        first in line, second in line or third in line 

        :param firt: boolean, True if shape is first in line otherwise False
        :param second: boolean, True if shape is seoncd in line otherwise False
        :param third: boolean, True if shape is third in line otherwise False
        :return: None
        """
        pass
