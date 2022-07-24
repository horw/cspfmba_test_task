# cspfmba_test_task
Two test task from cspfmba comp

RU:
1.	Необходимо вывести самую популярную категорию товаров

Решение:
1. Создадим необходимые таблицы с помощью предложенных команд.


2. Объединим необходимые поля таблиц с помошью INNER JOIN для того, чтобы избежать NULL категории и NULL продуктов: обрабатываем существущие категории с существующими продуктами.

2.1 Заказы с товарами по внешнему ключу goods_id<br />
  INNER JOIN goods ON goods.goods_id = orders.goods_id 
  
2.2 Категории с товарами по внешему ключу goods_type_id<br />
  INNER JOIN goods_type ON goods.goods_type_id = goods_type.goods_type_id 
  
2.3 Итоговая комманда для итоговой таблица:<br />
  SELECT *  FROM orders <br />
  INNER JOIN goods ON goods.goods_id = orders.goods_id <br />
  INNER JOIN goods_type ON goods.goods_type_id = goods_type.goods_type_id <br />


3. Чтобы посчитать сумму товаром по категориям необходимо выполнить GROUP BY по полю goods_type_id, добавим необходимый столбец в итоговую таблицу и запишим как "category_sum":<br />
  SUM(goods_type.goods_type_id) as category_sum


4.Для того, чтобы получить наиболее популярную категорию выполним сортировку - ORDER BY ... DESC, а для вывода первой строки ограничем вывод LIMIT 1:
<br />
SELECT goods_type.goods_type_name, SUM(goods_type.goods_type_id) as category_sum FROM orders <br />
INNER JOIN goods ON goods.goods_id = orders.goods_id <br />
INNER JOIN goods_type ON goods.goods_type_id = goods_type.goods_type_id <br />
GROUP BY goods_type.goods_type_id ORDER BY category_sum DESC LIMIT 1

5. Итог: Для заданого примера Топ-1 категорией является cookie, с количеством 12 шт.
