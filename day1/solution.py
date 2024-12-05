from collections import defaultdict


def get_left_and_right_nums_sorted(filename):
    left_nums = []
    right_nums = []
    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            left, right = line.split('   ')
            left_nums.append(int(left))
            right_nums.append(int(right))

    left_nums.sort()
    right_nums.sort()

    return left_nums, right_nums

def part_1(left_nums, right_nums):
    distance = 0
    for i in range(len(left_nums)):
        d = abs(left_nums[i] - right_nums[i])
        distance += d
    return distance

def part_2(left_nums, right_nums):
    right_freq = defaultdict(int)
    for num in right_nums:
        right_freq[num] += num
    return sum(right_freq[num] for num in left_nums)


if __name__ == '__main__':
    left_nums, right_nums = get_left_and_right_nums_sorted('input.txt')

    assert len(left_nums) == len(right_nums)

    print('part 1: ' + str(part_1(left_nums, right_nums)))
    print('part 2: ' + str(part_2(left_nums, right_nums)))
