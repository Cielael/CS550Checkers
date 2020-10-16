'''
@author: mroch
'''

# Game representation and mechanics

# tonto - Professor Roch's not too smart strategy
# You are not given source code to this, but compiled .pyc files
# are available for Python 3.7 and 3.8 (fails otherwise).
# This will let you test some of your game logic without having to worry
# about whether or not your AI is working and let you pit your player
# against another computer player.
#
# Decompilation is cheating, don't do it.
import statistics


# Python can load compiled modules using the imp module (deprecated)
# We'll format the path to the tonto module based on the
# release of Python.  Note that we provided tonto compilations for Python 3.7
# and 3.8.  If you're not using one of these, it won't work.
if True:
    import imp
    import sys
    major = sys.version_info[0]
    minor = sys.version_info[1]
    modpath = "lib/__pycache__/tonto.cpython-{}{}.pyc".format(major, minor)
    tonto = imp.load_compiled("tonto", modpath)


# human - human player, prompts for input    
from lib import human, checkerboard

import ai 

from lib.timer import Timer

# red = human.Strategy
def Game(red=ai.Strategy, black=tonto.Strategy,
         maxplies=6, init=None, verbose=True, firstmove=0):
    """Game(red, black, maxplies, init, verbose, turn)
    Start a game of checkers
    red,black - Strategy classes (not instances)
    maxplies - # of turns to explore (default 10)
    init - Start with given board (default None uses a brand new game)
    verbose - Show messages (default True)
    firstmove - Player N starts 0 (red) or 1 (black).  Default 0. 

    Returns winning player 'r' or 'b'
    """
    # Get ai.Strategy to work
    # Log time to perform action
    # Print board representation if verbose
    # Output to game.txt
    
    with open('game.txt','w') as f:

        redplayer = red('r', checkerboard.CheckerBoard, maxplies)
        blackplayer = black('b', checkerboard.CheckerBoard, maxplies)
        board = checkerboard.CheckerBoard()
        turncount = 0 # track turn number
    
        while not board.is_terminal()[0]:
            f.write('\nTURN: %d ' %(turncount))
            if (turncount % 2) == 0: # even turn
                if verbose:
                    f.write("It is red\'s turn\n")
                # want to time each action
                f.write(str(board)) # turn tuple to string
                board, action = redplayer.play(board)
                f.write(board.get_action_str(action) + '\n')
            else:
                if verbose:
                    f.write("It is black\'s turn\n")
                f.write(str(board)) # turn tuple to string
                board, action = blackplayer.play(board)
                f.write(board.get_action_str(action) + '\n')
            turncount += 1
    
        if board.is_terminal()[0]: # is game over
            winner = board.is_terminal()[1]
            if winner is None:
                f.write("\nGAME IS A DRAW")
            if winner == 'b':
                f.write("\nBLACK WINS")
            else:
                f.write("\nRED WINS") 
    f.close()

if __name__ == "__main__":
    # Examples
    # Starting from specific board with default strategy
    #Game(init=boardlibrary.boards["multihop"])
    #Game(init=boardlibrary.boards["StrategyTest1"])
    #Game(init=boardlibrary.boards["EndGame1"], firstmove = 1)

    # Tonto vs Tonto
    # Game(red=tonto.Strategy, black=tonto.Strategy)

    #Play with default strategies...
    Game()
        
        
        

        
                    
            
        

    
    
