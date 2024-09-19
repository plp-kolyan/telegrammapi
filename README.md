telegrammapi - это контсруктор телеграмм ботов главным образом заточенным на взаимодействие бота и стороннего api
домонтстрацию можно посмотреть https://youtu.be/SXaFrHVehCs?si=aqTZa_JFobeVkBxd
Видео с установкой и настройкой по этому мануалу тут https://youtu.be/VxQZo9DOUT8?si=4woGTdGEnSFj2OAd

для работу нужен python и pycharm
Установка python и pycharm https://www.youtube.com/watch?v=yBE4tw8uBic


Создать новый проект в pycharm c виртуальным окружением, если ты новичёк создавай на диске C папку telegrammapi чтобы получился путь в проект 
C:\telegrammapi - это поможет избежать лишних мучений на пути установки

скачать архив проекта из гитхаба https://github.com/plp-kolyan/telegrammapi/tree/master 
(или сделать клон если умеешь) если не умеешь пользоваться git просто качай архив
разорхивировать проект в корень чтобы получилась такая структура 

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_1.jpg)

Все вышеперечисленные действия сводятся к тому чтобы повторить структуру проекта на картинке, если структура такая то следуй дальше, если нет то перености файлы из архива так чтобы всё было как на картинке

Обновить пип в виндовс в терминале и установить все зависимости, если эта фраза ни о чем не говорит просто делай так как написанно
Терминал это вот, в красном прямоугольнике должно быть (venv) значит созданно виртуальное окружение и оно активно, если этого нет, самый простой способ его поставить просто удалить папку и сделать создание проекта в точности как на видео https://youtu.be/yBE4tw8uBic?si=h9a7oMPSUrJwP1nM&t=161:

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_6.jpg)


    python.exe -m pip install --upgrade pip
    pip install -r requirements.txt

Далее если все установилось нормально, а оно по другому быть не может вводи в терминал:

    pip list
    
должно выйти зависимости среди которых обязательно должны быть:

    Django     5.1
    Jinja2     3.1.4
    Telethon   1.36.0
    aiodns     3.2.0
    aiohttp    3.10.5

Помимо этого будут и другие библиотеки поэтому всё что выше будет в перемешку с другими, но особое внимание надо обратить на зависимости изображение на которые находятся над этим текстом

После этого
В папке message создать папку python package под названием migrations просто пустая папка


![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_2.jpg)



В папке message, создаём serveses_config.py с содержимым 

    api_id = 0
    api_hash = ''
    bot_token = ''
    sender_id = 0
    headers = {'Authorization': 'ваш токен'}
    url = 'http://ваш ip  или домен/api/ензоинд'

sender_id - Куда будет пересылаться сообшение (в начале пишем 0, позже будет написанно откуда его взять)в случе если в answer указанно что сообшение нужнно пересылать - это пока временный механизм который будет переделан на более обширные правила переотправки
как получить api_id и api_hash есть в видео https://www.youtube.com/watch?v=mLOYMg1lJJU&t=328s
bot_token получаем в https://t.me/BotFather (БотФазер) 

    /start
    /newbot

Водим всё что просим бот и по итогу получаем от него сообщение с Use this token to access the HTTP API:, вот этот токен и есть bot_token

headers, url = нужно для тестирования ip если их нет, то есть вы не предусматриваете отправку по апи и тестирование этой отправки можно заполнить как в примере, все равно эти данные использоваться нигде не будут, но если их нет они сломают импорт

Обращаю внимание (api_id, api_hash, bot_token, sender_id, headers, url) должны быть обязательно в этом файле может пустые не запонениые но обязательно нужно их определить

Затем выполняем

    python manage.py makemigrations
    python manage.py migrate

Если где то что то выдает ошибки пишите в комментариях на ютуб под видео к боту

Если всё ОК, то создаем пользователя для входа в админку
    python manage.py createsuperuser

Имя пользователя admin
Адрес электронной почты: можно пропустить нажать enter
далее пароль подтверждения если выходит предупреждения на всё соглашаемся

После выполняем
    python manage.py runserver 

далее идем http://127.0.0.1:8000/admin вводим логин и пароль


Теперь создадим первый сценарий, напишем ответ на сообщение старт
http://127.0.0.1:8000/admin/message/answer/ добавляем запись 
Заполняем Текст сообщения:

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_3.jpg)

И Скроллим до Client messages добавляем /start

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_4.jpg)

Далее в каталоге message в файле tests.py нажимаем на test_2

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_5.jpg)


после этого должен запустится бот и на каждый /start будет отвеченно сообщением из answer, тоесть этот привет который мы сейчас написали
На этом первоначальная настройка бота завершена

Настройка бота


![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_7.jpg)

Самый простой пример для обращения бота по api показывает индекс цен на биткоин (BPI) в режиме реального времени.

1) Протестируйте api запустите async def test_18(self):

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_10.jpg)
    В случае успеха должно быть что-то подобное этот шаг можно пропустить и вернуться к нему если не получается 
    получить ответ в самом боте, при помощи этого теста можно получить больше информации в случае провала чем в
    самом боте

2) Далее идем answer - находится вот здесь http://127.0.0.1:8000/admin/message/answer/ добавляем новую запись

    Текст сообщения заполняем вот так {{response_json}}

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_9.jpg)

    Создаем ответ из api

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_13.jpg)

    Название метода - придумываем любое, это просто название для себя чтобы было понятно что этот метод делает
    Url: пишем https://api.coindesk.com/v1/bpi/currentprice.json
    Метод: get, жмем сохранить

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_14.jpg)

    Скролим до /Bitcoin - это команда которая будет триггерить этот answer при ее вводе пользователем в боте
    
    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_12.jpg)

    Жмем сохранить

3) Запускаем бот если он не запущен

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_5.jpg)

4) Ввводим в боте /Bitcoin и получаем 

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_16.jpg)

5) Теперь сделаем вывод более человекочитаемым
    Текст сообщения заполняем вот так:
    {% for usd in response_json.bpi.USD %}
    {{usd}}: {{response_json.bpi.USD[usd]}}
    {% endfor %}
    Чтобы повторить /Bitcoin

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_16.jpg)

    Ввводим в боте /Bitcoin и получаем

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_17.jpg)


Для того чтобы настроить бот для работы с аpi протестируем api:
1) прописать в serveses_config.py данные для вашего api, 
    headers = {'Authorization': 'Token ****************************************'}
    url = 'http://1**.***.**.***:8000/api/results_operator_on_tables'
    если аpi не требует авторизациии ставим headers = {}
2) в файле tests.py находим async def test_17(self):

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_10.jpg)
    
    в данном примере payload заполнен {"date_gte": "12.09.2024", "date_lte": "13.09.2024"}, указан method = 'get', 
    в этом случае payload передастся как параметры к запросу, если post то payload будет передан как json
    Естественно у вас headers, url, payload и method должны быть выбранны в соответствии с вашим api 
3) Запускаем тест и видим результат

    ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_11.jpg)
    Если всё делать правильно должно получиться так, вот тут на картинке вернулись данные с которыми можно будет 
    работать в боте


Прежде чем настроить api уже в самом боте необходимо собрать полезную нагрузку(payload) из диалога пользователя и бота
полезную нагрузку можно собирать двумя способами:
1) Получать данные из текстового ввода пользователя
2) Получать данные из кнопок которые выбирает пользователь

