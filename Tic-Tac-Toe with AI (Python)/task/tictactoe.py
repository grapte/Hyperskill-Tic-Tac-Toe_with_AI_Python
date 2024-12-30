import random
import re
from collections import Counter
from enum import Enum
from itertools import chain

grid = [[' '] * 3 for _ in range(3)]


class GameState(Enum):
    NOT_FINISHED = "Game not finished"
    DRAW = "Draw"
    X_WINS = "X wins"
    O_WINS = "O wins"


state = GameState.NOT_FINISHED


def print_game():
    print('---------')
    for r in range(3):
        print('| ', end='')
        for c in range(3):
            print(f'{grid[r][c]} ', end='')
        print('|')
    print('---------')


def user_action():
    while True:
        line = input('Enter the coordinates: ')
        res = re.match(r'(\d) (\d)', line)
        if res:
            r, c = res.group().split()
        else:
            print('You should enter numbers!')
            continue

        r, c = int(r) - 1, int(c) - 1
        if (0 > r or r >= 3) or (0 > c or c >= 3):
            print('Coordinates should be from 1 to 3!')
            continue

        if grid[r][c] != ' ':
            print('This cell is occupied! Choose another one!')
            continue

        flat = chain.from_iterable(grid)
        count = Counter(flat)
        if count['X'] == count['O']:
            move = 'X'
        elif count['X'] == count['O']+1:
            move = 'O'
        else:
            raise RuntimeError("X, O count impossible for user_action")

        grid[r][c] = move
        break


def find_two_in_a_row(moved):
    # Check rows
    for row_idx, row in enumerate(grid):
        if row.count(moved) == 2 and row.count(' ') == 1:
            col_idx = row.index(' ')  # Find the empty cell in the row
            return row_idx, col_idx  # Return the position (row, col)

    # Check columns
    for col_idx in range(3):
        column = [grid[row_idx][col_idx] for row_idx in range(3)]
        if column.count(moved) == 2 and column.count(' ') == 1:
            row_idx = column.index(' ')  # Find the empty cell in the column
            return row_idx, col_idx  # Return the position (row, col)

    # Check main diagonal (top-left to bottom-right)
    main_diagonal = [grid[i][i] for i in range(3)]
    if main_diagonal.count(moved) == 2 and main_diagonal.count(' ') == 1:
        idx = main_diagonal.index(' ')  # Find the empty cell in the diagonal
        return idx, idx  # Row and column are the same for main diagonal

    # Check anti-diagonal (top-right to bottom-left)
    anti_diagonal = [grid[i][3 - 1 - i] for i in range(3)]
    if anti_diagonal.count(moved) == 2 and anti_diagonal.count(' ') == 1:
        idx = anti_diagonal.index(' ')  # Find the empty cell in the diagonal
        return idx, 3 - 1 - idx  # Compute the column for the anti-diagonal

    return None, None


