import tictactoe as ttt
X = "X"
O = "O"
EMPTY = None
board = [[X, EMPTY, O],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]]

ttt.player(board)

ttt.result(board, (1, 1))

ttt.minimax(board)