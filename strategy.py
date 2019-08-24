import Othello_Core as core
from random import *
import time

class Strategy(core.OthelloCore):
    player = core.BLACK
    SQUARE_WEIGHTS = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1200, -2000, 20, 5, 5, 20, -2000, 1200, 0,
    0, -2000, -4000, -5, -5, -5, -5, -4000, -2000, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 5, -5, 3, 3, 3, 3, -5, 5, 0,
    0, 20, -5, 15, 3, 3, 15, -5, 20, 0,
    0, -2000, -4000, -5, -5, -5, -5, -4000, -2000, 0,
    0, 1200, -2000, 20, 5, 5, 20, -2000, 1200, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    ]

    def __init__(self):
        self.count = 0
        
    def squares(self):
        """List all the valid squares on the board."""
        return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

    def initial_board(self):
        """Create a new board with the initial black and white positions filled."""
        board = [core.OUTER] * 100
        for i in self.squares():
            board[i] = core.EMPTY
        # The middle four squares should hold the initial piece positions.
        board[44], board[45] = core.WHITE, core.BLACK
        board[54], board[55] = core.BLACK, core.WHITE
        return board


    def print_board(self,board):
        """Get a string representation of the board."""
        rep = ''
        rep += '  %s\n' % ' '.join(map(str, list(range(1, 9))))
        for row in range(1, 9):
            begin, end = 10 * row + 1, 10 * row + 9
            rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
        return rep
    
    def is_valid(self, move):
        """Is move a square on the board?"""
        if int(move) == move and move in self.squares():
            return True
        else:
            return False
        #return isinstance(move, int) and move in squares()
        

    def opponent(self, player):
        """Get player's opponent piece."""
        if player == core.BLACK:
            return core.WHITE
        else:
            return core.BLACK

    def find_bracket(self, square, player, board, direction):
        """
        Find a square that forms a bracket with `square` for `player` in the given
        `direction`.  Returns None if no such square exists.
        Returns the index of the bracketing square if found
        """
        nextSquare = square + direction
        if board[nextSquare] == player:
            return None
        opp = self.opponent(player)
        while board[nextSquare] == opp:
            nextSquare += direction
        if board[nextSquare] == core.OUTER or board[nextSquare] == core.EMPTY:
            return None
        else:
            return nextSquare
        #return None if board[nextSquare] in (core.OUTER, core.EMPTY) else nextSquare

    def is_legal(self, move, player, board):
        """Is this a legal move for the player?"""
        is_legal=False
        if (self.is_valid(move)):
            if (board[move]!='.'):
                return False
            for x in core.DIRECTIONS:
                if (not self.find_bracket(move,player,board,x)==None):
                    is_legal=True
            return is_legal
        return False
    ### Making moves

    # When the player makes a move, we need to update the board and flip all the
    # bracketed pieces.

    def make_move(self, move, player, board):
        """Update the board to reflect the move by the specified player."""
        for x in core.DIRECTIONS:
            self.make_flips(move,player, board, x)
        board[move] = player

        return board

    def make_flips(self, move, player, board, direction):
        """Flip pieces in the given direction as a result of the move by player."""
        bracket = self.find_bracket(move, player, board, direction)
        if bracket != None:
            square = move + direction
            while square != bracket:
                board[square] = player
                square += direction

    def legal_moves(self, player, board):
        """Get a list of all legal moves for player, as a list of integers"""
        legal_list = []
        for x in (self.squares()):
            if(self.is_legal(x, player, board)):
                legal_list.append(x)
        #print(legal_list)
        return legal_list
        #return [sq for sq in self.squares() if self.is_legal(sq, player, board)]

    def any_legal_move(self, player, board):
        """Can player make any moves? Returns a boolean"""
