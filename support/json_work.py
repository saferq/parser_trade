import json
from json import encoder
from json.decoder import JSONDecodeError
from os import name


class JsonWork():
    '''  '''

    def __init__(self):
        '''  '''
        self.json = json

    def open_json(self, file_name):
        ''' Открытие json файл '''
        empty_json = '{}'
        with open(file_name, "r", encoding='utf8') as read_file:
            try:
                data = self.json.load(read_file)
                if data == None:
                    data = self.json.loads(empty_json)    
            except JSONDecodeError:
                data = self.json.loads(empty_json)

        return data

    def save_json(self, file_name, data):
        ''' Сохранение в json файл '''
        try:
            with open(file=file_name, mode="w", encoding='utf8') as write_file:
                self.json.dump(data, write_file, ensure_ascii=False, indent=2)
        except TypeError:
            print(f"TypeError: {data}")

    

    def add_value_list(self, date_json, category, id, key, value):
        # Проверка наличия категории
        if category not in date_json:
            # Новая лот в новой категория')
            date_json[category] = []
            date_json[category].append({
                'id': id,
                key: value
            })
        else:
            # Цикл по существующим лотам
            id_list = []
            for lot in date_json[category]:
                id_list.append(lot['id'])
                # обновление по id
                if lot['id'] == id:
                    lot[key] = value
            # Новый id
            if id not in id_list:
                date_json[category].append({
                    'id': id,
                    key: value
                })
        return date_json


if __name__ == '__main__':
    j = JsonWork()

    file_name = 'test.json'
    # open
    test_dir = j.open_json(file_name)
    # work
    # j.add_value_list(
    #     test_dir,
    #     category='lots',
    #     id='url1',
    #     key='Название',
    #     value='Каратышки1'
    # )
    # j.add_value_list(
    #     test_dir,
    #     category='lots',
    #     id='url3',
    #     key='Привет',
    #     value='Пока'
    # ) 
    j.add_value_list(
        test_dir,
        category='lots',
        id='url4',
        key='Адрес',
        value='ул. kjshd'
    )

    # save
    j.save_json(file_name, test_dir)
