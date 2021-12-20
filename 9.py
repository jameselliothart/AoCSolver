from dataclasses import dataclass
import os
import file_io

sample = [
    '2199943210',
    '3987894921',
    '9856789892',
    '8767896789',
    '9899965678',
]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


@dataclass
class Point:
    row: int
    col: int


def adjacent_points(matrix, row, column):
    adjacent = [Point(row-1, column), Point(row+1, column),
                Point(row, column-1), Point(row, column+1)]
    valid_adjacents = [
        p for p in adjacent
        if 0 <= p.row < len(matrix) and 0 <= p.col < len(matrix[p.row])
    ]
    return valid_adjacents


def point_value(matrix, point: Point):
    return int(matrix[point.row][point.col])


def risk_level_of(p_value):
    return p_value + 1


def is_low_point(matrix, row, col):
    current_value = point_value(matrix, Point(row, col))
    adjacent_values = [
        point_value(matrix, p)
        for p in adjacent_points(matrix, row, col)
    ]
    return all(current_value < adjacent for adjacent in adjacent_values)


def part_one(data):
    return sum(
        [
            risk_level_of(point_value(data, Point(row, col)))
            for row in range(len(data))
            for col in range(len(data[row]))
            if is_low_point(data, row, col)
        ]
    )


def part_two(data):
    pass


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    print(f'Part 2: {part_two(DATA)}')
