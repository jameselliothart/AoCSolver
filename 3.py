import os
from functools import partial
import shared

sample = [
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010',
]


def transpose(matrix):
    return map(list, zip(*matrix))


def sum_columns(matrix):
    return list(map(lambda xs: sum(int(x) for x in xs), transpose(matrix)))


def get_gamma_epsilon_binary(matrix):
    mid_point = len(matrix) / 2
    column_sums = sum_columns(matrix)
    return {
        'gamma': ''.join('1' if sum >= mid_point else '0' for sum in column_sums),
        'epsilon': ''.join('0' if sum >= mid_point else '1' for sum in column_sums)
    }


def power_consumption(gamma_epsilon):
    return int(gamma_epsilon['gamma'], 2) * int(gamma_epsilon['epsilon'], 2)


def main():
    file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
    data = sample
    data = shared.get_data(file_name)
    print(power_consumption(get_gamma_epsilon_binary(data)))


def sum_column(index, matrix):
    return sum(int(row[index]) for row in matrix)


def criteria(comparer, bit_position, matrix):
    column_length = len(matrix)
    column_sum = sum_column(bit_position, matrix)
    return (
        [row for row in matrix if row[bit_position] == '1']
        if comparer(column_sum, column_length)
        else [row for row in matrix if row[bit_position] == '0']
    )


def rating(criteria, matrix, bit_position):
    [candidate, *others] = criteria(bit_position, matrix)
    return candidate if len(others) == 0 else rating(criteria, [candidate] + others, bit_position + 1)


oxygen_criteria = partial(criteria, lambda column_sum,
                          column_length: column_sum >= column_length/2)
oxygen_rating = partial(rating, oxygen_criteria)
co2_criteria = partial(criteria, lambda column_sum,
                       column_length: column_sum < column_length/2)
co2_rating = partial(rating, co2_criteria)


def main2():
    file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
    data = sample
    data = shared.get_data(file_name)
    (oxygen, co2) = (oxygen_rating(data, 0), co2_rating(data, 0))
    print(int(oxygen, 2) * int(co2, 2))


if __name__ == '__main__':
    main2()
