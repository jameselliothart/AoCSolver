def get_data(file_name):
    with open(f'data/{file_name}', encoding='utf8') as f:
        return f.readlines()