def comp_action(level: str):
    print(f'Making move level "{level}"')
    match level:
        case 'easy':
            flat = chain.from_iterable(grid)
            spaces = [i for i, p in enumerate(flat) if p == ' ']
            pos = random.choice(spaces)
            r, c = divmod(pos, 3)
        case 'medium':
            flat = chain.from_iterable(grid)
            count = Counter(flat)
            if count['X'] == count['O']:
                moved = 'X'
            elif count['X'] == count['O'] + 1:
                moved = 'O'
            else:
                raise RuntimeError("X, O count impossible for medium comp_action")
            r, c = find_two_in_a_row(moved)  # winning move if we find 2 in a row
            if not r:
                if moved == 'O':
                    moved = 'X'
                else:
                    moved = 'O'
                r, c = find_two_in_a_row(moved)  # blocking move if other has 2 in a row
                if not r:
                    flat = chain.from_iterable(grid)
                    spaces = [i for i, p in enumerate(flat) if p == ' ']
                    pos = random.choice(spaces)
                    r, c = divmod(pos, 3)  # random if neither
        case 'hard':
            def minimax():
                flat = list(chain.from_iterable(grid))
                count = Counter(flat)
                if count['X'] == count['O']:
                    move = 'X'
                elif count['X'] == count['O'] + 1:
                    move = 'O'
                else:
                    raise RuntimeError("X, O count impossible for hard comp_action")

                if (any(all(c == 'X' for c in row) for row in grid) or
                    any(all(row[col] == 'X' for row in grid) for col in range(3)) or
                    all(grid[i][i] == 'X' for i in range(3)) or
                    all(grid[i][3 - 1 - i] == 'X' for i in range(3))
                    ):
                    return (+1, None, None)
                elif (any(all(c == 'O' for c in row) for row in grid) or
                    any(all(row[col] == 'O' for row in grid) for col in range(3)) or
                    all(grid[i][i] == 'O' for i in range(3)) or
                    all(grid[i][3 - 1 - i] == 'O' for i in range(3))
                    ):
                    return (-1, None, None)
                elif len([i for i, p in enumerate(flat) if p == ' ']) == 0:
                    return (0, None, None)

                best = (-2, None, None) if move == 'X' else (2, None, None)

                for i in [i for i, p in enumerate(flat) if p == ' ']:
                    r, c = divmod(i, 3)
                    grid[r][c] = move
                    score, _, _ = minimax()
                    grid[r][c] = ' '

                    if move == 'X':
                        if score > best[0]:
                            best = (score, r, c)
                        elif score == best[0] and best[1] is None:
                            best = (score, r, c)
                    else:
                        if score < best[0]:
                            best = (score, r, c)
                        elif score == best[0] and best[1] is None:
                            best = (score, r, c)

                return best

            s, r, c = minimax()

    flat = chain.from_iterable(grid)
    count = Counter(flat)
    if count['X'] == count['O']:
        move = 'X'
    elif count['X'] == count['O'] + 1:
        move = 'O'
    else:
        raise RuntimeError("X, O count impossible for comp_action")
    grid[r][c] = move


def check_grid():
    global state
    flat = chain.from_iterable(grid)
    count = Counter(flat)

    if count['X'] == count['O']:
        moved = 'O'
        win = GameState.O_WINS
    elif count['X'] == count['O'] + 1:
        moved = 'X'
        win = GameState.X_WINS
    else:
        raise RuntimeError("X, O count impossible for check_grid")

    three_in_a_row = (
        any(all(c == moved for c in row) for row in grid) or
        any(all(row[col] == moved for row in grid) for col in range(3)) or
        all(grid[i][i] == moved for i in range(3)) or
        all(grid[i][3 - 1 - i] == moved for i in range(3))
    )

    if three_in_a_row:
        state = win
    else:
        if count['X'] == 5 and count['O'] == 4:
            state = GameState.DRAW
            return

def init_cells():
    line = input('Enter the cells: ')
    assert all((i in {'X', 'O', '_'} for i in line)), 'Not all symbols are valid (X, O or _)'

    line = line.replace('_', ' ')
    for i, char in enumerate(line):
        r, c = divmod(i, 3)
        grid[r][c] = char


def game(p1, p2):
    turn = 0
    if p1 == 'user':
        p1_action = user_action
    else:
        p1_action = lambda: comp_action(p1)

    if p2 == 'user':
        p2_action = user_action
    else:
        p2_action = lambda: comp_action(p2)

    while True:
        match state:
            case GameState.X_WINS | GameState.O_WINS | GameState.DRAW:
                print_game()
                print(state.value)
                break
            case GameState.NOT_FINISHED:
                print_game()
                if turn % 2 == 0:
                    p1_action()
                else:
                    p2_action()
                check_grid()
                turn += 1


def main():
    global grid, state
    players = ['easy', 'medium', 'hard', 'user']
    while True:
        line = input('Input command: ')
        line = line.split(' ')
        match line:
            case ['start', p1, p2] if p1 in players and p2 in players:
                grid = [[' '] * 3 for _ in range(3)]
                state = GameState.NOT_FINISHED
                game(p1, p2)
            case ['exit']:
                break
            case _:
                print('Bad parameters!')

if __name__ == '__main__':
    main()
