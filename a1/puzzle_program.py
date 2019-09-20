"""Where's That Word? main program."""

from typing import List, TextIO
from puzzle_functions import FORWARD, BACKWARD, UP, DOWN
import puzzle_functions

DIRECTIONS = (FORWARD, BACKWARD, UP, DOWN)

def get_num_rows(puzzle: str) -> int:
    """Return the number of rows in puzzle.

    puzzle is a game board.

    >>> get_num_rows('abcd\nefgh\nijkl\n')
    3
    """

    return puzzle.count('\n')


def get_num_cols(puzzle: str) -> int:
    """Return the number of columns in puzzle.

    puzzle is a game board.

    >>> get_num_cols('abcd\nefgh\nijkl\n')
    4

    """

    return puzzle.index('\n')


def print_puzzle(puzzle: str) -> None:
    """Print the puzzle with row and column numbers and two spaces between
    each letter.

    """

    # Split puzzle into rows and get dimensions.
    puzzle_rows = puzzle.strip().split('\n')
    num_rows = get_num_rows(puzzle)
    num_columns = get_num_cols(puzzle)

    # Print the column headings.
    print('   ', end='')
    for col_number in range(num_columns):
        print(col_number, ' ', end='')

    print()

    # Print each row number and row.
    for row_number in range(num_rows):
        print(row_number, end='  ')
        print('  '.join(puzzle_rows[row_number]))

    print()


def print_words(words: List[str]) -> None:
    """Print the items from words.

    """

    for word in words:
        print(word, end=' ')
    print('\n')


def get_guess(current_player_name: str, remaining_words:
              List[str]) -> str:
    """Keep prompting user current_player_name for a guess. If user inputs
    a valid guess (it is in remaining_words), return it.

    """

    guess = None
    print(current_player_name + "'s turn")
    while guess not in remaining_words:
        guess = input(current_player_name + ', please enter a word: ').strip()
    return guess


def get_direction(current_player_name: str) -> str:
    """Keep prompting user current_player_name for direction. If user
    inputs a valid direction (it is in DIRECTIONS), return it.

    """

    direction = None
    while direction not in DIRECTIONS:
        direction = input(current_player_name + ', enter the direction (' \
            + ', '.join(DIRECTIONS) + '): ')
    return direction


def get_row_or_col_num(is_row: bool, upper_bound: int, guess: str) -> int:
    """Keep prompting user for row/column where guess occurs. If user
    inputs a valid row/column number (it is a number between 0 and
    upper_bound), return it.

    """

    if is_row:
        row_or_col = 'row'
    else:
        row_or_col = 'column'
    row_or_col_num_str = ''

    while (not row_or_col_num_str.isnumeric() or
           int(row_or_col_num_str) not in range(upper_bound)):
        row_or_col_num_str = input('enter the ' + row_or_col +
                                   ' number where ' + guess + ' occurs: ')
    return int(row_or_col_num_str)


def take_turn(puzzle: str, remaining_words: List[str],
              current_player_name: str) -> int:
    """Prompt the current player to make a guess, and then return the
    number of occurrences of that word in the puzzle. If the guess
    isn't in the list of remaining words, then return 0.  Remove the
    guess from the list of remaining words.

    """

    guess = get_guess(current_player_name, remaining_words)

    direction = get_direction(current_player_name)

    is_row = True

    # Decide whether we should ask for a row or a column number and
    # calculate the upper bound on that number.
    if direction == puzzle_functions.UP or direction == puzzle_functions.DOWN:
        upper_bound = get_num_cols(puzzle)
        is_row = False
    elif (direction == puzzle_functions.FORWARD or
          direction == puzzle_functions.BACKWARD):
        upper_bound = get_num_rows(puzzle)

    row_or_col_num = get_row_or_col_num(is_row, upper_bound, guess)

    num_words_left = len(remaining_words)

    points = puzzle_functions.check_guess(puzzle, direction, guess,
                                          row_or_col_num, num_words_left)

    if points != 0:
        remaining_words.remove(guess)

    return points


def game_over(remaining_words: List[str]) -> bool:
    """Return True iff remaining_words is empty.

    >>> game_over(['dan', 'paul'])
    False
    >>> game_over([])
    True
    """

    return remaining_words == []


def get_puzzle_words(puzzle_file: TextIO) -> List[str]:
    """Return the puzzle words in puzzle_file. These are the words in the
    first line of the file.
    """

    return puzzle_file.readline().strip().split(",")


def read_puzzle(puzzle_file: TextIO) -> str:
    """Return the puzzle in puzzle_file.

    Precondition: get_puzzle_words() was called prior to read_puzzle.
    """

    return puzzle_file.read()


def play_game(puzzle: str, remaining_words: List[str]) -> None:
    """Prompt the players to guess words that occur in the puzzle.  Print
    the score after each turn.  Print the winner.
    """

    # Whether it's player one's turn. If False, it's player two's turn.
    player_one_turn = True

    # The scores for the two players.
    player_one_score = 0
    player_two_score = 0

    print('''***************************************
**       Where's That Word?          **
***************************************''')

    # Prompt for a guess and add up the points until the game is over.
    while not game_over(remaining_words):

        print_puzzle(puzzle)
        print('the words left to be found: ')
        print_words(remaining_words)

        # Get the name of the player whose turn it is.
        current_player_name = puzzle_functions.get_current_player(
            player_one_turn)

        # Have the player take their turn and get the score.
        points = take_turn(puzzle, remaining_words, current_player_name)

        if (points == 0):
            print("incorrect guess :-(")
        else:
            print("correct guess!!!")

        # Update the score for whoever's turn it is.
        if player_one_turn:
            player_one_score = player_one_score + points
            current_player_score = player_one_score
        else:
            player_two_score = player_two_score + points
            current_player_score = player_two_score

        print(current_player_name + "'s score is " +
              str(current_player_score) + "\n")

        player_one_turn = not player_one_turn

    print('woohoo!!! ', 
          puzzle_functions.get_winner(player_one_score, player_two_score)
          + '!!!')


if __name__ == '__main__':

    puzzle_name = puzzle_functions.PUZZLE_FILE
    game_file = open(puzzle_name)
    game_words = get_puzzle_words(game_file)
    game_puzzle = read_puzzle(game_file)
    game_file.close()

    play_game(game_puzzle, game_words)