##        if len(self.legal_moves(player,board)) > 0:
##            return True
##        return False
        return any(self.is_legal(sq, player, board) for sq in self.squares())
    
    def next_player(self,board, prev_player):
        """Which player should move next?  Returns None if no legal moves exist."""
        if self.any_legal_move(self.opponent(prev_player), board):
            return self.opponent(prev_player)
        elif self.any_legal_move(prev_player, board):
            return prev_player
        else:
            return None
    
    def score(self,player, board):
        """Compute player's score (number of player's pieces minus opponent's)."""
        temp = board.count(core.BLACK) - board.count(core.WHITE)
        for x in range(len(board)):
            if board[x] == core.BLACK:
                temp += self.SQUARE_WEIGHTS[x]
            if board[x] == core.WHITE:
                temp -= self.SQUARE_WEIGHTS[x]
        return temp
    def random_strategy(self, board, player):
        if self.any_legal_move(player,board) == False:
            return None
        else:
            list_of_moves = self.legal_moves(player, board)
            shuffle(list_of_moves)
            move = list_of_moves.pop()
        return move
    def best_strategy(self, board, player, best_shared, still_running):
        start_depth = 6
        while(still_running.value > 0):
            best_shared.value = self.minimax_strategy(board,player,start_depth)
            start_depth += 2
        
    """
    :param board: a length 100 list representing the board state
    :param player: WHITE or BLACK
    :param best_move: shared multiptocessing.Value containing an int of
            the current best move
    :param still_running: shared multiprocessing.Value containing an int
            that is 0 iff the parent process intends to kill this process
    :return: best move as an int in [11,88] or possibly 0 for 'unknown'"""

    def minimax_strategy(self, board, player, max_depth):
        """ Takes a current board and player and max_depth and returns a best move
         This is the top level mini-max function. Note depth is ignored. We
         always search to the end of the game."""
        if len(self.legal_moves(player, board)) == 0:
            move = self.legal_moves(player, baord).pop()
            return move
        if player == core.BLACK:
            move = self.max_dfs(board, player, max_depth, 0, -10**9,10**9)[1]
        if player == core.WHITE:
            move = self.min_dfs(board, player, max_depth, 0,-10**9,10**9)[1]
        #print("the move",move)
        return move
     
    def max_dfs(self,board, player, max_depth, depth, alpha, beta):
        self.count += 1
        if depth >= max_depth:
            return self.score(player,board), None
        if not self.any_legal_move(player, board):
            score = board.count(core.BLACK) - board.count(core.WHITE)
            if score > 0:
                return 10**8, None
            if score == 0:
                return 0, None
            if score < 0:
                return -(10**8), None
        v = -10**9
        move = -1
        for m in self.legal_moves(player,board):
            new_board = board.copy()
            new_board = self.make_move(m,player,new_board)
            depth = depth + 1
            new_value = self.min_dfs(new_board, self.next_player(new_board,player), max_depth,depth, alpha, beta)[0]
            #print("max", new_value)
            if new_value > v:
                v = new_value
                move = int(m)
            if v >= beta:
                return v, int(move)
            alpha = self.max_dfs(new_board, self.next_player(new_board,player), max_depth,depth,alpha, v)[0]
        return v, int(move)
    
    def min_dfs(self, board, player, max_depth, depth, alpha, beta):
        self.count+=1
        if depth >= max_depth:
            return self.score(player,board),None
        if not self.any_legal_move(player, board) :
            score = board.count(core.BLACK) - board.count(core.WHITE)
            if score > 0:
                return -(10**8), None
            if score == 0:
                return 0, None
            if score < 0:
                return 10**8, None
        v = 10**9
        move = -1
        for m in self.legal_moves(player,board):
            new_board = board.copy()
            new_board = self.make_move(m,player,new_board)
            depth = depth + 1
            new_value = self.max_dfs(new_board, self.next_player(new_board,player), max_depth,depth,alpha, beta)[0]
            #print("min", new_value)
            if new_value < v:
                v = new_value
                move = m
            if v <= alpha:
                return v, int(move)
            beta = self.min_dfs(new_board, self.next_player(new_board,player), max_depth,depth,beta,v)[0]
        return v, int(move)
   
Start_time = time.time()
obj = Strategy()
obj2 = Strategy()
board = obj.initial_board()
print(obj.print_board(board))
while True:
    #temp = obj.random_strategy(obj.player,board)
    temp = obj.minimax_strategy(board, obj.player,5)
    if temp == None:
        break
    else:
        move = temp
        #print(obj.player)
        #print(move)
        board = obj.make_move(move,obj.player,board)
        print(obj.print_board(board))
    obj.player = obj.next_player(board, obj.player)
    if obj.player == None:
        break
#print("score: ",obj.score(obj.player, board))
print(obj.count)
print(time.time()-Start_time)
if(obj.score(obj.player, board) > 0):
    print("Black Wins")
else:
    print("White Wins")







