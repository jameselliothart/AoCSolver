import os
import file_io

sample = [
    '16,1,2,0,4,2,7,1,2,14'
]

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


def cost_to_move(starting: int, end: int):
    return abs(starting - end)


def get_fuel_costs(cost_fn, positions: list[int], destination: int):
    return [cost_fn(position, destination) for position in positions]


def total_cost(fuel_costs: list[int]):
    return sum(fuel_costs)


def solve(cost_fn, data):
    [positions_raw, *_] = data
    positions = [int(p) for p in positions_raw.split(',')]
    possibilities = [
        (destination, total_cost(get_fuel_costs(cost_fn, positions, destination)))
        for destination in range(max(positions) + 1)
    ]
    return min(possibilities, key=lambda x: x[1])


def part_one(data):
    return solve(cost_to_move, data)


def cost_to_move_two(starting: int, end: int):
    distance = abs(starting - end)
    return (distance * (distance + 1)) / 2


def part_two(data):
    return solve(cost_to_move_two, data)


if __name__ == '__main__':
    print(f'Part 1: {part_one(DATA)}')
    print(f'Part 2: {part_two(DATA)}')
