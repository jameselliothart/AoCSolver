import shared

sample = [

]


def main():
    file_name = '1.txt'
    data = sample
    data = [int(x) for x in shared.get_data(file_name)]


if __name__ == '__main__':
    main()
