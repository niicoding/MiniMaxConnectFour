import copy
import time
import abc
import random

class Game(object):
    """A connect four game."""

    def __init__(self, grid):
        """Instances differ by their board."""
        self.grid = copy.deepcopy(grid)  # No aliasing!

    def display(self):
        """Print the game board."""
        for row in self.grid:
            for mark in row:
                print(mark, end='')
            print()
        print()

    def possible_moves(self):
        """Return a list of possible moves given the current board."""
        moves = []
        index = 0
        for i in self.grid[0]:
            if i == '-':
                moves.append(index)
            index = index + 1

        return moves

    def neighbor(self, column, color):
        """Return a Game instance like this one but with a move made into the specified column."""
        # YOU FILL THIS IN

        game = Game([['-' for i in range(8)] for j in range(8)])
        set_move = False

        for row in range(8):
            for col in range(8):
                current_icon = self.grid[row][col]
                next_icon = game.grid[row][col]
                if current_icon != next_icon:
                    game.grid[row][col] = current_icon
                if col == column and game.grid[row][col] != '-' and set_move is False:
                    game.grid[row - 1][col] = color
                    set_move = True
                if row == 7 and col == column and set_move is False:
                    game.grid[row][col] = color
                    set_move = True

        return game

    def utility(self):
        """Return the minimax utility value of this game"""
        # YOU FILL THIS IN

    def winning_state(self):
        """Returns float("inf") if Red wins; float("-inf") if Black wins;
           0 if board full; None if not full and no winner"""
        black = 0
        red = 0

        # Check for horizontal win
        for row in self.grid:
            red = 0
            black = 0
            for mark in row:
                if mark == 'R':
                    black = 0
                    red = red + 1
                    if red == 4:
                        return float("inf")
                if mark == 'B':
                    red = 0
                    black = black + 1
                    if black == 4:
                        return float("-inf")

        i = 0
        j = 0
        black = 0
        red = 0
        # Check for vertical win
        for row in range(8):
            red = 0
            black = 0
            for column in range(8):
                if self.grid[column][row] == 'R':
                    black = 0
                    red = red + 1
                    if red == 4:
                        return float("inf")
                if self.grid[column][row] == 'B':
                    red = 0
                    black = black + 1
                    if black == 4:
                        return float("-inf")

        #go diagionally

        diagonal_array = []
        icon = ''
        i = 0
        j = 0
        for row in self.grid:
            i = 0
            j = 0
            if i < 5 and j < 5:
                diagonal_array.append(self.grid[i][j])
                diagonal_array.append(self.grid[i + 1][j + 1])
                diagonal_array.append(self.grid[i + 2][j + 2])
                diagonal_array.append(self.grid[i + 3][j + 3])
            if i > 4 and j > 4:
                diagonal_array.append(self.grid[i][j])
                diagonal_array.append(self.grid[7 - i][7 - j])
                diagonal_array.append(self.grid[6 - i][6 - j])
                diagonal_array.append(self.grid[5 - i][5 - j])
            j = j + 1
            i = i + 1

        r_count = 0
        b_count = 0
        for letter in diagonal_array:
            if letter == 'R':
                b_count = 0
                r_count = r_count + 1
                if r_count == 4:
                    return float('inf')
            if letter == 'B':
                r_count = 0
                b_count = b_count + 1
                if b_count == 4:
                    return float('-inf')

        # To count if board is full
        black = 0
        red = 0
        for row in self.grid:
            for mark in row:
                if mark == 'R':
                    red = red + 1
                if mark == 'B':
                    black = black + 1

        if red + black == 64:
            return 0

        return None

    def BoardFull(self):
        black = 0
        red = 0
        for row in self.grid:
            for mark in row:
                if mark == 'R':
                    red = red + 1
                if mark == 'B':
                    black = black + 1

        if red + black == 64:
            return True

        return False

class Agent(object):
    """Abstract class, extended by classes RandomAgent, FirstMoveAgent, MinimaxAgent.
    Do not make an instance of this class."""

    def __init__(self, color):
        """Agents use either RED or BLACK chips."""
        self.color = color

    @abc.abstractmethod
    def move(self, game):
        """Abstract. Must be implemented by a class that extends Agent."""
        pass


class RandomAgent(Agent):
    """Naive agent -- always performs a random move"""

    def move(self, game):
        """Returns a random move"""
        free_columns = []
        for i in range(8):
            if game.grid[0][i] == '-':
                free_columns.append(i)
            if i == 7 and free_columns.count == 0:
                return None

        free_column = random.choice(free_columns)
        free_row = -1
        for j in reversed(range(8)):
            if game.grid[j][free_column] == '-':
                free_row = j
            if free_row != -1:
                break

        if game.color == 'R':
            game.grid[free_row][free_column] = 'R'
            return Game(game.grid)
        else:
            game.grid[free_row][free_column] = 'B'
            return Game(game.grid)



