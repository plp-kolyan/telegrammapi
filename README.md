telegrammapi - это контсруктор телеграмм ботов главным образом заточенным на взаимодействие бота и стороннего api
домонтстрацию можно посмотреть https://youtu.be/SXaFrHVehCs?si=aqTZa_JFobeVkBxd
Видео с установкой и настройкой по этому мануалу тут https://youtu.be/VxQZo9DOUT8?si=4woGTdGEnSFj2OAd
Общая схема работы выглядит так, каждое сообщение отправленное ботом в телеграмм так же хранится в записях моделей джанго
Каждая такая запись будет отображенна в клиенте телеграмма, согласно правилам описанным в записях со специальными настройками

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/structure.jpg)



для работу нужен python и pycharm
Установка python и pycharm https://www.youtube.com/watch?v=yBE4tw8uBic

<h1>Установка</h1>
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
как получить api_id и api_hash есть в видео https://youtu.be/mLOYMg1lJJU?si=_BZyjWP07tg4h-yH&t=35
sender_id - Куда будет пересылаться сообщение (в начале пишем 0, позже будет написанно откуда его взять)в случе если в answer указанно что сообшение нужнно пересылать - это пока временный механизм который будет переделан на более обширные правила переотправки
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

<h1>Простой пример для обращения бота по api</h1>
видеоинструкция https://www.youtube.com/watch?v=JUe0h5vRFNI
показывает индекс цен на биткоин (BPI) в режиме реального времени.

1) Протестируйте api запустите в файле tests.py async def test_18(self):

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

    Скролим до Client messages добавим /Bitcoin - это команда которая будет триггерить этот answer при ее вводе пользователем в боте
    
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


   ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_15.jpg)

   Ввводим в боте /Bitcoin и получаем

   ![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_17.jpg)

<h1>ИИ помошник для чат для бота</h1>

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_18.jpg)

В telegrammapi есть встроенный метод api который делает запрос к ИИ 
для того чтобы настроить его работу нужно:


 
1)  Добавить http://127.0.0.1:8000/admin/message/api/    
    Название метода: Можно любое пусть будет - Аи Чат
    Url: http://127.0.0.1:8000/api/ai_chat
    Метод: post
    Тело запроса: {%- set _ = payload.update(context.payload) -%} - это запись означает что тело запроса будет 
    формироваться из контекста сообщений который будут заполнятся в процессе диалога 

2)  создать новый answer http://127.0.0.1:8000/admin/message/answer/add/
    Текст сообщения: {{response_json.content}} - это то что будет отправляться клиену, в данном случае content 
        ключ который будет браться из json который прийдёт от api, пример {"content": "Привет!"}, пользователю 
        будет отправленно привет.
    Шаблон ответа: {% set _ = context.payload.messages.append({"role": "assistant", "content": response_json.content}) %} 
         это запись означает что content приходящий при каждом обращении будет добавляться в context.payload.messages 
         
    Делать с пользовательским вводом: {% set _ = context.payload.messages.append({"role": "user", "content": message}) %}          
    это необходимо для учитывания ИИ контекста: в базе это будет выглядеть вот так:

             {'payload': 
                 {'model': 'gpt-4-turbo', 'messages': 
                  [{'role': 'user', 'content': 'привет'}, 
                  {'role': 'assistant', 'content': 'Привет! Чем могу помочь?'}]}}
    
    Ответ из апи: Нажимаем добавить и добавляем:

    Правило контекста: Наследовать   

    Удалять сообщение пользователя: Снять галочку

    Далее нажимаем Сохранить и продолжить редактирование

    Далее Ответить в случае ввода: Выбираем {{response_json.content}} - если его нет надо нажать 
        Сохранить и продолжить редактирование после этого СОХРАНИТЬ

