# breakout.py
# Nighat Ansari (na295) and Kati Hsu (kyh24)
# 8 December 2016
#We discussed method ideas from Devki Trivedi

"""Primary module for Breakout application

This module contains the main controller class for the Breakout application.
There is no need for any any need for additional classes in this module.  If you
need more classes, 99% of the time they belong in either the play module or the
models module. If you are ensure about where a new class should go, post a
question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for
    processing the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED,
                STATE_ACTIVE]:
                the current state of the game represented a value from
                constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle,
                ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                  the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if _state is STATE_ACTIVE or
                  STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for
    the method update().
    
    You may have more attributes if you wish (you might need an attribute to
    store any text messages you display on the screen). If you add new
    attributes, they need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        
        _incr   [int]: Number of keys pressed
        _time   [int]: Time since last update

    """
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the game
        is running. You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _mssg) saying that the user should press
        to play a game."""
          
        self._state= STATE_INACTIVE
        self._game = None
        self._mssg = GLabel(text="Press any key to play.", x=GAME_WIDTH/2,\
                            y=GAME_HEIGHT/2) \
        if self._state == STATE_INACTIVE else None
        self._incr=0
        self._last  = None
          
     
    def update(self,dt):
        """Animates a single frame in the game.
        
            It is the method that does most of the work. It is NOT in charge of
            playing the game.  That is the purpose of the class Play.The primary
            purpose of this game is to determine the current state, and -if the
            game is active - pass the input to the Play object _game to play the
            game.
            
            As part of the assignment, you are allowed to add your own states.
            However, at a minimum you must support the following states:
            STATE_INACTIVE, STATE_NEWGAME, STATE_COUNTDOWN, STATE_PAUSED, and
            STATE_ACTIVE.  Each one of these does its own thing, and so should 
            have its own helper.  We describe these below.
            
            STATE_INACTIVE: This is the state when the application first opens.
            is a paused state, waiting for the player to start the game.  It
            It displays a simple message on the screen.
            
            STATE_NEWGAME: This is the state creates a new game and shows it on 
            the screen. This state only lasts one animation frame before
            switching to STATE_COUNTDOWN.
            
            STATE_COUNTDOWN: This is a 3 second countdown that lasts until the
            ball is served.  The player can move the paddle during the countdown
            , but there is no ball on the screen.  Paddle movement is handled by
            the Play object.  Hence the Play class should have a method called
            updatePaddle()
            
            STATE_ACTIVE: This is a session of normal gameplay.  The player can
            move the paddle and the ball moves on its own about the board.  Both
            of these should be handled by methods inside of class Play (NOT in
            this class). Hence the Play class should have methods named
            updatePaddle() and updateBall().
            
            STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
            the game is still visible on the screen.
            
            The rules for determining the current state are as follows.
            
            STATE_INACTIVE: This is the state at the beginning, and is the state 
            as long as the player never presses a key. In addition, the
            application switches to this state if the previous state was
            STATE_ACTIVE and the game is over 
            (e.g. all balls are lost or no more bricks are on the screen).
            
            STATE_NEWGAME: The application switches to this state if the state
            was STATE_INACTIVE in the previous frame, and the player pressed a
            key.
            
            STATE_COUNTDOWN: The application switches to this state if the state
            was STATE_NEWGAME in the previous frame (so that state only lasts
            one frame)
            
            STATE_ACTIVE: The application switches to this state after it has
            spent 3 seconds in the state STATE_COUNTDOWN.
            
            STATE_PAUSED: The application switches to this state if the state was 
            STATE_ACTIVE in the previous frame, the ball was lost, and there are
            still some tries remaining.
            
            STATE_LOSER: The application switches to this state when the player
            loses all of his lives before removing all of the bricks.
            
            STATE_WINNER: The application switches to this state when the player
            successfully removes all of the bricks before losing all lives.
            
            You are allowed to add more states if you wish. Should you do so, you
            should describe them here.
            Parameter dt: The time in seconds since last update
            Precondition: dt is a number (int or float)
        """
        #Assert preconditions
        assert type(dt) in [int, float]
        
        self.determine_state()
        
        if self._state==STATE_INACTIVE:
            self.stateInactive()
            
        if self._state==STATE_NEWGAME:
            self.stateNewGame()
            
        if self._state==STATE_COUNTDOWN:
            self.stateCountdown()
            
        if self._state==STATE_ACTIVE:
            self.stateActive()
            
        if self._state==STATE_PAUSED:
            self.paused_det_state()
            
        if self._state == STATE_LOSER:
            self.stateLoser()
        
        if self._state == STATE_WINNER:
            self.stateWinner()
    
    
    def draw(self):
        """Draws the game objects to the view.
        
            Every single thing you want to draw in this game is a GObject.  To
            draw a GObject g, simply use the method g.draw(self.view).  It is
            that easy!
            
            Many of the GObjects (such as the paddle, ball, and bricks) are
            attributes in Play. In order to draw them, you either need to add
            getters for these attributes or you need to add a draw method to
            class Play. We suggest the latter. See the example subcontroller.py
            from class."""
        
        # IMPLEMENT ME
        if self._mssg is not None:
            self._mssg.draw(self.view) #Draws message
               
        if self._state==STATE_ACTIVE or self._state==STATE_COUNTDOWN:
            if self._mssg is not None:
                self._mssg.draw(self.view) 
            self._game.playDraw(self.view) #Draws game
            
       
    # HELPER METHODS FOR THE STATES GO HERE
    def determine_state(self):
        """Determines the current state and assigns it to self._state.
        
            This method checks for a key press, and if there is one, changes the
            state from STATE_INACTIVE to STATE_NEWGAME.  A key press is when a
            key is pressed for the FIRST TIME.
            We do not want the state to continue to change as we hold down the
            key.
            The user must release the key and press it again to change the state
            """
            
        # Updates state
        keys_pressed=self.input.key_count
        if self._incr==0:
            if keys_pressed > 0:
                self._state = (self._state + 1) % 5
                self._incr = self._incr + 1
     
    def stateInactive(self):
        """Displays welcome message and assigns None to self._game.
        
            This method is called when self._state = STATE_INACTIVE."""
        
        self._mssg = GLabel(text="Press any key to play", x=GAME_WIDTH/2,\
                            y=GAME_HEIGHT/2)
        self._game = None
    
    def stateNewGame(self):
        """Initializes _time attribute to 0 and creates a new Play object (a new
            game) and assigns it to self._game. Once these two steps are done,
            this method changes self._state to STATE_COUNTDOWN.
               
            This method is called when self._state = STATE_NEWGAME, after a key
            press is detected when self._state = STATE_INACTIVE."""
            
        self._time=0
        self._game=Play()
        self._state= STATE_COUNTDOWN
    
    def stateCountdown(self):
        """Calls updatePaddle method in class Play and countdown helper method
            in Breakout.
               
            This method allows movement of the paddle as the countdown starts to
            begin a new game."""
        
        self._game.updatePaddle(self.input)
        self.countdown()
    
    def stateActive(self):
        """Calls updatePaddle and updateBall methods in class Play.
        
           This method is called when self._state = STATE_ACTIVE and the game is
           ongoing.The state remains STATE_ACTIVE until the ball goes offscreen.
           If the ball goes offscreen, self._state changes to STATE_PAUSED."""
        
        self._game.updatePaddle(self.input)
        self._game.updateBall()
        if len(self._game.getBricks()) == 0 and self._game.getTries() > 0:
            self._state = STATE_WINNER
        if self._game._offScreen:
            self._state = STATE_PAUSED
    
    def paused_det_state(self):
        """Changes state based on the number of tries left.
        
           This method first checks to see if the player has any tries/lives
           left. If not, this method reassigns self._state to STATE_COMPLETE. If
           the player does have tries left, a message will display telling the
           player how many lives he/she has left. After this message is
           displayed, this method checks for a key press. If a key press is
           detected, self._state is reassigned to STATE_COUNTDOWN and _time
           attribute reinitialized to 0 to start the countdown to begin a new
           game."""
           
        if self._game.getTries() == 1 and len(self._game.getBricks()) > 0:
            self._state = STATE_LOSER
        else:
            if self._game.getTries() == 2:
                self._mssg= GLabel(text="Press any key to play." + \
                           str(self._game.getTries()-1) + " try left", \
                                    x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
            else:
                self._mssg= GLabel(text="Press any key to play. " + \
                           str(self._game.getTries()-1) + " tries left", \
                                   x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
            
            keys_pressed = self._input.key_count
            if keys_pressed >0:
                self._game.setTries(self._game.getTries()-1)
                newTries = self._game.getTries()
                if self._game.getTries()>0:
                    self._mssg= GLabel(text='',x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
                    self._time = 0
                    self._state= STATE_COUNTDOWN
    
    def stateLoser(self):
        """Displays a message when player loses the game."""
        self._mssg = GLabel(text="LOSERRRRR", x=GAME_WIDTH/2,\
                                    y=GAME_HEIGHT/2)
    
    def stateWinner(self):
        """Displays a message when player wins the game."""
        self._mssg = GLabel(text="WINNERRRR", x=GAME_WIDTH/2,\
                                    y=GAME_HEIGHT/2)
        
    def countdown(self):
        """Displays countdown on screen when transitioning from STATE_NEWGAME to
            STATE_COUNTDOWN.
            
            This method updates the _time attribute, which
            keeps track of the number of animation frames passed. Because
            Breakout is designed to run at 60 frames a second, one second =
            60 frames.
            Therefore, for every increase in 60 for self._time, one second has
            passed and the countdown will display the number of seconds left
            until the game begins. Once 3 seconds are up, the game state changes
            to STATE_ACTIVE."""
        
        if self._time == 0:
            self._mssg = GLabel(text='3', x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
            
        if self._time == 60:
            self._mssg = GLabel(text='2', x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
           
        if self._time == 120:
            self._mssg = GLabel(text='1', x=GAME_WIDTH/2, y=GAME_HEIGHT/2)
        
        self._time += 1
        
        if self._time == 180:
            self._mssg = GLabel(text=' ', x=GAME_WIDTH/2, y=GAME_HEIGHT/2,
                                linecolor = colormodel.WHITE, \
                                            fillcolor = colormodel.WHITE)
            self._game.makeBall()
            self._state = STATE_ACTIVE
           
        