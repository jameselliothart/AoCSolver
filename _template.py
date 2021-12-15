import os
import file_io

sample = [

]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


def part_one(data):
    return data


def part_two(data):
    return data


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    print(f'Part 2: {part_two(DATA)}')