3) создать новый answer http://127.0.0.1:8000/admin/message/answer/add/
    Текст сообщения: Указывайте любой можно добавить в конец /aichat - это пригодиться для того чтобы обнулить контекст сообщений
    Шаблон ответа: {% set _ = context.update({"payload":{"model": "gpt-4-turbo", 'messages':[]}}) %}
    Делать с пользовательским вводом: {% set _ = context.payload.messages.append({"role": "user", "content": message}) %}
    Правило контекста: Новый
    Ответить в случае ввода: Выбираем {{response_json.content}}        
    Удалять сообщение пользователя: Снять галочку
    Скролим вниз до Client messages добавляем /aichat - это пользовательская команда в телеграмм, если напишите другую тогда 
    в Текст сообщения указывайте другую команду

<h1>Добавление сложных Api, использование python библиотек для работы бота</h1>
В примере о ИИ было продемонстрированно когда запрос производился на внутреннее апи telegrammapi бота, 
далее будет продемонстрированно как можно добавить свой собственный python сценарий который может включать например 
какое то сложное api с составным запросом, использование какой либо python библиотеки или собственного python сценария
для этого нужно сделать 2 действия:
    1) message/views.py написать новую функцию аналогичную ai_chat(request) и обернуть ее в декоратор @api_view(['POST или GET'])
    2) в project/urls.py добавить path('api/новый путь', новая функция) в urlpatterns


<h1>Структура Answer</h1>
answer находится по этой ссылке http://127.0.0.1:8000/admin/message/answer/ данная модель описывает действия бота
в случае какого то пользовательского триггера это может быть нажатие пользователем на кнопку либо ввод текствого сообщение
Текст сообщения - это сообщение пользователю


<h2>JSON подобные обьекты в полях Answer</h2>
К ним относятся context, response_json, payload, payload_internal подробнее о json я обьясняю 
вот здесь https://github.com/plp-kolyan/whatisjson/tree/master

<h2>Отрисовка кнопок</h2>

Добавьте новый Аnswer http://127.0.0.1:8000/admin/message/answer/add/

Текст сообщения: Пример кнопки /buttons

Шаблон ответа: 

    {% set _ = button_kwargs.append([{
                            "type_b": "i",
                            "arg_1": "Самая простая кнопка",                       
                        }]) %}



Проскрольте до Client messages и добавьте /buttons

нажмите сохранить

напишите боту /buttons

получите такой ответ:

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_20.jpg)

В данном примере нажатие на эту кнопку ни к чему не приведет, давайте сделаем так, чтобы по нажатию генерировалось 
новое сообщение из Answer который мы укажем, для этого создадим новый answer http://127.0.0.1:8000/admin/message/answer/add/
    
Текст сообщения: "Результат нажатия кнопки"

Нажимаем сохранить именно сохранить чтобы перекинуло на страницу со всеми записями, запоминаем ID нового ответа

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_27.jpg)

Вернемся в Аnswer с кнопками и поменяем 
Шаблон ответа: 

    {% set _ = button_kwargs.append([{
                            "type_b": "i",
                            "arg_1": "Самая простая кнопка",
                            "answer_id": 14
                        }]) %}

В шаблон ответа добавим "answer_id": 14, где 14 номер id записи которую вы создали
Жмем сохранить, пишем боту /buttons получаем сообщение с кнопкой, нажимаем кнопку и получаем такой результат

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_28.jpg)

button_kwargs - это список c кнопками такой структуры [[], []] где каждый вложенный список это новый ряд кнопок, 
для того чтобы каждая кнопка была добавленна в один ряд


![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_21.jpg)

