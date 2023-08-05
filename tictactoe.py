"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """

    # Initial board ( matrice 3x3 )
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """

    # If the game is over determine the winner
    #if terminal(board):
        #return utility(board)

    # Count the number of X and O
    x_count = 0
    o_count = 0

    # If the board is equal to the initial state -> X moves(not needed)
    #if initial_state() == board:
        #return X

    # Otherwise count the number of X`s and O`s and determine that way
    for row in board:
        for cell in row:
            if cell == X:
                    x_count += 1
            elif cell == O:
                    o_count += 1
    if x_count <= o_count:
        return X
    else:
        return O

    # Implementation v 2 with indexing
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == X:
                x_count = 0
            if board[row][col] == Y:
                y_count = 0
    if x_count <= o_count:
        return X
    else:
        return O



    """
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    # If the game is over determine the winner
    #if terminal(board):
        #return utility(board)

    action_set = set()

    # Go through the board and determine legal moves, add them to the set
    for r_n, i in enumerate(board):
        for c_n, j in enumerate(i):
            if j==EMPTY:
                action_set.add((r_n, c_n))

    return action_set

    # Implementation v2 with indexing
    """
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                action.set.add(row, col)
    """

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    import copy

    # Only valid actions are allowed
    if action not in actions(board):
        raise Exception("Invalid move")

    # Creates a deepcopy (also copies nested objects, rather then just refrencing them in the original object like copy does)
    deep_Cboard = copy.deepcopy(board)

    # Unpacking the (i, j) tuple
    i, j = action

    # Adding an 'X' or 'O' to the specified cell depending on whos turn is it
    deep_Cboard[i][j] = player(board)

    # Returning the new board state after the move
    return deep_Cboard


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check for X and O
    if check_row(board, X) or check_col(board, X) or check_diag1(board, X) or check_diag2(board, X):
        return X
    elif check_row(board, O) or check_col(board, O) or check_diag1(board, O) or check_diag2(board, O):
        return O
    else:
        return None

# Manaul checking
######################################################################################################
# Check if there are three of the same symbols in any row (Returns True if statment true)
def check_row(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    return False

# Check if there are three of the same symbols in any col (Returns True if statment true)
def check_col(board, player):
    for col in range(len(board[0])):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True
    return False

# Check if there are three of the same symbols in diag 1 -> \ (Returns True if statment true)
def check_diag1(board, player):
    count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if row == col and board[row][col] == player:
                count += 1
    if count == 3:
        return True
    return False

# Check if there are three of the same symbols in diag 2 -> / (Returns True if statment true)
def check_diag2(board, player):
    count = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if (len(board) - row - 1 ) == col and board[row][col] == player:
                count += 1
    if count == 3:
        return True
    return False
############################################################################################

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board):
        return True

    # If there is no winner and there is an empty cell -> game continues
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False

    # If there are no more possible actions
    """
    if not actions(board):
        return False

    """

    # Otherwise if all the cells are not-EMPTY -> game is over
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # Returns X, O or None depending on if X or O won or if there is no winner for multiple reasons
    val = winner(board)
    if val == X:
        return 1
    elif val == O:
        return -1
    else:
        return 0

# Minimax funtion is only called when its the AI`s turn !!!
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If the state of the board is terminal return None
    if terminal(board):
        return None
    import random
    # Return a random element from the non-empty sequence seq. If seq is empty, raises IndexError.
    # random.choice(seq) /./

    # Force the bots first move to be one of the corners
    if board == initial_state():
        return random.choice([(0, 0), (0, 2), (2, 0), (2, 2)])

    # If its X`s turn try to maximaze the value
    if player(board) == X:
        best_action = []
        for action in actions(board):
            # Create a list of all min_value, action pairs so that later i can look for the biggest value as the best move
            best_action.append([min_value(result(board,action)), action])
        return sorted(best_action, key=lambda list: list[0], reverse=True)[0][1]
        # Reverse because i want from highes value to lowest
        # [0][1] will take the action that corresponds to the highes value in my list of [[min_value, (action)]]

    # If its O`s turn try to minimize the value
    elif player(board) == O:
        best_action = []
        for action in actions(board):
            # Create a list of all max_value, action pairs so that later i can look for the lowest value as the best move
            best_action.append([max_value(result(board,action)), action])
        return sorted(best_action, key=lambda list: list[0])[0][1]
        # I dont do list[0][0] because list is just a list not a list[list]
        # Because of the lambda funtion the list variable is initialized to an element of best_action
        # which is a list and thats why i dont need to do [0][0]

def max_value(state):

    # Base case
    if terminal(state):
        return utility(state)

    # v = -inf
    v = -math.inf

    # Recursive step, check all available actions in that board state
    for action in actions(state):
        # ! Max takes in two arguments
        v = max(v, min_value(result(state, action)))
    return v

def min_value(state):

    # Base case
    if terminal(state):
        return utility(state)

    # v = inf
    v = math.inf

    # Recursive step, check all available actions in that board state
    for action in actions(state):
        v = min(v, max_value(result(state, action)))
    return v



"""
# If its O`s turn try to minimize the value
    elif player(board) == O:
        best_action = []
        for action in actions(board):
            val = min_value(result(board, action))
            if val < v:
                v = val
                best_action = action
        return best_action

Semi-working version but AI doesnt make optimal moves 100% of the time

"""

"""
If you use sorted on best_action with the key parameter and the lambda function,
the lambda function will be applied to each element of best_action,


LAMBDA FUNC IS APPLIED TO THE INDIVIDUAL ELEMENTS
"""