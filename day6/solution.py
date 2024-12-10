BARRIER = '#'
EMPTY_SPACE = '.'
GUARD = '^'
STEP = 'X'

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

TURNS = {
    NORTH: EAST,
    EAST: SOUTH,
    SOUTH: WEST,
    WEST: NORTH,
}


def parse_input(filename):
    return [[c for c in line.strip()] for line in open(filename, 'r').readlines()]


def count_footsteps(_maze):
    count = 0
    for row in range(len(_maze)):
        for col in range(len(_maze[row])):
            if _maze[row][col] == STEP:
                count += 1
    return count


def part1(_maze, row, col):
    direction = NORTH
    while 0 <= row < len(_maze) and 0 <= col < len(_maze[row]):
        if _maze[row][col] == BARRIER:
            # retrace step + turn
            row, col = row - direction[0], col - direction[1]
            direction = TURNS[direction]
        else:
            _maze[row][col] = STEP  # record current position
            row, col = row + direction[0], col + direction[1]

    return count_footsteps(_maze)


def find_guard_position(_maze):
    for row in range(len(_maze)):
        for col in range(len(_maze[row])):
            if _maze[row][col] == GUARD:
                return row, col


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

    print('part 1: ' + str(part1(maze, x, y)))
