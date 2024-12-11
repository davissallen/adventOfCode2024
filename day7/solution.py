def parse_input(filename):
    lines = open(filename, 'r').readlines()
    parsed = []
    for line in lines:
        i = line.index(':')
        result, operands = int(line[:i].strip()), [int(i) for i in line[i+1:].strip().split(' ')]
        parsed.append((result, operands))
    return parsed


def is_possible(need, remaining_numbers):
    if need < 0:
        return False
    elif need == 0:
        return True
    elif not remaining_numbers:
        return False
    else:
        return any((
            is_possible(need / remaining_numbers[-1], remaining_numbers[:-1]),
            is_possible(need - remaining_numbers[-1], remaining_numbers[:-1])
        ))


def part1(_result_to_operands):
    answer = 0
    for result, operands in _result_to_operands:
        if is_possible(result, operands):
            answer += result
    return answer


if __name__ == '__main__':
    result_to_operands = parse_input('input.txt')

    print('part 1:' + str(part1(result_to_operands)))