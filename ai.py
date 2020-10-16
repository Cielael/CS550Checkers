from lib import abstractstrategy, boardlibrary, checkerboard


class AlphaBetaSearch:
    
    def __init__(self, strategy, maxplayer, minplayer, maxplies=3, 
                 verbose=False):
        """"alphabeta_search - Initialize a class capable of alphabeta search
        problem - problem representation
        maxplayer - name of player that will maximize the utility function
        minplayer - name of player that will minimize the uitlity function
        maxplies- Maximum ply depth to search
        verbose - Output debugging information
        """
        self.strategy = strategy
        self.maxplayer = maxplayer
        self.minplayer = minplayer
        self.maxplies = maxplies
        self.verbose = verbose

    def alphabeta(self, state):
        """
        Conduct an alpha beta pruning search from state
        :param state: Instance of the game representation
        :return: best action for maxplayer
        """
        # maxvalue returns tuple w/ value[0] and action[1]
        return self.maxvalue(state, alpha = -1e6, beta = 1e6, ply = 0)[1]

    def cutoff(self, state, ply):
        """
        cutoff_test - Should the search stop?
        :param state: current game state
        :param ply: current ply (depth) in search tree
        :return: True if search is to be stopped (terminal state or cutoff
           condition reached)
        """
        # check with is_terminal(state)
        if state.is_terminal()[0] or ply == self.maxplies:
            return True
        return False

    def maxvalue(self, state, alpha, beta, ply):
        """
        maxvalue - - alpha/beta search from a maximum node
        Find the best possible move knowing that the next move will try to
        minimize utility.
        :param state: current state
        :param alpha: lower bound of best move max player can make
        :param beta: upper bound of best move max player can make
        :param ply: current search depth
        :return: (value, maxaction)
        """
        maxaction = None # prevents reference error
        if self.cutoff(state, ply): # when ply = 0 it steps into (BUG!)
            v = self.strategy.evaluate(state) # get utility
        else:
            v = -1e6
            actions = state.get_actions(self.maxplayer)
            for action in actions:
                # take minvalue of action and increase the search depth
                v = max(v, self.minvalue(state.move(action), alpha, beta, ply+1)[0])
                maxaction = action # unsure
                if v >= beta:
                    break # prune
                else:
                    alpha = max(alpha, v)
        return v, maxaction
                    
    def minvalue(self, state, alpha, beta, ply):
        """
        minvalue - alpha/beta search from a minimum node
        :param state: current state
        :param alpha:  lower bound on best move for min player
        :param beta:  upper bound on best move for max player
        :param ply: current depth
        :return: (v, minaction)  Value of min action and the action that
           produced it.
        """
        minaction = None # prefents reference error
        if self.cutoff(state, ply):
            v = self.strategy.evaluate(state) # get utility
        else:
            v = 1e6
            actions = state.get_actions(self.maxplayer)
            for action in actions:
                # take maxvalue of action and increase the search depth
                v = min(v, self.maxvalue(state.move(action), alpha, beta, ply+1)[0])
                minaction = action # unsure
                if v <= alpha:
                    break # prune
                else:
                    beta = min(beta, v)
        return v, minaction

class Strategy(abstractstrategy.Strategy):
    """Your strategy, maybe you can beat Tamara Tansykkuzhina, 
       2019 World Women's Champion
    """

    def __init__(self, *args):
        """
        Strategy - Concrete implementation of abstractstrategy.Strategy
        See abstractstrategy.Strategy for parameters
       """
        
        super(Strategy, self).__init__(*args)
        
        self.search = \
            AlphaBetaSearch(self, self.maxplayer, self.minplayer,
                                   maxplies=self.maxplies, verbose=False)
     
    def play(self, board):
        """
        play(board) - Find best move on current board for the maxplayer
        Returns (newboard, action)
        """
        action = self.search.alphabeta(board) # best possible action
        return board.move(action), action
    
    def evaluate(self, state, turn = None):
        """
        evaluate - Determine utility of terminal state or estimated
        utility of a non-terminal state
        :param state: Game state
        :param turn: Optional turn (None to omit)
        :return:  utility or utility estimate based on strengh of board
                  (bigger numbers for max player, smaller numbers for
                   min player)
        """

        utility = self.piececount(state)
        # check if can prevent capture (double up pieces)
        utility += self.buddy(state)
        utility += self.kingme(state)
        return utility
 
    def piececount(self, state):
        """
        piececount - Get total amount of pawns and kings on the board
        with respect to each player
        :param state: Game state
        :return: total difference of pawns and kings (bias towards kings)
        """
        # subtract pawns of minplayer from maxplayer
        pawncount = state.get_pawnsN()[state.playeridx(self.maxplayer)] - \
                state.get_pawnsN()[state.playeridx(self.minplayer)]
        # subtract kings of minplayer from maxplayer
        kingcount = state.get_kingsN()[state.playeridx(self.maxplayer)] - \
                state.get_kingsN()[state.playeridx(self.minplayer)]
        return pawncount + (3 * kingcount)

    def kingme(self, state):
        """
        kingme - Determine which pieces are closer to becoming a king
        :param state: Game state
        :return: integer that represents making king (larger is better)
        """
        utility = 0
        for row, col, piece in state:
            (player, king) = state.identifypiece(piece)
            if not king:
                # current piece is maxplayer
                if player is state.playeridx(self.maxplayer):
                    # larger distance to king is better in alg (fix)
                    utility += state.disttoking(piece, row)
                # current piece is minplayer
                else:
                    utility -= state.disttoking(piece, row)
        return utility

    def buddy(self, state):
        """
        buddy - Tell if pieces are next to each other (defensive)
        :param state: Game state
        :return: number of pieces next to each other
        """
        # check piece location
        # check diagonals
        return 0

# Run test cases if invoked as main module
if __name__ == "__main__":
    b = boardlibrary.boards["StrategyTest1"]
    redstrat = Strategy('r', b, 6)
    blackstrat = Strategy('b', b, 6)
    
    print(b)
    (nb, action) = redstrat.play(b)
    print("Red would select ", action)
    print(nb)
    
    
    (nb, action) = blackstrat.play(b)
    print("Black would select ", action)
    print(nb)
    
 

