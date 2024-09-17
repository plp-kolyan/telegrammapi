
Обновить пип в виндовс
python.exe -m pip install --upgrade pip

Создать новый проект в pycharm c виртуальным окружением
скачать архив проекта из гитхаба или сделать клон если умеешь
разорхивировать проект в корень чтобы получилась такая структура 

Из корневой папки выполнить
pip install -r requirements.txt

Для проверки выполнить pip list должно выйти зависимости среди которых обязательно должны быть:

    Django     5.1
    Jinja2     3.1.4
    Telethon   1.36.0



В папке message создать папку python package под названием migrations
python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser

    Имя пользователя admin
    Адрес электронной почты: можно пропустить нажать enter

После python manage.py runserver далее идем http://127.0.0.1:8000/admin вводим логин и пароль

Далее в бот фазер получем 

в message создаём serveses_config.py с содержимым 

    api_id = 0
    api_hash = ''
    bot_token = ''
    sender_id = 0

Естественно данные должны быть заполнены 

Теперь создадим первый сценарий, напишем ответ на сообщение старт
http://127.0.0.1:8000/admin/message/answer/ добавляем запись 
Заполняем Текст сообщения:
И Скроллим до Client messages добавляем /start

Далее в файле test.py нажимаем на test_2 
после этого должен запустится бот и на каждый /start будет отвеченно сообщением из answer

Для того чтобы сделать запрос к апи нужно прописать в serveses_config payload и headers в headers содержаться заголовки,
в payload будет содержать если запрос get то params, если пост то json запроса