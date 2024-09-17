import json
from unittest import TestCase
from test_config import *
from message.serveses import *
from message.models import Api
import asyncio
from unittest import IsolatedAsyncioTestCase

class DevTestCase(TestCase):
    def test_0(self):
        api_obj = Api.objects.get(id=1)
        # response_json = json.loads(api_obj.example)
        # print(response_json)
        print(get_answer(api_obj.example, api_obj))

    def test_1(self):
        response_json = {"orders": [{"number": 2133, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"},
                    {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"},
                    {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"},
                    {"number": 2143, "date": "12.08.2024"}],
         "descriptions": "Скорректировать заявку или задать вопрос по ней"}

    def test_1_1(self):

        from jinja2.ext import do
        node = {'Name': 'Вася', 'id': 2, "ButtonInline": custom.Button.inline}

        template = Template('''
            {%- set data = {
                  'name' : node.Name,
                  'id' : node.id,
               }
            -%}
            {%- set _ = node.update({"key": "value"}) -%}
            {{node}}
            {#   
            {% for name in names %}
                {{ name }}
            {% endfor %}
            #}
        ''')
        print(template.render(node=node))
        print(node)

    def test_1_2(self):

        from jinja2.ext import do
        node = {'Name': 'Вася', 'id': 2, "ButtonInline": custom.Button.inline}
        telegramm = {"ButtonInline": custom.Button.inline}
        buttons = []
        template = Template('''
            {%- set _ = buttons.append([telegramm.ButtonInline(text='привет', data=1)]) -%}
        ''')
        print(template.render(buttons=buttons, telegramm=telegramm))
        # print(template.new_context({"buttons":buttons, "telegramm":telegramm}))
        print(node)

    def test_2(self):
        start_bot()

    def test_3(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        # save_send(loop=loop)

    def test_4(self):
        d = {"number": 2133, "date": "12.08.2024"}
        schema = 'N:{number}, от: {date}'
        print(schema.format(number = 6, date = "12.08.2024"))
        r = "N:2133, от: 12.08.2024"

    def test_5(self):
        print(Answer.objects.filter(answer=None).values('id', 'clien_qw'))

    def test_6(self):
        b = b'2'
        print(int(str(b.decode('utf-8'))) == 2)

    def test_7(self):
        answer = Answer.objects.select_related("api").get(id=2)
        print(answer.api)
        print(answer.api)

    def test_8(self):
        answer = Answer.objects.get(id=2)
        print(answer.api)
        print(answer.api)

    def test_9(self):
        b = b'answer_id_1'
        print(type(json.dumps({"c": 0, "b": 0, "a": 0})))
        print(type(b))
        r = re.compile(b'answer_id_')
        print(r)

    def test_10(self):
        rList = [1, 2, 3, 4, 5]

        arr = bytes(rList)
        print(arr.count())
        print(dir(arr))

    def test_11(self):
        answer = Answer.objects.get(id=4, clien_qw='{{Выбирает дату}}')
        print(answer.clien_qw)

    def test_12(self):
        buttons = Button.objects.select_related("buttonsrow").filter(buttonsrow__botmess_id=9)
        for button in buttons:
            print(button.buttonsrow.id)

    def test_13(self):
        ''''
        {%- set _ = payload.update({"user_id": user_id,
            "ofset": 0
            }) -%}

        {"orders": [{"number": 2133, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"}], "descriptions": "Скорректировать заявку или задать вопрос по ней"}


        {% for order in response_json.orders %}
                {% with %}
                    {% set text = "N:{number}, от: {date}".format(number = order.number, date = order.date) %}
                    {% set _ = button_kwargs.append([{
                        "type_b": "i",
                        "arg_1": text,
                        "arg_2":   "{number}".format(number = order.number),
                        "answer_id": 7,
                        "payload": {"number": order.number}

                    }, {
                    "type_b": "u",
                    "arg_1": "Посмотреть счет",
                    "arg_2": "https://www.google.com/"
                    }]) %}
                {% endwith %}
            {% endfor %}
            {% with %}
            {% set ofset= 5 %}



            {% set button_row = [] %}

            {% if payload.ofset >=  ofset %}
                {% set payload_left= payload.copy() %}
                {%- set _ = payload_left.update({"ofset": payload_left.ofset - ofset}) -%}
                {%- set _ = button_row .append({
                                    "type_b": "i",
                                    "arg_1": "Посмотреть на {number} страннице".format(number=payload.ofset//ofset) ,
                                    "answer_id": 2,
                       "payload": payload_left
                                }) -%}

            {% endif %}
            {% if response_json.orders|length >=  ofset %}
                {% set payload_right= payload.copy() %}
                {%- set _ = payload_right.update({"ofset": payload_right.ofset + ofset}) -%}
                 {%- set _ = button_row .append({
                                    "type_b": "i",
                                    "arg_1": "Посмотреть на {number} страннице".format(number=payload.ofset//ofset+2) ,
                                    "answer_id": 2,
                       "payload": payload_right
                                }) -%}
            {% endif %}


            {% set _ = button_kwargs.append(button_row ) %}
            {% set _ = message.update({"text": "Ваши неотгруженные счетов:  {count}, страница {page}, за всё время".format(count=response_json.orders|length, page=payload.ofset//ofset + 1)}) %}

            {% endwith %}

        '''
        l= {"adresses": [{
            "name": "603010,РОССИЯ,НИЖЕГОРОДСКАЯ ОБЛ.,ГОРОД НИЖНИЙ НОВГОРОД Г.О., ,НИЖНИЙ НОВГОРОД Г., ,ЗЕЛЕНОДОЛЬСКАЯ УЛ., Д. 55, , , ,КВ. 1,",
            "id": 12345}, {
            "name": "195030,РОССИЯ,САНКТ-ПЕТЕРБУРГ Г.,МУНИЦИПАЛЬНЫЙ ОКРУГ РЖЕВКА ВН.ТЕР.Г., , , ,НАСТАВНИКОВ ПР-КТ, Д. 21,ЛИТЕРА А, , ,КВ. 345,",
            "id": 54321}],
            "dates": [{"data": "05.09.2024", "id": 456}, {"data": "06.09.2024", "id": 457}, {"data": "07.09.2024", "id": 458},
                      {"data": "08.09.2024", "id": 459}]}
        print(l)

    def test_14(self):
        for i in [4]:
            print(i)
        else:
            print(45)

    def test_15(self):
        y = False
        b = not y
        print(b)

        а = {
            "orders": [
                {
                    "number": 2133,
                    "date": "2024-08-12",
                    "img": "/url",
                },
                {
                    "number": 2143,
                    "date": "2024-08-12",
                    "img": "/url",
                }
            ],
            "descriptions": "Ваши крайние счета",
            "telegram_chat_id": "ID чата логистов"
        }


class Test(IsolatedAsyncioTestCase):
    async def test_0(self):
        callback_query= b'2'
        print(await Answer.objects.aget(id=callback_query))

    async def test_1(self):
        print(await get_message(2))

    async def test_2(self):
        start_message_qw = Answer.objects.filter(answer=None).values('id', 'clien_qw')
        buttons = [[custom.Button.inline(mess_obj['clien_qw'], data=mess_obj['id'])] async for mess_obj in
                   start_message_qw]
        print(buttons)

    async def test_3(self):
        botanswer = await Button.objects.select_related("answer__api").select_related("buttonsrow__botmess").aget(id=12)
        api = botanswer.answer.api
        if api:
            json = {}
            """выполняем запрос"""
            template = Template(api.body)
            print(template.render(user_id=botanswer.buttonsrow.botmess.user_id, json=json))
            response_json = api.response_json_test
            template = Template(api.sucsess)
            button_kwargs = []
            template.render(button_kwargs=button_kwargs, response_json=response_json)
            print(button_kwargs)
            if button_kwargs:
                botmess = await BotMess.objects.acreate(user_id=botanswer.buttonsrow.botmess.user_id,
                                       parrent=botanswer.buttonsrow.botmess)
                for button_kwargs_row in button_kwargs:
                    buttonsrow = await ButtonsRow.objects.acreate(botmess=botmess)
                    # await ButtonsRow.objects.acreate(botmess=)

                    for button_kwargs in button_kwargs_row:
                        print(button_kwargs)
                        await Button.objects.acreate(buttonsrow=buttonsrow, **button_kwargs)







    async def test_4(self):
        telegramm_buttons = await get_telegramm_buttons(9)
        print(telegramm_buttons[0][0].data)


    async def test_5(self):
        answers = Answer.objects.select_related('api').filter(answer=None)
        user_id = 2312432
        buttons = []
        async for answer in answers:
            payload = {}
            if answer.api:
                print(answer.api.body)
                template = Template(answer.api.body)
                print(template.render(user_id=user_id, payload=payload))
            print(payload)


    async def test_6(self):
        parrent = await Answer.objects.aget(id=8)
        async for button in Answer.objects.filter(parrent=parrent):
            print(button)
        # async for button in answer.answer_answer_set.all():
        #     print(button)


    async def test_7(self):
        button = await Button.objects.select_related('buttonsrow__botmess__context').aget(id=7269)
        print({f'payload_internal__{list(button.payload_internal.keys())[0]}__isnull': False})

        await Button.objects.filter(buttonsrow__botmess__context=button.buttonsrow.botmess.context)\
         .filter(**{f'payload_internal__has_key': list(button.payload_internal.keys())[0]}).filter(select=True)\
                .exclude(id=button.id).aupdate(select=False)

    async def test_8(self):
        context_dict = {}
        async for button in Button.objects.filter(buttonsrow__botmess__context__id=44, select=True).values('payload_internal', 'unique_in_context'):
            if button['unique_in_context']:
                context_dict.update(button['payload_internal'])
            else:
                key = list(button['payload_internal'].keys())[0]
                seq = context_dict.setdefault(key, [])
                seq.append(button['payload_internal'])

        print(context_dict)

    async def test_9(self):
        context = await Context.objects.aget(id=44)
        print(await context.get_select_payload())


    async def test_10(self):
        context = await Context.objects.aget(id=51)
        select_payload = await context.get_select_payload()
        print(select_payload)
        template = Template(
            '''
            {{ select_payload.name }}<br>
            <strong>Заказы</strong>:<br>
            <ul>
            {% for order in select_payload.order %}
                <li>N{{order.order.number}} от: {{order.order.date}}<li>
            {% endfor %}
            </ul>
            <strong>Доставить {{select_payload.date.date}}</strong>:<br>
            {{select_payload.adress.name}}
            
            
            '''
        )

        print(template.render(select_payload=select_payload))

    async def test_11(self):
        button = await Button.objects.select_related('buttonsrow__botmess__context').aget(id=(8137))
        print(await button.asave())


    async def test_12(self):
        answer = await Answer.objects.prefetch_related('delete_buttons').aget(id=10)
        # print(answer.delete_buttons.all())
        print([a async for a in answer.delete_buttons.values_list('id', flat=True)])


    async def test_13(self):
        async for button in (Button.objects.filter(buttonsrow__botmess__context=106, select=True)
                .filter(**{f'payload_internal__has_keys': ['order']})):
            print(button)

    async def test_14(self):
        print(await Button.objects.filter(buttonsrow__botmess__context=106, select=True)
                .filter(**{f'payload_internal__has_keys': ['order']}).aexists())

    async def test_15(self):
        button_django = await Button.objects.select_related('buttonsrow__botmess__context').aget(id=12238)
        context = button_django.buttonsrow.botmess.context
        print(button_django.collect_in_context)
        print([payload_internal[button_django.collect_in_context] async for payload_internal in
         (Button.objects.filter(buttonsrow__botmess__context=context, select=True)
          .filter(**{f'payload_internal__has_key': button_django.collect_in_context}).values_list('payload_internal',
                                                                                                   flat=True))])







# Create your tests here .
