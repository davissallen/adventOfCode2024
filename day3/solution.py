import functools
import operator
import re

MUL_PATTERN = r'mul\((?P<first>\d{1,3}),(?P<second>\d{1,3})\)'
DO_PATTERN = r'(do\(\))'
DONT_PATTERN = r"(don't\(\))"
COMBINED_PATTERN = re.compile(DO_PATTERN + '|' + DONT_PATTERN + '|' + MUL_PATTERN)

def solve_mul(match):
    return functools.reduce(operator.mul, [int(x) for x in match])


def solve_command_part1(command):
    matches = re.findall(MUL_PATTERN, command)
    return sum(solve_mul(match) for match in matches)


def solve_command_part2(command):
    matches = re.findall(COMBINED_PATTERN, command)
    solution = 0
    can_mul = True
    for match in matches:
        if not can_mul:
            # check for do
            if match[0]:
                can_mul = True
        else:
            # check for don't
            if match[1]:
                can_mul = False
            # check for mul, ignore repeat do()
            elif not match[0]:
                solution += solve_mul(match[2:])
    return solution

def part1(commands):
    return sum(solve_command_part1(command) for command in commands)


def part2(commands):
    command = ''.join(commands)
    return solve_command_part2(command)


if __name__ == '__main__':
    commands = open('input.txt', 'r').readlines()

    print('part1: ' + str(part1(commands)))
    print('part2: ' + str(part2(commands)))
