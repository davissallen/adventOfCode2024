def parse_reports(filename):
    return [[int(x) for x in line.split(' ')] for line in open(filename, 'r').read().splitlines()]


def report_is_valid(report):
    if len(report) <= 1:
        return True, 1
    if report[1] < report[0]:
        # expect decreasing
        previous = report[0]
        for i in range(1, len(report)):
            difference = previous - report[i]
            if not 1 <= difference <= 3:
                return False, i
            previous = report[i]
    else:
        # expect increasing
        previous = report[0]
        for i in range(1, len(report)):
            difference = report[i] - previous
            if not 1 <= difference <= 3:
                return False, i
            previous = report[i]

    return True, 1


def part1(reports):
    return sum(1 for report in reports if report_is_valid(report)[0])


def report_is_valid_part2(report):
    # try the entire report
    ans = report_is_valid(report)
    if ans[0]:
        return True
    else:
        i = ans[1]
        return any((
            report_is_valid(report[:i - 2] + report[i - 1:])[0],
            report_is_valid(report[:i - 1] + report[i + 0:])[0],
            report_is_valid(report[:i + 0] + report[i + 1:])[0],
            report_is_valid(report[:i + 1] + report[i + 2:])[0],
        ))
    # do a second try by removing the breaking element
    # find breaking element
    # try removing element and idx - 1 and idx + 1


def part2(reports):
    return sum(1 for report in reports if report_is_valid_part2(report))


if __name__ == '__main__':
    reports = parse_reports('../inputs/2.txt')
    print('part 1: ' + str(part1(reports)))
    print('part 2: ' + str(part2(reports)))