class FirstMoveAgent(Agent):
    """Naive agent -- always performs the first move"""

    def move(self, game):
        """Returns the first possible move"""
        free_column = -1
        # Find first free column
        for i in range(8):
            if game.grid[0][i] == '-':
                free_column = i
            if i != -1:
                break

        if i == -1:
            return None

        free_row = -1
        for j in reversed(range(8)):
            if game.grid[j][free_column] == '-':
                free_row = j
            if j != -1:
                break

        if game.color == 'R':
            game.grid[free_row][free_column] = 'R'
            return Game(game.grid)
        else:
            game.grid[free_row][free_column] = 'B'
            return Game(game.grid)


class MinimaxAgent(Agent):
    """Smart agent -- uses minimax to determine the best move"""

    def move(self, game):
        """Returns the best move using minimax"""
        best_move = (0, 0)
        agent_color = self.color
        opponent_color = ''
        if agent_color == 'R':
            opponent_color = 'B'
        else:
            opponent_color = 'R'

        best_move_horizontal = (-1, -1)
        best_move_vertical = (-1, -1)
        best_move_diagonal = (-1, -1)

        available_moves = []
        unavailable_columns = []

        for row in reversed(range(8)):
            for column in range(8):
                if column not in unavailable_columns:
                    if game.grid[row][column] == '-':
                        available_moves.append((row, column))
                        unavailable_columns.append(column)

        print("")

        isTerminal = True

        for row in reversed(range(8)):
            for column in range(8):
                piece = game.grid[row][column]
                if row != 0:
                    if game.grid[row - 1][column] == '-':
                        isTerminal = False
                if column != 0 and column != 7:
                    if game.grid[row][column - 1] == '-':
                        isTerminal = False
                    if game.grid[row][column + 1] == '-':
                        isTerminal = False
                if column == 0:
                    if game.grid[row][column + 1] == '-':
                        isTerminal = False
                if column == 7:
                    if game.grid[row][column - 1] == '-':
                        isTerminal = False

        depth = 0

        for move in available_moves:
            if depth <= move[0]:
                depth = move[0]

        if depth == 0 or isTerminal:
            return Game.winning_state(self)

        best_move == game
        r_count = 0
        r_counts = []

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Down')
            for i in range(1, 4):
                if move[0] + i <= 7:
                    move_down_row = move[0] + i
                    r_arr.append(game.grid[move_down_row][move[1]])
            r_counts.append(r_arr)

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Right')
            for i in range(1, 4):
                if move[1] + i <= 7:
                    move_right_row = move[1] + i
                    r_arr.append(game.grid[move[0]][move_right_row])
            r_counts.append(r_arr)

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Left')
            for i in range(1, 4):
                if move[1] - i >= 0:
                    move_left_column = move[1] - i
                    r_arr.append(game.grid[move[0]][move_left_column])
            r_counts.append(r_arr)

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Down Left')
            for i in range(1, 4):
                if move[0] + i <= 7 and move[1] - i >= 0:
                    move_down_row = move[0] + i
                    move_left_column = move[1] - i
                    r_arr.append(game.grid[move_down_row][move_left_column])
            r_counts.append(r_arr)

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Down Right')
            for i in range(1, 4):
                if move[0] + i <= 7 and move[1] + i <= 7:
                    move_down_row = move[0] + i
                    move_right_column = move[1] + i
                    r_arr.append(game.grid[move_down_row][move_right_column])
            r_counts.append(r_arr)

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Up Right')
            for i in range(1, 4):
                if move[0] - i >= 0 and move[1] + i <= 7:
                    move_up_row = move[0] - i
                    move_right_column = move[1] + i
                    r_arr.append(game.grid[move_up_row][move_right_column])
            r_counts.append(r_arr)

        for move in available_moves:
            r_arr = []
            r_arr.append(move)
            r_arr.append('Up Left')
            for i in range(1, 4):
                if move[0] - i >= 0 and move[1] - i >= 0:
                    move_up_row = move[0] - i
                    move_left_column = move[1] - i
                    r_arr.append(game.grid[move_up_row][move_left_column])
            r_counts.append(r_arr)

        r_counts2 = []
        for array in r_counts:
            index = 0

            cleaned_array = []
            if len(array) > 2:
                for item in array:
                    if item == 'B' or item == '-':
                        break
                    cleaned_array.append(item)
                if len(cleaned_array) > 2:
                    r_counts2.append(cleaned_array)
            cleaned_array = []

            index = index + 1

        right_left_r_array = []
        ul_dr_r_array = []
        up_right_down_left_array = []
        down_r_array = []

        combined_r_array_of_r_arrays = []
        for array in r_counts2:
            if array[1] == 'Right' or array[1] == 'Left':
                right_left_r_array.append(array)
            if array[1] == 'Up Left' or array[1] == 'Down Right':
                ul_dr_r_array.append(array)
            if array[1] == 'Up Right' or array[1] == 'Down Left':
                up_right_down_left_array.append(array)
            if array[1] == 'Down':
                down_r_array.append(array)

        right_left_r_array = sorted(right_left_r_array, key = lambda x: x[0])
        ul_dr_r_array = sorted(ul_dr_r_array, key = lambda x: x[0])
        up_right_down_left_array = sorted(up_right_down_left_array, key = lambda x: x[0])

        right_and_left_r_array = []
        ul_and_dr_r_array = []
        up_right_and_down_left_array = []

        for array in right_left_r_array:
            index = 0
            combined_array = []
            if index != len(right_left_r_array) - 1 and len(right_left_r_array) != 0 and array[0] == right_left_r_array[index + 1][0]:
                for item in array:
                    combined_array.append(item)
                for item in reversed(right_left_r_array[index + 1]):
                    if item != 'R':
                        break
                    combined_array.append(item)
                combined_array[1] = "Right and Left"
                if combined_array not in right_and_left_r_array:
                    right_and_left_r_array.append(combined_array)

            index = index + 1

        for array in ul_dr_r_array:
            index = 0
            combined_array = []
            if index != len(ul_dr_r_array) - 1 and len(ul_dr_r_array) != 0 and array[0] == ul_dr_r_array[index + 1][0]:
                for item in array:
                    combined_array.append(item)
                for item in reversed(ul_dr_r_array[index + 1]):
                    if item != 'R':
                        break
                    combined_array.append(item)
                combined_array[1] = "Up Left and Down Right"
                if combined_array not in ul_and_dr_r_array:
                    ul_and_dr_r_array.append(combined_array)

        for array in up_right_down_left_array:
            index = 0
            combined_array = []
            if index != len(up_right_down_left_array) - 1 and len(up_right_down_left_array) != 0 and array[0] == up_right_down_left_array[index + 1][0]:
                for item in array:
                    combined_array.append(item)
                for item in reversed(up_right_down_left_array[index + 1]):
                    if item != 'R':
                        break
                    combined_array.append(item)
                combined_array[1] = "Up Right and Down Left"
                if combined_array not in up_right_and_down_left_array:
                    up_right_and_down_left_array.append(combined_array)

            index = index + 1

        best_move_r = [(0,0),0]

        for array in right_left_r_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        for array in down_r_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        for array in ul_dr_r_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        for array in up_right_down_left_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        for array in right_and_left_r_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        for array in up_right_and_down_left_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        for array in ul_and_dr_r_array:
            count = array.count('R')
            if count > best_move_r[1]:
                best_move_r[1] = count
                best_move_r[0] = array[0]

        best_move_tuple = best_move_r[0]
        best_move = (best_move_r[0][0], best_move_r[0][1])
        print(best_move)

        #game.grid[best_move_tuple[0]][best_move_tuple[1]] = 'R'
        print(".")
        return best_move

