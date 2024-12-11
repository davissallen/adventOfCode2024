from copy import deepcopy

BARRIER = '#'
UNEXPLORED = '.'
GUARD = '^'

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

TURN = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
}

DIRECTIONAL_STEP = {
    NORTH: '^',
    EAST: '>',
    SOUTH: 'v',
    WEST: '<',
}


def parse_input(filename):
    return [[set() if c == UNEXPLORED else c for c in line.strip()] for line in open(filename, 'r').readlines()]


def count_footsteps(_maze):
    count = 0
    for row in range(len(_maze)):
        for col in range(len(_maze[row])):
            if isinstance(_maze[row][col], set):
                count += 1
    return count


def part1(_maze, row, col):
    simulate_and_record_guard_movement(_maze, row, col, NORTH)
    return count_footsteps(_maze)


def is_loop(_maze, row, col, direction):
    while is_in_bounds(_maze, row, col):
        if _maze[row][col] == BARRIER:
            row, col = row - direction[0], col - direction[1]
            direction = TURN[direction]
        elif DIRECTIONAL_STEP[direction] in _maze[row][col]:
            return True
        else:
            _maze[row][col].add(DIRECTIONAL_STEP[direction])
            row, col = row + direction[0], col + direction[1]
    return False


def simulate_and_record_guard_movement(_maze, row, col, direction):
    path_coordinates = set()
    # aside: the really cool version would use a 4-bit bitmap
    while 0 <= row < len(_maze) and 0 <= col < len(_maze[row]):
        path_coordinates.add((row, col))
        if _maze[row][col] == BARRIER:
            # retrace step + turn
            row, col = row - direction[0], col - direction[1]
            direction = TURN[direction]
        else:
            _maze[row][col].add(DIRECTIONAL_STEP[direction])
            row, col = row + direction[0], col + direction[1]
    return path_coordinates


def find_guard_position(_maze):
    for row in range(len(_maze)):
        for col in range(len(_maze[row])):
            if _maze[row][col] == GUARD:
                return row, col


def pretty_print_maze(_maze):
    for row in _maze:
        new_row = []
        for item in row:
            if item == {'<'} or item == {'>'}:
                translation = '-'
            elif item == {'^'} or item == {'v'}:
                translation = '|'
            elif item == set():
                translation = '.'
            elif item == BARRIER:
                translation = BARRIER
            elif item == 'O':
                translation = 'O'
            else:
                translation = '+'
            new_row.append(translation)
        print(''.join(new_row))
    print()


def part2_rec(barrier_memo, _maze, row, col, direction, barrier_location, guard_x, guard_y):
    if not 0 <= row < len(_maze) or not 0 <= col < len(_maze[row]):
        return 0  # escaped
    elif DIRECTIONAL_STEP[direction] in _maze[row][col]:
        pretty_print_maze(_maze)
        barrier_memo.add(barrier_location)
        return 1  # looped
    elif _maze[row][col] == BARRIER:
        # undo last step and turn
        return part2_rec(barrier_memo, _maze, row - direction[0], col - direction[1], TURN[direction], barrier_location,
                         guard_x, guard_y)
    elif not barrier_location:
        _maze[row][col].add(DIRECTIONAL_STEP[direction])

        # minor edge case: cannot place barrier on guard's position. just continue
        if (row == guard_x and col == guard_y) or (row, col) in barrier_memo:
            return part2_rec(barrier_memo, _maze, row + direction[0], col + direction[1], direction, barrier_location, guard_x,
                             guard_y)

        temp = _maze[row][col]
        _maze[row][col] = 'O'
        # place barrier on current position (pretend), retrace, and turn
        loop_res = part2_rec(barrier_memo, _maze, row - direction[0], col - direction[1], TURN[direction], (row, col),
                             guard_x, guard_y)
        _maze[row][col] = temp

        continue_res = part2_rec(barrier_memo, _maze, row + direction[0], col + direction[1], direction, barrier_location,
                                 guard_x, guard_y)

        return loop_res + continue_res
    else:
        # if i've already placed a barrier, that means I am on an exploratory path, and I need to un-do my steps after exploring
        _maze[row][col].add(DIRECTIONAL_STEP[direction])
        ans = part2_rec(barrier_memo, _maze, row + direction[0], col + direction[1], direction, barrier_location, guard_x,
                    guard_y)
        _maze[row][col].remove(DIRECTIONAL_STEP[direction])
        return ans


def part2_iter(_maze, row, col):
    guard_x, guard_y = row, col
    barrier_locations = set()
    direction = NORTH

    # main loop
    while is_in_bounds(_maze, col, row):
        current_cell = _maze[row][col]
        if current_cell == BARRIER:
            # retrace step + turn
            row, col = row - direction[0], col - direction[1]
            direction = TURN[direction]
        else:
            # first, pretend there is a barrier (eventually ignore guard's spot)
            can_place_barrier = (row, col) != (guard_x, guard_y) and (row, col) not in barrier_locations and _maze[row][col] == set()
            if can_place_barrier:
                maze_copy = [row[:] for row in _maze]
                temp = maze_copy[row][col]
                maze_copy[row][col] = BARRIER
                if is_loop(maze_copy, row, col, direction):
                    barrier_locations.add((row, col))
                maze_copy[row][col] = temp

            _maze[row][col].add(DIRECTIONAL_STEP[direction])
            row, col = row + direction[0], col + direction[1]

    return len(barrier_locations)

def part2_iter_try2(_maze, guard_x, guard_y):
    maze_copy = deepcopy(_maze)
    coordinates = simulate_and_record_guard_movement(maze_copy, guard_x, guard_y, NORTH)

    count = 0
    for i, (row, col) in enumerate(coordinates):
        if i % 100 == 0:
            print(str(i / len(coordinates) * 100)[:3] + '%')
        if (row, col) != (guard_x, guard_y) and _maze[row][col] == set():
            maze_copy = deepcopy(_maze)
            maze_copy[row][col] = BARRIER
            count += 1 if is_loop(maze_copy, guard_x, guard_y, NORTH) else 0
    return count


def is_in_bounds(_maze, col, row):
    return 0 <= row < len(_maze) and 0 <= col < len(_maze[row])


if __name__ == '__main__':
    '''https://adventofcode.com/2024/day/6'''

    '''
    Instructions:
    If there is something directly in front of you, turn right 90 degrees.
    Otherwise, take a step forward.
    
    Problem:
    Predict the path of the guard.
    How many distinct positions will the guard visit before leaving the mapped area?
    '''
    maze = parse_input('input.txt')
    x, y = find_guard_position(maze)
    maze[x][y] = set()  # erase guard icon

    # print('part 1: ' + str(part1(maze, x, y)))
    print('part 2: ' + str(part2_iter_try2(maze, x, y)))
