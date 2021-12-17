from itertools import chain
from dataclasses import dataclass
import os
import file_io

sample = [
    '3,4,3,1,2'
]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


@dataclass
class Fish:
    days_left: int
    timer: int = 8


def num_offspring(timer, days_left, so_far):
    if days_left - timer <= 0:
        return so_far
    if timer != 6:
        return num_offspring(6, days_left - timer - 1, 1)
    return (days_left // (timer + 1)) + so_far


def get_offspring(fish: Fish):
    if fish.timer + 1 > fish.days_left:
        return []
    first_offspring_days_left = fish.days_left - fish.timer - 1
    offspring = [Fish(days_left)
                 for days_left in range(first_offspring_days_left, -1, -7)]
    return offspring


def count_lineage_of(fish: Fish):
    offspring = get_offspring(fish)
    return len([fish]) + sum(count_lineage_of(f) for f in offspring)


def part_one(data):
    fish_string, *_ = data
    fishes = [Fish(80, int(x)) for x in fish_string.split(',')]
    return sum(count_lineage_of(fish) for fish in fishes)


def part_two(data):
    fish_string, *_ = data
    fishes = [Fish(256, int(x)) for x in fish_string.split(',')]
    return sum(count_lineage_of(fish) for fish in fishes)


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    # print(f'Part 2: {part_two(DATA)}')