def tournament(simulations=50):
    """Simulate connect four games, of a minimax agent playing
    against a random agent"""

    redwin, blackwin, tie = 0, 0, 0
    for i in range(simulations):

        game = single_game(io=False)

        print(i, end=" ")
        if game.winning_state() == float("inf"):
            redwin += 1
        elif game.winning_state() == float("-inf"):
            blackwin += 1
        elif game.winning_state() == 0:
            tie += 1

    print("Red %d (%.0f%%) Black %d (%.0f%%) Tie %d" % (
    redwin, redwin / simulations * 100, blackwin, blackwin / simulations * 100, tie))

    return redwin / simulations

def diagonal_arrays(self):
    diagonal_array = []
    icon = ''
    i = 0
    j = 0
    for row in self.grid:
        for column in row:
            if (2 < i < 5) and (2 < j < 5):
                diagonal_array.append(self.grid[i][j])
                diagonal_array.append(self.grid[i - 1][j + 1])
                diagonal_array.append(self.grid[i - 2][j + 2])
                diagonal_array.append(self.grid[i - 3][j + 3])
            j = j + 1
        i = i + 1


def single_game(io=True):
    """Create a game and have two agents play it."""
    game1 = Game([['-' for i in range(8)] for j in range(8)])

    game2 = Game([['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', 'R', '-', '-', '-', '-', '-']])

    game3 = Game([['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', 'B', '-', '-', '-'],
                  ['-', '-', 'R', '-', 'B', '-', '-', '-'],
                  ['-', '-', 'R', '-', 'B', '-', '-', '-'],
                  ['-', '-', 'R', 'R', 'B', '-', '-', '-']])

    game4 = Game([['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['R', 'R', 'R', 'R', 'B', 'B', 'B', '-']])

    game5 = Game([['-', '-', 'R', '-', '-', '-', '-', '-'],
                  ['-', '-', 'B', '-', '-', '-', '-', '-'],
                  ['-', '-', 'R', '-', '-', '-', '-', '-'],
                  ['-', '-', 'B', '-', '-', '-', '-', '-'],
                  ['-', '-', 'R', '-', 'R', '-', '-', '-'],
                  ['-', '-', 'B', 'R', 'B', '-', '-', '-'],
                  ['-', 'B', 'R', 'B', 'B', '-', '-', '-'],
                  ['-', 'R', 'R', 'B', 'R', '-', '-', '-']])

    game6 = Game([['B', 'B', 'B', 'R', 'R', 'R', 'B', 'R'],
                  ['B', 'B', 'R', 'R', 'B', 'B', 'B', 'R'],
                  ['B', 'R', 'B', 'B', 'B', 'R', 'R', 'B'],
                  ['B', 'B', 'B', 'R', 'R', 'B', 'R', 'B'],
                  ['R', 'R', 'R', 'B', 'B', 'B', 'R', 'B'],
                  ['R', 'R', 'B', 'B', 'R', 'R', 'B', 'R'],
                  ['B', 'B', 'R', 'R', 'B', 'R', 'R', 'B'],
                  ['R', 'B', 'B', 'B', 'R', 'B', 'R', 'B']])

    game7 = Game([['R', 'B', 'B', 'R', 'R', 'R', 'B', 'R'],
                  ['B', 'B', 'R', 'R', 'B', 'B', 'B', 'R'],
                  ['B', 'R', 'B', 'B', 'B', 'R', 'R', 'B'],
                  ['B', 'B', 'B', 'R', 'R', 'B', 'R', 'B'],
                  ['R', 'R', 'R', 'B', 'B', 'B', 'R', 'B'],
                  ['R', 'R', 'B', 'B', 'R', 'R', 'B', 'R'],
                  ['B', 'B', 'R', 'R', 'B', 'R', 'R', 'B'],
                  ['R', 'B', 'B', 'B', 'R', 'B', 'R', 'B']])

    game8 = Game([['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', '-', '-', '-', '-', '-', '-'],
                  ['-', '-', 'R', 'R', '-', '-', '-', '-']])

    game9 = Game([['-', 'B', 'B', 'R', 'R', 'B', 'B', 'R'],
                  ['-', 'B', 'B', 'R', 'R', 'B', 'B', 'R'],
                  ['B', 'R', 'R', 'B', 'B', 'R', 'R', 'B'],
                  ['B', 'R', 'B', 'R', 'B', 'B', 'R', 'B'],
                  ['R', 'B', 'R', 'B', 'B', 'B', 'R', 'B'],
                  ['B', 'R', 'R', 'B', 'R', 'R', 'B', 'R'],
                  ['B', 'B', 'R', 'R', 'B', 'R', 'R', 'B'],
                  ['R', 'B', 'B', 'B', 'R', 'B', 'R', 'B']])

    game10 = Game([['-', 'B', 'B', 'R', 'R', 'B', 'B', 'R'],
                   ['B', 'B', 'B', 'R', 'R', 'B', 'B', 'R'],
                   ['B', 'R', 'R', 'B', 'B', 'R', 'R', 'B'],
                   ['B', 'R', 'B', 'R', 'B', 'B', 'R', 'B'],
                   ['R', 'B', 'R', 'B', 'B', 'B', 'R', 'B'],
                   ['B', 'R', 'R', 'B', 'R', 'R', 'B', 'R'],
                   ['B', 'B', 'R', 'R', 'B', 'R', 'R', 'B'],
                   ['R', 'B', 'B', 'B', 'R', 'B', 'R', 'B']])

    #game = Game([['-' for i in range(8)] for j in range(8)])  # 8x8 empty board
    game = game5

    if io:
        game.display()

    maxplayer = MinimaxAgent('R')
    minplayer = RandomAgent('B')


    while True:

        m = maxplayer.move(game)
        game = game.neighbor(m[1], maxplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

        g = minplayer.move(game)
        game = game.neighbor(g, minplayer.color)
        if io:
            time.sleep(1)
            game.display()

        if game.winning_state() is not None:
            break

    if game.winning_state() == float("inf"):
        print("RED WINS!")
    elif game.winning_state() == float("-inf"):
        print("BLACK WINS!")
    elif game.winning_state() == 0:
        print("TIE!")

    return game


if __name__ == '__main__':
    single_game(io=True)
    #tournament(simulations=50)
