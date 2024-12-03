import functools
import operator
import re

MUL_PATTERN = re.compile(r'mul\((?P<first>\d{1,3}),(?P<second>\d{1,3})\)')

def solve_mul(match):
    return functools.reduce(operator.mul, [int(x) for x in match])


def solve_command(command):
    matches = re.findall(MUL_PATTERN, command)
    return sum(solve_mul(match) for match in matches)


def part1(commands):
    return sum(solve_command(command) for command in commands)


if __name__ == '__main__':
    commands = open('../inputs/3.txt', 'r').readlines()

    print('part1: ' + str(part1(commands)))