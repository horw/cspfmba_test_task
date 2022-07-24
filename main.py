from typing import List, Dict
import json
import datetime

'''
Среди покупателей провели опрос —
какие товары они считают наиболее «интересными» для себя.
На выбор предлагалось 5 различных
вариантов фильтра:
'''


def json_date_hook(json_dict):
    if 'date' in json_dict.keys():
        try:
            json_dict['date'] = datetime.datetime.strptime(json_dict['date'],
                                                           "%d.%m.%Y")
        except ValueError as e:
            print(e)
            pass
    return json_dict


def get_file_json(file_name: str) -> List[Dict]:
    with open(file_name, 'r') as read_stream:
        data = json.loads(read_stream.read(), object_hook=json_date_hook)
    return data


#«Наименование товара содержит подстроку в любом регистре» (внутренний ключ ‘NAME_CONTAINS’)
def substring_filter(substring: str, products_list: List[Dict]):
    assert isinstance(substring, str) and len(substring) in range(1, 101)
    for product in products_list:
        if product_name := product.get('name'):
            if substring.lower() in product_name.lower():
                yield product


#«Цена больше или равна чем» (внутренний ключ ‘PRICE_GREATER_THAN’);
def greater_than_price_filter(compare_price: int, products_list: List[Dict]):
    compare_price = int(compare_price)

    assert compare_price in range(0, 2**31)
    for product in products_list:
        if product['price'] >= compare_price:
            yield product


#«Цена меньше или равна чем» (внутренний ключ ‘PRICE_LESS_THAN’);
def lower_than_price_filter(compare_price: int, products_list: List[Dict]):
    compare_price = int(compare_price)
    assert compare_price in range(0, 2**31)
    for product in products_list:
        if product['price'] <= compare_price:
            yield product


#«Товар поступил в продажу не позднее» (внутренний ключ ‘DATE_BEFORE’);
def arrive_before_filter(arrived_date: str, products_list: List[Dict]):
    try:
        arrived_date = datetime.datetime.strptime(arrived_date, "%d.%m.%Y")
    except ValueError as e:
        return {'error': 'got invalid date value'}
    assert datetime.datetime(1970, 1, 1) <= arrived_date <= datetime.datetime(2070, 12, 31)
    for product in products_list:
        # if product's date smaller than arrived date, then return it
        if arrived_date >= product['date']:
            yield product


#«Товар поступил в продажу не ранее» (внутренний ключ ‘DATE_AFTER’);
def arrive_after_filter(arrived_date: str, products_list: List[Dict]):
    try:
        arrived_date = datetime.datetime.strptime(arrived_date, "%d.%m.%Y")
    except ValueError as e:
        return {'error': 'got invalid date value'}
    assert datetime.datetime(1970, 1, 1) <= arrived_date <= datetime.datetime(2070, 12, 31)
    for product in products_list:
        if arrived_date <= product['date']:
            yield product


def generate_random_products() -> List[Dict]:
    print('Generate random products')
    from random import randrange, choices
    import string
    for i in range(1000):
        yield {'id': i,
               'name': ''.join(choices(string.ascii_letters, k=randrange(5, 20))),
               'price': randrange(100, 10000),
               'date': f'{randrange(10,20)}.{randrange(1, 12):02d}.{randrange(2000,2020)}'
               }


if __name__ == '__main__':
    filters = {
        'NAME_CONTAINS': substring_filter,
        'PRICE_GREATER_THAN': greater_than_price_filter,
        'PRICE_LESS_THAN': lower_than_price_filter,
        'DATE_BEFORE': arrive_before_filter,
        'DATE_AFTER': arrive_after_filter
    }

    #Первая строка входных данных содержит список товаров в формате JSON
    products_json_str = json.dumps(
        list(generate_random_products())
    )
    # Следующие 5 строк имеют вид qivi — фильтр и соответствующее ему актуальное значение
    INPUT_VALUE = f"""{products_json_str}
        NAME_CONTAINS A
        PRICE_LESS_THAN 6000
        PRICE_GREATER_THAN 1000
        DATE_BEFORE 10.10.2019
        DATE_AFTER 10.10.2010"""

    PRODUCTS_DATA, *commands = [line.strip() for line in INPUT_VALUE.split('\n')]
    PRODUCTS_DATA = json.loads(PRODUCTS_DATA, object_hook=json_date_hook)
    print(f'Initialized product list: {PRODUCTS_DATA}\n')

    #Каждый товар должен быть выведен ровно один раз в отсортированном по возрастанию id порядке, sorted by id
    out_product_list: List[Dict] = sorted(PRODUCTS_DATA, key=lambda product: product['id'])
    for command in commands:
        print(f'Command:\n'
              f'  {command}')
        command, control = command.split(' ')
        out_product_list = list(filters[command](control, out_product_list))
        print(f'Result:\n'
              f'  Product list len: {len(out_product_list)}\n'
              f'  Product list {out_product_list}\n')

    #datetime to str
    for product in out_product_list:
        product['date'] = product['date'].strftime("%d.%m.%Y")
    print(f'OUTPUT_VALUES:\n'
          f'{out_product_list}')

