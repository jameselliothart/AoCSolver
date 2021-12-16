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

@dataclass(frozen=True)
class Fish:
    timer: int

    @staticmethod
    def new():
        return Fish(8)

    @staticmethod
    def mature():
        return Fish(6)


def pass_day(fish: Fish):
    if fish.timer > 0:
        yield Fish(fish.timer - 1)
    else:
        yield Fish.new()
        yield Fish.mature()


def pass_days(fishes: list[Fish], stopping_day: int, current_day: int):
    if current_day == stopping_day:
        return fishes
    new_fishes = list(chain(*(pass_day(fish) for fish in fishes)))
    return pass_days(new_fishes, stopping_day, current_day + 1)


def part_one(data):
    fish_string, *_ = data
    fishes = [Fish(int(x)) for x in fish_string.split(',')]
    return len(pass_days(fishes, 80, 0))


def part_two(data):
    pass


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    print(f'Part 2: {part_two(DATA)}')
