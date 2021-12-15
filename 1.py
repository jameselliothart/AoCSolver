import file_io

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


class SlidingWindow():
    def __init__(self, iterable, window_size=3):
        self._window_size = window_size
        self._iterable = iterable
        self._index = 0
        self._stop = False

    def __iter__(self):
        return self

    def __next__(self):
        if self._stop:
            raise StopIteration
        item = sum(
            self._iterable[self._index:self._index + self._window_size])
        self._index += 1
        if len(self._iterable[self._index:]) < 3:
            self._stop = True
        return item


def main():
    file_name = '1.txt'
    data = sample
    data = [int(x) for x in file_io.get_data(file_name)]
    print(increases(get_comparer(list(SlidingWindow(data)))))


if __name__ == '__main__':
    main()
