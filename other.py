from support import parser
from support import json_work
from support import ggl_work
from pprint import pprint


def main():
    pr = parser.PareserLom()
    urls = [
        'https://utp.sberbank-ast.ru/AP/NBT/PurchaseView/13/0/0/783591',
        'https://utp.sberbank-ast.ru/AP/NBT/PurchaseView/13/0/0/783577',
        'https://utp.sberbank-ast.ru/AP/NBT/PurchaseView/13/0/0/770646',
        'http://utp.sberbank-ast.ru/AP/NBT/PurchaseView/9/0/0/776681',
        'http://utp.sberbank-ast.ru/AP/NBT/PurchaseView/13/0/0/777374',
        'https://utp.sberbank-ast.ru/VIP/NBT/PurchaseView/43/0/0/778979',
        'https://utp.sberbank-ast.ru/Transneft/NBT/PurchaseView/43/0/0/774848',
        'http://www.sberbank-ast.ru/purchaseview.aspx?id=8335002',
        'http://www.sberbank-ast.ru/OK/purchaseview.aspx?id=8334336',
        'https://sberb2b.ru/request/supplier/preview/17cd063d-f9cb-454d-a32b-ccebcac902b9',
        'http://sberb2b.ru/request/supplier/preview/3d14f21c-6771-4340-a0d1-0cb1562ff590'
    ]

    for url in urls:
        print(url)
        category = 'lots'
        if 'PurchaseView' in url:
            print('PurchaseView')
            # pr.parse_type_1(url, category)
        elif 'purchaseview' in url:
            print('purchaseview')
            # pr.parse_type_2(url, category)
        elif 'sberb2b.ru' in url:
            print('sberb2b.ru')
            pr.parse_sberb2b(url, category)
        else:
            print('other')


def google_test():
    """ Гугл """
    print('---- google ----')
    # Настройки
    config = json_work.JsonWork().open_json('res\setting.json')
    sheet_name = config['table_name']
    # Получение таблицы
    g = ggl_work.GoogleSheet(config)
    row_tag = g.get_row_values(sheet_name, 2)

    dir_lots = json_work.JsonWork().open_json('temp.json')
    for lot in dir_lots['lots']:
        lot_date = []
        for tag in row_tag:
            if tag in lot:
                lot_date.append(lot[tag])
            else:
                lot_date.append('---')
        # Запись
        g.insert_row(sheet_name, lot_date)


if __name__ == '__main__':
    # main()
    google_test()
