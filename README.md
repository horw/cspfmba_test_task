# cspfmba_test_task
Two test task from cspfmba comp

RU:
<h1>
  1.	Необходимо вывести самую популярную категорию товаров
</h1>
<h2>Решение:</h2>
<div>
1. Создадим необходимые таблицы с помощью предложенных команд.
</div>
</br>
<div>
2. Объединим необходимые поля таблиц с помошью INNER JOIN для того, чтобы избежать NULL категории и NULL продуктов: обрабатываем существущие категории с существующими продуктами.
</div>
</br>
<div>
2.1 Заказы с товарами по внешнему ключу goods_id<br />
  <b>INNER JOIN goods ON goods.goods_id = orders.goods_id</b>
</div>
</br>
<div>
2.2 Категории с товарами по внешему ключу goods_type_id<br />
  <b>INNER JOIN goods_type ON goods.goods_type_id = goods_type.goods_type_id</b>
</div>
</br>
<div>
2.3 Итоговая комманда для итоговой таблица:<br />
  <b>SELECT *  FROM orders <br />
  INNER JOIN goods ON goods.goods_id = orders.goods_id <br />
  INNER JOIN goods_type ON goods.goods_type_id = goods_type.goods_type_id <br /></b>
</div>
</br>
<div>
3. Чтобы посчитать сумму товаром по категориям необходимо выполнить GROUP BY по полю goods_type_id, добавим необходимый столбец в итоговую таблицу и запишим как "category_sum":<br />
   <b>SUM(goods_type.goods_type_id) as category_sum</b>
</div>
</br>
<div>
4.Для того, чтобы получить наиболее популярную категорию выполним сортировку - ORDER BY ... DESC, а для вывода первой строки ограничим вывод LIMIT 1:
<br />
 <b>
  SELECT goods_type.goods_type_name, SUM(goods_type.goods_type_id) as category_sum FROM orders <br />
  INNER JOIN goods ON goods.goods_id = orders.goods_id <br />
  INNER JOIN goods_type ON goods.goods_type_id = goods_type.goods_type_id <br />
  GROUP BY goods_type.goods_type_id ORDER BY category_sum DESC LIMIT 1
  </b>
</div>
</br>
<div>
5. Итог: Для заданого примера Топ-1 категорией является cookie, с количеством 12 шт.
<h1>2 из имеющегося списка товаров выбрать все товары, удовлетворяющие актуальным значениям всех указанных фильтров.</h1>
</div>
