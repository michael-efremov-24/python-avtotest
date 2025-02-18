# python-avtotest
Программа получает на вход строку одного из двух видов:
-H https://*****.***,https://*****.***,... -C * -O **** или -F ***** -C * -O *****
Ключи -C и -F используются необязательно.
Первое, что делает программа после получения входной строки - определяет местоположение ключей -H, -C, -F, -O в ней (строки 40 - 43). Ключи во входной строке могут быть записаны в любом порядке.
Далее программа производит ряд проверок входных данных. 
1. Сначала функцией Proverka_probelov осуществляется проверка на наличие в строке лишних пробелов, или ох отсутствие в нужных местах.
Пробелы могут быть только до и после ключей. Между ключом и его содержимым ровно один пробел:

данные/пробел/-КЛЮЧ/пробел/данные

Работает функция следующим образом: в неё передаётся входная строка и список из индексов ключей. Далее функция пробегает по списку индексов ключей, которые есть во входной строке (их индекс не равен -1) и условием в строке 30 проверяет, что между ключом и его содержимым ровно один пробел справа.
Далее она пробегает по всей строке, ищет в ней пробелы и условием 34 проверяет, что для каждого пробела существует хотя бы один ключ, от которого этот пробел "удалён" не более чем на 2 по модулю.
Такая проверка отметает например случаи, когда пользователь случайно поставит пробел вместо "," при перечислении хостов:

-H https://ya.ru, https://apple.com -C 10

чего по условию быть не должно.
2. Далее в строках 46 - 51 отметаются входные данные, где присутствуют оба входных ключа -F и -H, или они оба отсутствуют. По условию должен быть только один из этих двух ключей.
3. В строках 52 - 60 рассматривается случай, когда есть входной ключ -H. У входной строки обрезается начало до ключа -H, включая его самого. Далее в полученной строке ищется пробел, который означает окончание перечисления хостов. Лишних пробелов нет, ранее проверили. Хвост строки после этого пробела отрезается. Из полученного среза делается список строк Hosts_list делением по ",". Отдельно рассматривается случай (строка 57), когда ключ -H идёт последним и тогда просто строка делится по ",".
Для строк из списка Hosts_list вызывается функция Proverka_adresov. Она проверяет их на соответствие формату https://*****.******
Работает следующим образом: проверяет, что начало строки имеет вид https:// ; затем отрезает от исходной строки https:// и ищет в срезе точку-разделитель. Если её нет, возвращает ЛОЖЬ. Затем пробегает по обрезку до этой точки, проверяя, что символы допустимые (условие 15). Затем пробегает от точки до конца строки и условием 21 проверяет, что после точки все символы также допустимые.
4. В строках 61 - 75 рассматривается случай, когда имеется ключ -F. По описанному в пункте 3 алгоритму из входной строки извлекается имя файла с входными данными. Производится открытие файла, возможные ошибки обрабатываются блоками try/except (строки 65 - 69). В случае успешного открытия файла его содержимое считывается и также записывается в список Hosts_list. Производится проверка адресов в Hosts_list.
5. Далее работаем с ключом C. Если его нет (индекс равен -1), присваиваем ему значение -1. Если он есть по описанному выше алгоритму из строки входных данных извлекается подстрока, содержащая С. Методом isdigit() проверяется, что все её символы - цифры, то есть C действительно натуральное число.
6. Далее идёт выполнение основного блока заданий. Рассматриваются два случая - когда входного ключа -O нет (строки 90 - 121), и когда он есть (строки 123 - 174).
Используется библиотека requests. Последовательно выполняются C запросов на каждый из указанных адресов (строки 99 - 105). Возможные ошибки при открытии страницы обрабатываются блоками try/except. Замеряется время выполнения каждого запроса. Переменные-счётчики (Success, Failed, Error) считают количество интересующих статус кодов - Success считаются через .ok, в Failed по условию считаются запросы со статус кодом 400 или 500, и в Error с кодом 503, что означает "Сервер недоступен". Стандартными алгоритмами определяются минимальное, максимальное и среднее время запроса. Всё выводится на экран. 
В случае, если указан ключ -O также из строки входных данных извлекается имя файла и запись производится в него. В случае неудачного открытия Python автоматически создаст файл с указанным названием.

ПРИМЕР:
Вход: -H https://ya.ru,https://google.com,https://apple.com -C 10

Вывод:
a.  https://ya.ru
b. Success =  10
c. Failed =  0
d. Errors =  0
e. Min =  0.2422872000024654
f. Max =  0.5370018999674357
g. Avg =  0.32712088999105615


a.  https://google.com
b. Success =  10
c. Failed =  0
d. Errors =  0
e. Min =  0.6310163000016473
f. Max =  0.6823413000092842
g. Avg =  0.6571971699944698


a.  https://apple.com
b. Success =  10
c. Failed =  0
d. Errors =  0
e. Min =  0.5444892000523396
f. Max =  0.636355199967511
g. Avg =  0.5711467699962668