Нужно прописать в шаблон ответа вот так: 

    {% set list = [] %}
    {% for number in [1, 2] %}
        {% set _ = list.append({"type_b": "i", "arg_1": "Кнопка {number}".format(number=number)}) %}
    {% endfor %}    
    {% set _ = button_kwargs.append(list) %}`


чтобы проверить напишите боту /buttons - команда которую вы указывали в Client messages


для того чтобы каждая кнопка была добавленна в новый ряд

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_22.jpg)

Пропишите Шаблон ответа 


    {% for number in [1, 2] %}
        {% set _ = button_kwargs.append([{
                                    "type_b": "i",
                                    "arg_1": "Кнопка {number}".format(number=number),                       
                                }
        ]) %}
    {% endfor %}

Добавить выбор к кнопке при нажатии

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_23.jpg)

Шаблон ответа для примера

    {% set _ = button_kwargs.append([{
                                        "type_b": "i",
                                        "arg_1": "Самая простая кнопка", 
                                       "select": False,
                                    }
    ]) %}

"select": False - означает что по умолчанию эта кнопка не выбранна, True - будет выбранна сразу

Данный пример не содержит ни какой полезной нагрузки, полезную нагрузку за кнопкой можно посмотреть 
тут http://127.0.0.1:8000/admin/message/button/ в данном случае будет выглядеть так

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_24.jpg)

Для того чтобы добавить полезную нагрузку прописать в шаблон ответа шаблон вот так
    
    {% set buttons =  [{
        "type_b": "i",
        "arg_1": "Самая простая кнопка", 
        "select": False,
        "payload_internal": {'selects':{'key': 1}},
    },
    {
        "type_b": "i",
        "arg_1": "Добавить в контекст", 
        "collect_in_context": "selects",                                    
    }] %}
    {% for button in buttons %}
        {% set _ = button_kwargs.append([button]) %}
    {% endfor %}
    
Тоесть нужно добавить "payload_internal": {'selects':{'key': 1}}, структура должна быть именно как в примере ключи и значения могут быть любые,
collect_in_context указывает какой ключ из выбранных элементов нужно добавлять в контекст

Если в пользователь нажмет на "Добавить в контекст" с галочкой на "Самая простая кнопка"

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_25.jpg)




Тогда выбор будет добавленн в контекст таким образом, его можно будет посмотреть тут http://127.0.0.1:8000/admin/message/button/

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_26.jpg)

Если же убрать галочку с "Самая простая кнопка" и нажать "Добавить в контекст" то selects в контексте 
пересоберется по новой и будет пуст, так как нет выбранных элементов, визуально это выглядит как удаление раннее выбраного selects

Данный пример позволяет делать множественный выбор чтобы кнопок для выбора стало больше,
пропишите в шаблон ответа вот так:


    {% for number in [1, 2, 3] %}
        {% set _ = button_kwargs.append([{
            "type_b": "i",
            "arg_1": "Кнопка {number}".format(number=number), 
            "select": False,
            "payload_internal": {'selects':{'key': number}},
        }]) %}        
    {% endfor %}
    {% set _ = button_kwargs.append([{
        "type_b": "i",
        "arg_1": "Добавить в контекст", 
        "collect_in_context": "selects",                                    
        }]) %}

Напишите боту /buttons - результат выполнения будет выглядеть вот так:

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_29.jpg)

При нажатии на кнопку добавить в контекст, контекст http://127.0.0.1:8000/admin/message/botmess/ будет заполнен всеми выбранными элементами

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_30.jpg)

Данный пример позволяет выполнить множественный выбор, но часто бывает так что нам нужно ограничить выбор каким то одним 
вариантов, для этого просто добавьте ключ "unique_select_in_context": True, "payload_internal": {'select': number} и "collect_in_context": "select",

Пропишите в шаблон ответа вот так:


    {% for number in [1, 2, 3] %}
        {% set _ = button_kwargs.append([{
            "type_b": "i",
            "arg_1": "Кнопка {number}".format(number=number), 
            "select": False,
            "unique_select_in_context": True,
            "payload_internal": {'select': number},
        }]) %}        
    {% endfor %}
    {% set _ = button_kwargs.append([{
        "type_b": "i",
        "arg_1": "Добавить в контекст",       
        }]) %}

Теперь если выбрать другую кнопку при действующем выборе, то галочка на действующем выборе исчезнет

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_31.jpg)

Нажатие на кнопку "Добавить в контекст" приведет к заполнению контекста в таком виде http://127.0.0.1:8000/admin/message/botmess/:

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_32.jpg)

В вышеприведенных примаерах мы видим кнопку "Добавить в контекст" даже если не выбранно не одного элемента, 
это не правильно исправим это

Пропишите в шаблон ответа вот так:


    {% for number in [1, 2, 3] %}
        {% set _ = button_kwargs.append([{
            "type_b": "i",
            "arg_1": "Кнопка {number}".format(number=number), 
            "select": False,
            "unique_select_in_context": True,
            "payload_internal": {'select': number},
        }]) %}        
    {% endfor %}
    {% set _ = button_kwargs.append([{
        "type_b": "i",
        "arg_1": "Добавить в контекст",
        "show_button_if": ["select"]
        }]) %}

Теперь кнопка "добавить в контекст" будет появляться только в случае если есть какой-то выбор кнопки с номером, 
аналогично свойство show_button_if будет работать и с кнопками с множественным выбором

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_33.jpg)

На данный момент кнопка "Добавить в контекст" просто добавляет данные в контекст которые нигде не используются
Измените ранее созданный answer "Результат нажатия кнопки" или создайте его таким образом:

Текст сообщения: 

    Вы выбрали кнопку:
        №{{ context.select }}
    Пример кнопки /buttons

Шаблон ответа:

    {% set _ = button_kwargs.append([{
            "type_b": "i",
            "arg_1": "Назат", 
            "delete_in_context": ["select"],
            "answer_id": 11
        }]) %}

"delete_in_context" - Указывает ключ который нужно удалить из контекста, если его не указать то вы результат 
нажатия на эту кнопку изменит сообщение на предыдущее без выбора но выбор останеться в контексте, 
для того чтобы очистить контекст от select нужно это явно указать

"answer_id" это id answer где Текст сообщения: "Пример кнопки /buttons" который отрисовывает кнопки с возможностью выбора

Шаблон ответа в answer, где Текст сообщения: "Пример кнопки /buttons"

    {% for number in [1, 2, 3] %}
        {% set _ = button_kwargs.append([{
            "type_b": "i",
            "arg_1": "Кнопка {number}".format(number=number), 
            "select": False,
            "unique_select_in_context": True,
            "payload_internal": {'select': number},
        }]) %}        
    {% endfor %}
    {% set _ = button_kwargs.append([{
        "type_b": "i",
        "arg_1": "Добавить в контекст",
        "show_button_if": ["select"],
        "answer_id": 14
        }]) %}

Результат работы будет выглядеть так:

![Image alt](https://github.com/plp-kolyan/telegrammapi/raw/master/img/Screenshot_35.jpg)

<h1>Переменный в шаблонах Answer</h1>
user(first_name, last_name, username, phone) - это данные пользователя из телеграмм акаунта 
для добавления их к ответу можно использовать такой синтаксис: 
    
    user.first_name или user['first_name']

context - это данные в виде json поля которое хранит в себе всю полезную информацию, полученную от пользователя и бота, 
включая ответы от апи в рамках контекста сообщений

Это данные хранящие переменые контекста сообщений в json поле каждого отдельного контекста сообщения. 
В context можно как, добавлять данные из действий пользователя или сообщений, так и извлекать их для дальнейших действий например для заполнения
payload для выполнения запросов по апи или вывода каких то данных в тексте сообщения которым отвечает бот пользователю.


<h1>Тут будет продолжение</h1>
Для того чтобы настроить бот для работы с аpi протестируем api:
1) прописать в serveses_config.py данные для вашего api, 
    headers = {'Authorization': 'Token ****************************************'}
    url = 'http://1**.***.**.***:8000/api/results_operator_on_tables'
    если аpi не требует авторизациии ставим headers = {}
2) в файле tests.py находим async def test_17(self):    
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

