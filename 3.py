import os
import file_io

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

file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
DATA = sample
DATA = file_io.get_data(file_name)


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


def part_one(data):
    return power_consumption(get_gamma_epsilon_binary(data))


def sum_column(index, matrix):
    return sum(int(row[index]) for row in matrix)


def new_criteria(comparer):
    def criteria(bit_position, matrix):
        column_length = len(matrix)
        column_sum = sum_column(bit_position, matrix)
        return (
            [row for row in matrix if row[bit_position] == '1']
            if comparer(column_sum, column_length)
            else [row for row in matrix if row[bit_position] == '0']
        )
    return criteria


def new_rater(criteria):
    def rate(matrix, bit_position):
        [candidate, *others] = criteria(bit_position, matrix)
        return candidate if len(others) == 0 else rate([candidate] + others, bit_position + 1)
    return rate


def life_support_rating(oxygen_rating, co2_rating):
    return int(oxygen_rating, 2) * int(co2_rating, 2)


oxygen_criteria = new_criteria(lambda column_sum,
                               column_length: column_sum >= column_length/2)
rate_oxygen = new_rater(oxygen_criteria)
co2_criteria = new_criteria(lambda column_sum,
                            column_length: column_sum < column_length/2)
rate_co2 = new_rater(co2_criteria)


def part_two(data):
    (oxygen, co2) = (rate_oxygen(data, 0), rate_co2(data, 0))
    return life_support_rating(oxygen, co2)


if __name__ == '__main__':
    print(part_one(DATA))
    print(part_two(DATA))
