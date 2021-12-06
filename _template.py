import os
import shared

sample = [

]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = shared.get_data(file_name)


def part_1(data):
    return data


def part_2(data):
    return data


if __name__ == '__main__':
    print(f'Part 1: {part_1(DATA)}')
    print(f'Part 2: {part_2(DATA)}')
