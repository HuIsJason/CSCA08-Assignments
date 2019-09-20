""" Where's That Word? functions. """

# The constant describing the valid directions. These should be used
# in functions get_factor and check_guess.
UP = 'up'
DOWN = 'down'
FORWARD = 'forward'
BACKWARD = 'backward'

# The constants describing the multiplicative factor for finding a
# word in a particular direction.  This should be used in get_factor.
FORWARD_FACTOR = 1
DOWN_FACTOR = 2
BACKWARD_FACTOR = 3
UP_FACTOR = 4

# The constant describing the threshold for scoring. This should be
# used in get_points.
THRESHOLD = 5
BONUS = 12

# The constants describing two players and the result of the
# game. These should be used as return values in get_current_player
# and get_winner.
P1 = 'player one'
P2 = 'player two'
P1_WINS = 'player one wins'
P2_WINS = 'player two wins'
TIE = 'tie game'

# The constant describing which puzzle to play. Replace the 'puzzle1.txt' with
# any other puzzle file (e.g., 'puzzle2.txt') to play a different game.
PUZZLE_FILE = 'puzzle2.txt'


# Helper functions.  Do not modify these, although you are welcome to
# call them.

def get_column(puzzle: str, col_num: int) -> str:
    """Return column col_num of puzzle.

    Precondition: 0 <= col_num < number of columns in puzzle

    >>> get_column('abcd\nefgh\nijkl\n', 1)
    'bfj'
    """

    puzzle_list = puzzle.strip().split('\n')
    column = ''
    for row in puzzle_list:
        column += row[col_num]

    return column


def get_row_length(puzzle: str) -> int:
    """Return the length of a row in puzzle.

    >>> get_row_length('abcd\nefgh\nijkl\n')
    4
    """

    return len(puzzle.split('\n')[0])


def contains(text1: str, text2: str) -> bool:
    """Return whether text2 appears anywhere in text1.

    >>> contains('abc', 'bc')
    True
    >>> contains('abc', 'cb')
    False
    """

    return text2 in text1


# Implement the required functions below.

def get_current_player(player_one_turn: bool) -> str:
    """Return 'player one' iff player_one_turn is True; otherwise return
    'player two'.

    >>> get_current_player(True)
    'player one'
    >>> get_current_player(False)
    'player two'
    """

    if player_one_turn:
        return P1
    else:
        return P2


def get_winner(player_one_score: int, player_two_score: int) -> int:
    """Return 'player one wins' if player_one_score is greater than
    player_two_score, and vice-versa. If they are equivalent, return 'tie game'.
    
    Precaution: player_one_score, player_two_score >= 0
    
    >>> get_winner(10, 12)
    'player two wins'
    >>> get_winner(21, 21)
    'tie game'
    """
    
    if player_one_score > player_two_score:
        return P1_WINS
    elif player_one_score < player_two_score:
        return P2_WINS
    else:
        return TIE


def reverse(reversed_word: str) -> str:
    """Return a reversed copy of the string reversed_word.
    
    >>> reverse('Jason Hu')
    'uH nosaJ'
    >>> reverse('Kaveh')
    'hevaK'
    """
    
    return reversed_word[::-1]


def get_row(puzzle: str, row_num: int) -> str:
    """Return the characters in row row_num of puzzle.
    
    Precondition: 0 <= row_num < get_row_length(puzzle)
    
    >>> get_row('abcd\nefgh\nijkl\n', 2)
    'ijkl'
    >>> get_row('abcd\nefgh\nijkl\n', 0)
    'abcd'
    """
    
    first_index = get_row_length(puzzle) * row_num + row_num
    last_index = get_row_length(puzzle) * row_num + row_num + \
    get_row_length(puzzle)
    
    return puzzle[first_index:last_index]


def get_factor(direction: str) -> str:
    """Return multiplicative factor associated with direction.
    
    >>> get_factor('down')
    '2'
    >>> get_factor('up')
    '4'
    """
    
    if direction == UP:
        return UP_FACTOR
    elif direction == DOWN:
        return DOWN_FACTOR
    elif direction == FORWARD:
        return FORWARD_FACTOR
    return BACKWARD_FACTOR
  
 
def get_points(direction: str, words_left: int) -> int:
    """Return number of points earned if a word is found in a certain direction.
    
    Precondition: 0 < words_left
    
    >>> get_points('forward', 5)
    5
    >>> get_points('down', 3)
    14
    """
    
    if words_left >= THRESHOLD:
        return THRESHOLD * get_factor(direction)
    elif 1 < words_left < THRESHOLD:
        return (2 * THRESHOLD - words_left) * get_factor(direction)
    return (2 * THRESHOLD - words_left) * get_factor(direction) + BONUS


def check_guess(puzzle: str, direction: str, guessed_word: str, \
                row_col_num: int, words_left: int) -> int:
    """Return number of points earned if there are words_left words left and \
    guessed_word is found in row/column row_col_num of puzzle in given \
    direction. Otherwise, return 0.
    
    Precondition: 0 <= rowcol_num, 0 < words_left
    
    >>> check_guess('abcd\nefgh\nijkl\n', 'forward', 'efg', 1, 5)
    5
    >>> check_guess('abcd\nefgh\nijkl\n', 'backward', 'cba', 0, 1)
    39
    """
        
    if contains(reverse(get_column(puzzle, row_col_num)), guessed_word) \
       or contains(get_column(puzzle, row_col_num), guessed_word) \
       or contains(reverse(get_row(puzzle, row_col_num)), guessed_word) \
       or contains(get_row(puzzle, row_col_num), guessed_word):
        return get_points(direction, words_left)
    return 0