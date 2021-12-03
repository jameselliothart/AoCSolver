import os
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

def get_gamma_epsilon_binary(matrix):
    mid_point = len(matrix) / 2
    column_sums = list(map(lambda xs: sum(int(x) for x in xs), map(list, zip(*matrix))))
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


if __name__ == '__main__':
    main()
