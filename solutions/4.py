XMAS = 'XMAS'


def parse_input(filename):
    return [s.strip() for s in open(filename, 'r').readlines()]


def does_match_word(word_search, word, ordered_coordinates):
    found_word = []
    for x, y in ordered_coordinates:
        if not 0 <= x < len(word_search) or not 0 <= y < len(word_search[x]):
            return False
        found_word.append(word_search[x][y])
    return ''.join(found_word) == word


def search(word_search, row, col):
    if not word_search[row][col] == 'X':
        return 0

    # right
    right = [(row, col), (row, col + 1), (row, col + 2), (row, col + 3)]
    # left
    left = [(row, col), (row, col - 1), (row, col - 2), (row, col - 3)]
    # up
    up = [(row, col), (row - 1, col), (row - 2, col), (row - 3, col)]
    # down
    down = [(row, col), (row + 1, col), (row + 2, col), (row + 3, col)]
    # diag up-right
    up_right = [(row, col), (row - 1, col + 1), (row - 2, col + 2), (row - 3, col + 3)]
    # diag bottom-right
    bottom_right = [(row, col), (row + 1, col + 1), (row + 2, col + 2), (row + 3, col + 3)]
    # diag bottom-left
    bottom_left = [(row, col), (row + 1, col - 1), (row + 2, col - 2), (row + 3, col - 3)]
    # diag up-left
    up_left = [(row, col), (row - 1, col - 1), (row - 2, col - 2), (row - 3, col - 3)]

    cases = [right, left, up, down, up_right, bottom_right, bottom_left, up_left]
    return sum(does_match_word(word_search, XMAS, coords) for coords in cases)


def solve_part1(word_search):
    count = 0
    for row in range(len(word_search)):
        for col in range(len(word_search[row])):
            count += search(word_search, row, col)
    return count


if __name__ == '__main__':
    word_search = parse_input('../inputs/4.txt')

    print('part1: ' + str(solve_part1(word_search)))
