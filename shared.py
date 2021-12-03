def get_data(file_name):
    with open(f'data/{file_name}', encoding='utf8') as f:
        return [line.strip() for line in f.readlines()]
