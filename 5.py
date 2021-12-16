from dataclasses import dataclass
from collections import Counter
import os
import file_io

sample = [
    '0,9 -> 5,9',
    '8,0 -> 0,8',
    '9,4 -> 3,4',
    '2,2 -> 2,1',
    '7,0 -> 7,4',
    '6,4 -> 2,0',
    '0,9 -> 2,9',
    '3,4 -> 1,4',
    '0,0 -> 8,8',
    '5,5 -> 8,2',
]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


@dataclass(frozen=True)
class Point:
    x: int
    y: int


@dataclass
class VentLine:
    point_one: Point
    point_two: Point

    def is_vertical(self):
        return self.point_one.x == self.point_two.x

    def is_horizontal(self):
        return self.point_one.y == self.point_two.y


def to_vent_line(raw_line):
    [point_one, point_two] = raw_line.split(' -> ')
    [x1, y1], [x2, y2] = point_one.split(','), point_two.split(',')
    return VentLine(
        Point(int(x1), int(y1)),
        Point(int(x2), int(y2))
    )


def non_diagonal_coverage_of(line: VentLine):
    return [
        Point(x, y)
        for x in range(min(line.point_one.x, line.point_two.x), max(line.point_one.x, line.point_two.x) + 1)
        for y in range(min(line.point_one.y, line.point_two.y), max(line.point_one.y, line.point_two.y) + 1)
    ]


def part_one(data):
    vent_lines = [
        to_vent_line(line) for line in data
        if to_vent_line(line).is_horizontal() or to_vent_line(line).is_vertical()
    ]
    coverages = [non_diagonal_coverage_of(line) for line in vent_lines]
    coverage_counts = Counter(
        point for coverage in coverages for point in coverage)
    dangerous_areas = {k: v for k, v in coverage_counts.items() if v > 1}

    return len(dangerous_areas)


def inc_toward(a, b):
    if a == b:
        return b
    return a + 1 if b > a else a - 1

def move_toward(a: Point, b: Point):
    yield a
    if a == b:
        return StopIteration
    yield from move_toward(Point(inc_toward(a.x, b.x), inc_toward(a.y, b.y)), b)


def coverage_of(line: VentLine):
    return move_toward(line.point_one, line.point_two)

def part_two(data):
    vent_lines = [
        to_vent_line(line) for line in data
    ]
    coverage_counts = Counter()
    for line in vent_lines:
        coverage_counts.update(coverage_of(line))
    dangerous_areas = {k: v for k, v in coverage_counts.items() if v > 1}

    return len(dangerous_areas)


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    print(f'Part 2: {part_two(DATA)}')
