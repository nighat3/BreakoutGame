# play.py
# Nighat Ansari (na295), Kati Hsu (kyh24)
# 8 December 2016
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout
App. Instances of Play represent a single game.  If you want to restart a new
game, you are expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model
objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a
complicated issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *
import colormodel

# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It
    animates the ball, removing any bricks as necessary.  When the game is won,
    it stops animating. You should create a NEW instance of Play (in Breakout)
    if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you
    want to access an attribute in class Breakout. It is okay if you do, but you
    MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter
    for any attribute that you need to access in Breakout.  Only add the getters
    and setters that you need for Breakout.
    
    You may change any of the attributes above as you see fit. For example, you
    may want to add new objects on the screen (e.g power-ups).  If you make
    changes, please list the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _offScreen [bool]: True if _ball is offscreen, False otherwise
    """
    
    # GETTERS AND SETTERS
    def getTries(self):
        """Returns: _tries attribute (number of tries left)"""
        return self._tries
    
    def setTries(self,value):
        """Sets the value of self._tries"""
        assert type(value)==int and value>=0
        self._tries=value
    
    def setBricks(self,left,y,color):
        """Helper method to draw the bricks
        
        Parameter left: x-coordinate of left boundary of brick
        Precondition: left is a number >= BRICK_SEP_H/2 (REMEMbER UPPER BOUND)
        
        Parameter y: y-coordinate of the center of the brick
        Precondition: y is a float between 0 and GAME_HEIGHT
        
        Parameter color: corresponds to row brick is in (color starts at 1)
        Precondition: color is an integer >0 """
        assert type(left) in [int, float] and left >= BRICK_SEP_H/2
        assert type(y) == float and y in range(0, GAME_HEIGHT+1)
        assert type(color) == int and color >0
        
        for z in range(BRICKS_IN_ROW):
            self._bricks.append(Brick(left, y,color))
            left=left+ BRICK_WIDTH + BRICK_SEP_H

    def getBricks(self):
        """Returns: attribute self._bricks"""
        return self._bricks
        
        
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializes an instance of Play (a new game)
        
        A game (instance of Play) consists of a paddle (Paddle object),
        bricks(list of Brick objects), and ball (Ball object).
        
        Initializes the self._bricks attribute with a list of Brick objects.
        Initializes self._paddle with a Paddle object. However, sets self._ball
        to None. A ball is not created at the start. Initializes self._tries to
        NUMBER_TURNS (3) because a player always starts off with three lives.
        Initializes self._offScreen to False because when the ball is created,
        it is not initially off the screen."""
        
        self._paddle = Paddle() # Initializes _paddle attribute
        # Initializes _brick attribute
       
        self._bricks = []
        left=float(BRICK_SEP_H/2)
        y=float(GAME_HEIGHT-BRICK_Y_OFFSET)
        color_counter=1
        for q in range(BRICK_ROWS):
            self.setBricks(left,y,color_counter)
            y= y- (BRICK_HEIGHT+BRICK_SEP_V)
            color_counter=color_counter+1
        self._ball= None # Initializes _ball attribute; no ball present at start
        self.setTries(NUMBER_TURNS) # Initializes _tries attribute
        self._offScreen = False
        
        
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, input):
        """This method checks for whether or not the 'left' or 'right' arrow key
        is pressed.
        
        If the 'left' arrow is pressed, the paddle will move to the left 6 units.
        If the 'right' arrow key is pressed, the paddle will shift to the right
        6 units. The paddle will not move to the left if the x-coordinate of its
        left boundary is (0,PADDLE_OFFSET). It will not move to the right if the
        x-coordinate of its right boundary is (GAME_WIDTH, PADDLE_OFFSET).
        
        The paddle does not move up or down."""
        assert isinstance(input, GInput)
        
        if input.is_key_down('left'):
            if self._paddle.left >= 0:
                self._paddle.left -= 6
        if input.is_key_down('right'):
            if self._paddle.right <= GAME_WIDTH:
                self._paddle.x += 6
            
    def makeBall(self):
        """When called, this method constructs a Ball object and assigns it to
        the _ball attribute of Play. This Ball is initiatelly placed at the
        center of the screen."""
        
        self._ball= Ball()
        
    def updateBall(self):
        """When called, this method moves the ball and handles any physics
        regarding the ball's movements. This method is called in update when
        self._state = STATE_ACTIVE"""
        
        self._ball.moveBall(self._paddle.collides(self._ball),\
                            self.collisionWithBricks())
        self._offScreen = self._ball.checkOffScreen()
                
        
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def playDraw(self, view):
        """This method draws the paddle, ball, and bricks to the game view.
        
        Parameter view: the game view used for drawing
        Precondition: view is an instance of GView"""
        
        assert isinstance(view, GView)
        
        # Draw bricks
        if self._bricks is not []:
            for b in self._bricks:
                b.draw(view)
        # Draw paddle
        if self._paddle is not None:
            self._paddle.draw(view)
        #Draw Ball
        if self._ball is not None:
            self._ball.draw(view)
        
    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def collisionWithBricks(self):
        """Returns: True if ball (self) collides with a brick. False otherwise."""
        if len(self._bricks)>0: 
            for b in self._bricks:
                    
                collideWithBrick = b.collides(self._ball)
                if collideWithBrick==True:
                    self._bricks.remove(b)
                    break
            return collideWithBrick
        else:
            return False
        
# ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
                