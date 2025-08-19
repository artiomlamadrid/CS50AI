"""
Tic Tac Toe Player
"""

import math, copy, random

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    sum_x = sum(row.count(X) for row in board)
    sum_o = sum(row.count(O) for row in board)
    
    if sum_x > sum_o:
        return O
    else:
        return X



def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for row in range(3):
        for column in range(3):
            if board[row][column] == EMPTY:
                actions.add((row, column))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # check out of bounds
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2:
        raise ValueError("Invalid action")
    
    # check if cell is already played
    if board[action[0]][action[1]] != EMPTY:
        raise ValueError("Cell is already played")

    current_player = player(board)
    
    row = action[0]
    column = action[1]

    new_board = copy.deepcopy(board)
    new_board[row][column] = current_player

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    # check columns
    for column in range(3):
            if board[0][column] == board[1][column] == board[2][column] != EMPTY:
                return board[0][column]
            
    # check diagonals
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    # check if there is a winner
    if winner(board) is not None:
        return True

    # check for empty spaces
    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # check if the game is over
    if terminal(board):
        return None

    # define current player
    current_player = player(board)

    # If current player is X
    if current_player == X:

        # start with lowest possible value, any value higher than -inf is better
        best_score = -math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = min_score(new_board)
            if score > best_score:
                best_score = score
                best_action = action
        return best_action

    else:  # current_player == O

        # start with highest possible value, any value lower than +inf is better
        best_score = math.inf
        best_action = None
        for action in actions(board):
            new_board = result(board, action)
            score = max_score(new_board)
            if score < best_score:
                best_score = score
                best_action = action
        return best_action


def max_score(board):
    """Helper function that returns the maximum utility value for X"""
    if terminal(board):
        return utility(board)
    
    score = -math.inf
    for action in actions(board):
        new_board = result(board, action)
        score = max(score, min_score(new_board))
    return score


def min_score(board):
    """Helper function that returns the minimum utility value for O"""
    if terminal(board):
        return utility(board)
    
    score = math.inf
    for action in actions(board):
        new_board = result(board, action)
        score = min(score, max_score(new_board))
    return score