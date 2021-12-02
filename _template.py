import shared
import os

sample = [

]


def main():
    file_name = f'{os.path.basename(__file__).split(".")[0]}.txt'
    data = sample
    data = [int(x) for x in shared.get_data(file_name)]


if __name__ == '__main__':
    main()
