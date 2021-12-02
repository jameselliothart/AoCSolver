import shared

sample = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
]

def get_comparer(measurements):
    return [x[1] - x[0] for x in zip(measurements, measurements[1:])]

def increases(comparisons):
    return len([x for x in comparisons if x > 0])

if __name__ == '__main__':
    file_name = '1.txt'
    data = [int(x) for x in shared.get_data(file_name)]
    print(increases(get_comparer(data)))
    # print(shared.download(f'{file_name}.txt'))
