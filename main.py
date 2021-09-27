
from support import ggl_work, json_work, parser


def sber(ids):
    pars = parser.PareserSber()
    pars.main(ids)


def tek(url, ids):
    x = parser.PareserTektorg()
    x.main(url, ids)


def b2b_center(url, ids):
    x = parser.PareserB2Bcenter()
    x.main(url, ids)


def etpgpb(url, ids):
    x = parser.PareserEtpgpb()
    x.main(url, ids)


def get_ids(col='B'):
    """ полачаем список id из гугла """
    # Настройки
    config = json_work.JsonWork().open_json('res\setting.json')
    sheet_name = config['table_name']
    # Получение таблицы
    g = ggl_work.GoogleSheet(config)
    col_id = g.get_col_values(sheet_name, col)
    col_id = list(map(list, zip(*col_id)))[0]
    return col_id


def google():
    """ Гугл """
    print('---- google ----')
    # Настройки
    config = json_work.JsonWork().open_json('res\setting.json')
    sheet_name = config['table_name']
    # Получение таблицы
    g = ggl_work.GoogleSheet(config)
    row_tag = g.get_row_values(sheet_name, 2)
    col_id = g.get_col_values(sheet_name, col='B')
    col_id = list(map(list, zip(*col_id)))[0]

    dir_lots = json_work.JsonWork().open_json('temp.json')
    for lot in dir_lots['lots']:
        id = lot['id']
        if id not in col_id:
            lot_date = []
            for tag in row_tag:
                if tag in lot:
                    lot_date.append(lot[tag])
                else:
                    lot_date.append('-')
            # Запись
            g.insert_row(sheet_name, lot_date)


if __name__ == '__main__':
    # список ID
    ids = get_ids()

    # www.sberbank-ast.ru
    sber(ids)
    # www.tektorg.ru/sale
    url_ts = 'https://www.tektorg.ru/procedures?q=%D0%BB%D0%BE%D0%BC&section_id=4&status=328%3B288%3B346%3B347%3B261%3B268%3B246%3B256%3B266%3B267%3B212%3B222%3B243%3B314%3B316%3B191%3B201%3B210%3B318%3B186%3B187%3B21%3B22%3B11%3B12%3B0%3B1%3B2%3B175%3B179%3B245%3B239%3B321%3B230&lang=ru&sort=datestart&order=desc&limit=500'
    tek(url_ts, ids)
    # www.tektorg.ru
    url_t = 'https://www.tektorg.ru/procedures?q=%D0%BB%D0%BE%D0%BC+%D0%BC%D0%B5%D1%82%D0%B0%D0%BB%D0%BB&status=328%3B288%3B346%3B347%3B261%3B268%3B246%3B256%3B266%3B267%3B212%3B222%3B243%3B314%3B316%3B191%3B201%3B210%3B318%3B186%3B187%3B21%3B22%3B11%3B12%3B0%3B1%3B2%3B175%3B179%3B245%3B239%3B321%3B230&lang=ru&sort=datestart&order=desc&limit=500'
    tek(url_t, ids)
    # www.b2b-center.ru
    url_b = 'https://www.b2b-center.ru/market/?f_keyword=%D0%BB%D0%BE%D0%BC&searching=1&map_country%5B0%5D=643_d7&map_country%5B1%5D=643_d6&company_type=2&price_currency=0&date=1&trade=all#search-result'
    b2b_center(url_b, ids)
    # etpgpb.ru
    url_e = 'https://etpgpb.ru/procedures/?procedure%5Bcategory%5D=actual&search=%D0%BB%D0%BE%D0%BC&sort=by_published_desc'
    etpgpb(url_e, ids)

    # Заполняем таблицу
    google()
