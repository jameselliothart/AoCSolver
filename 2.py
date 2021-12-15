import file_io
import os
from functools import reduce
from dataclasses import dataclass, replace

sample = [
    'forward 5',
    'down 5',
    'forward 8',
    'up 3',
    'down 8',
    'forward 2',
]


@dataclass(frozen=True)
class Position:
    horizontal: int
    depth: int
    aim: int = 0


def forward(position: Position, amount):
    return replace(position, horizontal=position.horizontal + amount)


def down(position: Position, amount):
    return replace(position, depth=position.depth + amount)


def up(position: Position, amount):
    return replace(position, depth=position.depth - amount)


def forward_(position: Position, amount):
    return replace(
        replace(position, horizontal=position.horizontal + amount),
        depth=position.depth + (position.aim * amount)
    )


def down_(position: Position, amount):
    return replace(position, aim=position.aim + amount)


def up_(position: Position, amount):
    return replace(position, aim=position.aim - amount)


def position_number(position: Position):
    return position.horizontal * position.depth


@dataclass()
class Command:
    direction: str
    amount: int


def to_command(line):
    [direction, amount] = line.split(' ')
    return Command(direction, int(amount))

def move_1(position, command: Command):
    direction_to_fn = {
        'forward': forward,
        'up': up,
        'down': down,
    }
    fn = direction_to_fn[command.direction]
    return fn(position, command.amount)


def move(position, command: Command):
    direction_to_fn = {
        'forward': forward_,
        'up': up_,
        'down': down_,
    }
    fn = direction_to_fn[command.direction]
    return fn(position, command.amount)


def part_one(data):
    data = [to_command(x) for x in data]
    return position_number(reduce(move_1, data, Position(0, 0)))

def part_two(data):
    data = [to_command(x) for x in data]
    return position_number(reduce(move, data, Position(0, 0)))


if __name__ == '__main__':
    file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
    DATA = file_io.get_data(file_name)
    print(part_one(DATA))
    print(part_two(DATA))
