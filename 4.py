from dataclasses import dataclass
import os
from typing import List
import file_io

sample = [
    '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1',
    '',
    '22 13 17 11  0',
    ' 8  2 23  4 24',
    '21  9 14 16  7',
    ' 6 10  3 18  5',
    ' 1 12 20 15 19',
    '',
    ' 3 15  0  2 22',
    ' 9 18 13 17  5',
    '19  8  7 25 23',
    '20 11 10 24  4',
    '14 21 16 12  6',
    '',
    '14 21 17 24  4',
    '10 16 15  9 19',
    '18  8 23 26 20',
    '22 11 13  6  5',
    ' 2  0 12  3  7',
]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


@dataclass
class Tile:
    value: int
    marked: bool = False

    def mark(self): self.marked = True


class Board:
    def __init__(self, rows: List[List[Tile]]):
        self.rows = rows

    def mark(self, number):
        for row in self.rows:
            for tile in row:
                if tile.value == number:
                    tile.mark()

    def is_winner(self):
        return (
            any(all(tile.marked for tile in row) for row in self.rows)
            or
            any(all(tile.marked for tile in col) for col in zip(*self.rows))
        )

    def sum_unmarked(self):
        return sum(sum(tile.value for tile in row if not tile.marked) for row in self.rows)


def get_numbers(data) -> List[int]:
    return [int(x) for x in data.split(',')]


def get_boards(data):
    if data[-1] != '':
        data += ['']
    rows = []
    for line in data:
        if len(line) > 0:
            rows += [[Tile(int(x)) for x in line.split()]]
        else:
            yield Board(rows)
            rows = []


def play(boards: List[Board], numbers: List[int]):
    for number in numbers:
        for board in boards:
            board.mark(number)
        winners = [board for board in boards if board.is_winner()]
        if any(winners):
            return winners[0].sum_unmarked(), number, winners[0].sum_unmarked() * number
    return None


def part_one(data):
    [raw_numbers, _, *raw_boards] = data
    numbers = get_numbers(raw_numbers)
    boards = list(get_boards(raw_boards))
    return play(boards, numbers)


def play_two(boards: List[Board], numbers: List[int]):
    for number in numbers:
        for board in boards:
            board.mark(number)
        boards = [board for board in boards if not board.is_winner()] if len(boards) > 1 else boards
        if len(boards) == 1 and boards[0].is_winner():
            return boards[0].sum_unmarked(), number, boards[0].sum_unmarked() * number
    return None


def part_two(data):
    [raw_numbers, _, *raw_boards] = data
    numbers = get_numbers(raw_numbers)
    boards = list(get_boards(raw_boards))
    return play_two(boards, numbers)


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    print(f'Part 2: {part_two(DATA)}')
