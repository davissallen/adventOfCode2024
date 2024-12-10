def parse_rules(raw_rules):
    dependency_map = {}
    for raw_rule in raw_rules:
        a, b = raw_rule.split('|')
        a, b = int(a), int(b)
        if b in dependency_map:
            dependency_map[b].add(a)
        else:
            dependency_map[b] = {a}
    return dependency_map


def parse_updates(raw_updates):
    return [[int(x) for x in update.split(',')] for update in raw_updates]


def parse_input(filename):
    lines = open(filename).read().splitlines()
    i = lines.index('')
    raw_rules, raw_updates = lines[:i], lines[i + 1:]

    rule_map = parse_rules(raw_rules)
    update_list = parse_updates(raw_updates)

    return rule_map, update_list


def update_is_valid_part1(rules, pages):
    exists = set(pages)
    seen = set()

    for page in pages:
        if page in rules:
            # if the page has pre-requisites, filter out the ones that exist, and guarantee they are in seen
            existing_pages_that_should_come_before = rules[page] & exists
            if existing_pages_that_should_come_before and not existing_pages_that_should_come_before.issubset(seen):
                return False
        seen.add(page)
    return True


def part1(rules, updates):
    correct_updates = [update for update in updates if update_is_valid_part1(rules, update)]

    # seems like all updates are of odd length
    assert all(len(update) % 2 == 1 for update in correct_updates)

    return sum(update[len(update) // 2] for update in correct_updates)


def custom_sort(pages, rules):
    included_pages = set(pages)

    i = 0
    seen = set()
    while not update_is_valid_part1(rules, pages):
        if pages[i] not in rules:
            seen.add(pages[i])
            i += 1
            continue

        need = (rules[pages[i]] - seen) & included_pages
        if not need:
            seen.add(pages[i])
            i += 1
        else:
            j = i + 1
            while need:
                if pages[j] in need:
                    need.remove(pages[j])
                j += 1
            pages[i], pages[j - 1] = pages[j - 1], pages[i]
            seen.add(pages[i])
            # don't increment i

    return pages


def part2(rules, updates):
    bad_updates = [custom_sort(update, rules) for update in updates if not update_is_valid_part1(rules, update)]

    return sum(update[len(update) // 2] for update in bad_updates)


if __name__ == "__main__":
    # problem:
    # https://adventofcode.com/2024/day/5

    rules, updates = parse_input('input.txt')

    print('part 1: ' + str(part1(rules, updates)))
    print('part 2: ' + str(part2(rules, updates)))
