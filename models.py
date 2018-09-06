# models.py
# Nighat Ansari (na295), Kati Hsu (kyh24)
# 8 December 2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything
that you interact with on the screen is model: the paddle, the ball, and any of
the bricks.

Technically, just because something is a model does not mean there has to be a
special class for it.  Unless you need something special, both paddle and
individual bricks could just be instances of GRectangle.  However, we do need
something special: collision detection. That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you
add new features to your game.  If you are unsure about whether to make a new
class or not, please ask on Piazza."""

import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module
# constants.py.
# If you need extra information from Play, then it should be a parameter in your
#method, 
# and Play should pass it as a argument when it calls the method.

class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as
    move it left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self):
        """Initializes an instance of Paddle.
            Uses the GRectangle initializer to initialize values x and y
            (position), width, height, and fillcolor.
        """
        GRectangle.__init__(self,x=GAME_WIDTH/2,y=PADDLE_OFFSET,width=\
                            PADDLE_WIDTH,height=PADDLE_HEIGHT, \
                            fillcolor=colormodel.BLACK)
      
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self,ball):
        """Returns: True if the ball collides with paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        assert isinstance(ball, Ball)
        
        point1 = self.contains(ball.get_x() - (BALL_DIAMETER/2), ball.get_y() +\
                               (BALL_DIAMETER/2))
        point2 = self.contains(ball.get_x() - (BALL_DIAMETER/2), ball.get_y() -\
                               (BALL_DIAMETER/2))
        point3 = self.contains(ball.get_x() + (BALL_DIAMETER/2), ball.get_y() -\
                               (BALL_DIAMETER/2))
        point4 = self.contains(ball.get_x() + (BALL_DIAMETER/2), ball.get_y() +\
                               (BALL_DIAMETER/2))
        
        if (point1 or point2 or point3 or point4) and ball.get_vy() < 0:
            return True
        else:
            return False
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Brick(GRectangle):
    """An instance is the game brick.
    
    This class contains a method to detect collision with the ball.  You may
    wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    _linecolor: color of outline of brick [colormodel attribute]
    
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    colorNumber: [int] represents the current row being lined with bricks.
                 This row number correponds to a particular color.      
    """
    
    # GETTERS AND SETTERS 
    def setLinecolor(self, color):
        """Sets _linecolor attribute"""
        assert isinstance(color, colormodel.RGB)
        self._linecolor = color
        
    def __init__(self, x, y, colorNumber):
        """Initializes a Brick object."""
 
        assert type(colorNumber)==int and colorNumber>0
        assert type(x) == float and x in range(0, GAME_WIDTH+1)
        assert type(y) == float and y in range(0, GAME_HEIGHT+2)
        
        if colorNumber==1 or colorNumber==2:
                colorNumber=BRICK_COLOR[0]
                self.setLinecolor(colorNumber)
        elif colorNumber==3 or colorNumber==4:
                colorNumber=BRICK_COLOR[1]
                self.setLinecolor(colorNumber)
        elif colorNumber==5 or colorNumber==6:
                colorNumber=BRICK_COLOR[2]
                self.setLinecolor(colorNumber)
        elif colorNumber==7 or colorNumber==8:
                colorNumber=BRICK_COLOR[3]
                self.setLinecolor(colorNumber)
        elif colorNumber==9 or colorNumber==10:
                colorNumber=BRICK_COLOR[4]
                self.setLinecolor(colorNumber)
        
        GRectangle.__init__(self, left=x, y=y, width=BRICK_WIDTH,\
                            height=BRICK_HEIGHT, fillcolor=colorNumber,\
                            linecolor=self._linecolor)
    
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        assert isinstance(ball, Ball)
        
        point1 = self.contains(ball.get_x() - (BALL_DIAMETER/2), ball.get_y() +\
                               (BALL_DIAMETER/2))
        point2 = self.contains(ball.get_x() - (BALL_DIAMETER/2), ball.get_y() -\
                               (BALL_DIAMETER/2))
        point3 = self.contains(ball.get_x() + (BALL_DIAMETER/2), ball.get_y() -\
                               (BALL_DIAMETER/2))
        point4 = self.contains(ball.get_x() + (BALL_DIAMETER/2), ball.get_y() +\
                               (BALL_DIAMETER/2))
        
        if point1 or point2 or point3 or point4:
            return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for
    velocity. This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    """
        
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def get_vx(self):
        """Returns: the attribute _vx."""
        
        return self._vx
    
    def get_vy(self):
        """Returns: the attribute _vy."""
        
        return self._vy
    
    def get_x(self):
        """Returns: x coordinate of the center of the ball"""
        
        return self.x
    
    def get_y(self):
        """"Returns: y coordinate of the center of the ball"""
        
        return self.y
    
    def set_vx(self, value):
        """Sets _vx attribute"""
        assert type(value)==int or type(value)==float
        self._vx=value
    
    def set_vy(self, value):
        """Sets _vy attribute"""
        assert type(value)==int or type(value)==float
        self._vy=value
    
        
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """Initializes instance of Ball.
        
        Uses the GEllipse initializer to initialize inherited attributes
        that specify position, height, width, and color of the ball object.
        x(position), y (position), width, height, and fillcolor.
        Initializes _vx and _vy separately, which are attributes specific to
        a Ball object."""
        
        GEllipse.__init__(self, x=GAME_WIDTH/2,y=GAME_HEIGHT/2,\
                          width=BALL_DIAMETER/2,
                          height=BALL_DIAMETER/2,fillcolor=colormodel.RED)
        self._vx=random.uniform(1.0,5.0)
        self._vx=self._vx*random.choice([-1,1])
        self._vy=-5.0
        
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self, c,b):
        """Controls ball's movements.
        
        This method initializes top_point, bottom_point, right_point, and
        left_point to be the points on the ball to use in order to check whether
        the ball has hit one of the four walls of the screen. If the
        y-coordinate of the top point of the ball becomes greater than or equal
        to GAME_HEIGHT, then the ball's _vy (y-velocity) attribute
        is negated. If the left point of the ball becomes less than or equal to
        0 or the right point becomes greater than or equal to GAME_WIDTH, then
        the ball's _vx (x velocity) will be negated.
        
        Each call of this method moves the ball one step. To do this, this
        method adds self._vx to the ball's current x-coordinate and self._vy to
        the ball's current y-coordinate."""
        
        assert type(b)==bool
        assert type(c)==bool
        
        top_point= (BALL_DIAMETER/2)+ self.y
        bottom_point=self.y -(BALL_DIAMETER/2)
        right_point = self.x + (BALL_DIAMETER/2)
        left_point = self.x - (BALL_DIAMETER/2)
        
        if top_point >= GAME_HEIGHT or c or b:
            self._vy = -self._vy
              
        if left_point <= 0 or right_point >= GAME_WIDTH:
            self._vx = -self._vx
            
        self.x = self.x + self._vx
        self.y = self.y + self._vy
         
   
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def checkOffScreen(self):
        """Returns: True if the ball has gone off screen. False otherwise."""
        
        top_point= (BALL_DIAMETER/2)+ self.y
        if top_point <= 0:
            return True
        return False

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE