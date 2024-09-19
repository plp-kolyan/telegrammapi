import json
from telethon.sync import TelegramClient, events, custom
import re
from telethon import functions, types
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from message.models import Api, Answer, Mess, BotMess, ButtonsRow, Button, ClientMessage, Context, TelegrammUser
from jinja2 import Template
from django.db.models import Q
from serveses_config import api_id, api_hash, bot_token, sender_id
import aiohttp
telegramm = {"ButtonInline": custom.Button.inline}

async def get_user_info(bot, user_id):
    user = await bot.get_entity(user_id)
    kwargs = {}
    for field in ['first_name', 'last_name', 'username', 'phone']:
        value = getattr(user, field)
        if value is not None:
            kwargs.update({field: value})
    return kwargs

async def get_response_json(url, payload, headers, method):
    metods = {
        'get': 'params',
        'post': 'json',
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with getattr(session, method)(url, headers=headers, **{metods[method]: payload}) as resp:
                response_json = await resp.json()
        except Exception:
            response_json = {'error': 'Ошибка вызвавшая исключение'}

    return response_json


async def get_message(id_answer):
    answer = await Answer.objects.aget(id=id_answer)


    await answer



def get_answer(response_json, object_id):

    response_json = json.loads(response_json)

    answer = {'text': response_json['descriptions'],
              'buttons': []
              }

    for order in response_json['orders']:
        answer['buttons'].append({"text": f"N{order['number']} от {order['date']}", "bytes": order['number']})

    return answer

# def get_message(response_json, get_response):
#     pass

async def update_messages_all_context(button_django, user_id, bot):
    if button_django:
        async for bm in BotMess.objects.filter(context=button_django.buttonsrow.botmess.context):
            try:
                await bot.edit_message(user_id, bm.msg_id, bm.text, **await get_message_kwargs(bm.id))
            except:
                continue

async def event_reply(bot, answer, user_id, parrent, button_django):
    if answer:
        botmess = await create_botmess_dj(answer, user_id, parrent, button_django, bot)

        if button_django:
            # print(f'answer == button_django.answer {answer == button_django.answer}')
            if not answer == parrent.answer:
                bot_mess_qw = BotMess.objects.filter(context=button_django.buttonsrow.botmess.context).exclude(id=botmess.id)
                await bot.delete_messages(user_id,
                                    message_ids=[msg_id async for msg_id in bot_mess_qw.values_list('msg_id', flat=True)])
                await bot_mess_qw.adelete()

            await (Button.objects.filter(buttonsrow__botmess__context=button_django.buttonsrow.botmess.context).exclude(buttonsrow__botmess__id=botmess.id)
                   .filter(answer_id__in=[a async for a in answer.delete_buttons.values_list('id', flat=True)])).adelete()

        await update_messages_all_context(button_django, user_id, bot)
        kwargs = await get_message_kwargs(botmess_id=botmess.id)
        # print(botmess.text, kwargs)
        # message = await event.reply(botmess.text, **kwargs)
        message = await bot.send_message(user_id, botmess.text, **kwargs)
        # print(f'botmess.msg_id {botmess.msg_id}')
        botmess.msg_id = message.id
        # print(f'botmess.msg_id {botmess.msg_id}')
        await botmess.asave(update_fields=["msg_id"])
        if answer.forward != '':
            select_payload = await button_django.buttonsrow.botmess.context.get_select_payload()
            template = Template(answer.forward)

            await bot.send_message(sender_id, template.render(select_payload=select_payload), parse_mode='HTML')


# def save_send(api_obj, loop, sender_id=sender_id):
#     bot = TelegramClient('bot', api_id, api_hash, loop=loop).start(bot_token=bot_token)
#     with (bot):
#
#         buttons = []
#         response_json = json.loads(api_obj.example)
#
#         try:
#             template = Template(api_obj.sucsess)
#         except Exception:
#             bot.send_message(sender_id, 'Ошибка в шаблоне')
#         else:
#             template.render(response_json=response_json, buttons=buttons, button=custom.Button)
#             bot.send_message(sender_id, 'Сообщение из админки', buttons=buttons)




async def get_message_kwargs(botmess_id):
    kwargs = {}
    buttons = Button.objects.select_related("buttonsrow__botmess__context").filter(buttonsrow__botmess_id=botmess_id)
    row = None
    t_buttons = [[]]
    async for button in buttons:
        if button.show_button_if:
            if button.buttonsrow.botmess.context:
                if not await (Button.objects.filter(buttonsrow__botmess__context=button.buttonsrow.botmess.context, select=True)
                       .filter(**{f'payload_internal__has_keys': button.show_button_if}).aexists()):
                    continue
        if button.type_b == 'i': t_button = custom.Button.inline(f"{'✅' if button.select else ''}{button.arg_1}", data=button.id)
        elif button.type_b == 'u': t_button = custom.Button.url(button.arg_1, button.arg_2)
        else: continue



        if row == button.buttonsrow.id or row is None:
            t_buttons[-1].append(t_button)
        else:
            t_buttons.append([t_button])
        row = button.buttonsrow.id
    if buttons:
        kwargs.update({'buttons': t_buttons})
    return kwargs



async def create_botmess_dj(answer, user_id, parrent, button_django, bot):
    message = {"text": None, "context": None}
    response_json = {}
    buttons_list = []
    payload = button_django.payload if button_django else {}
    payload_internal = button_django.payload_internal if button_django else {}
    user = await get_user_info(bot, user_id)


    context = None
    if answer.context == 'new':
        context = await Context.objects.acreate()
    elif answer.context == 'parrent':
        if parrent:
            if parrent.context:
                context = parrent.context
            else:
                context = await Context.objects.acreate()
        else:
            context = await Context.objects.acreate()
    if answer.api:
        """выполняем запрос"""
        # if not payload:
        template = Template(answer.api.body)
        template.render(user=user, payload=payload, context=context.payload if context else {})
        print(response_json)
        response_json = await get_response_json(answer.api.url, payload, answer.api.headers, answer.api.method)


    if answer.template == '':
        async for ans in Answer.objects.filter(parrent=answer):
            buttons_list.append([
                {
                    "type_b": "i",
                    "arg_1": ans.text,
                    "answer_id": ans.id,
                    "payload": payload

                }
            ])
        message.update({'text': answer.text})
    else:
        template = Template(answer.template)
        template.render(user=user, button_kwargs=buttons_list, response_json=response_json,
                        payload=payload, payload_internal=payload_internal, message=message, context=context.payload if context else {})
    if context: await context.asave(update_fields=["payload"])
    message_template = Template(answer.text)
    message_text = message_template.render(user=user, response_json=response_json, context=context.payload if context else {})

    if message["text"] is None:
        message["text"] = answer.text
    botmess = await BotMess.objects.acreate(user_id=user_id,
                                            parrent=parrent, text=message_text, context=context, answer=answer)
    # print(message)
    # if button_kwargs:
    for button_kwargs_row in buttons_list:
        buttonsrow = await ButtonsRow.objects.acreate(botmess=botmess)
        # await ButtonsRow.objects.acreate(botmess=)

        for button_kwargs in button_kwargs_row:
            await Button.objects.acreate(buttonsrow=buttonsrow, **button_kwargs)

    return botmess



def start_bot():

    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
    with ((bot)):

        # @bot.on(events.NewMessage)
        # async def handler(event):
        #
        #     value = event.message.message
        #     sender_id = event.message.peer_id.user_id
        #     await bot.send_message(sender_id,
        #                            'Новая новость из канала: ... [ID: ...]\n\nТут новость будет.\n\nДля того, чтобы опубликовать эту новость, нажмите на соответствующую кнопку.',
        #                            buttons=[[custom.Button.inline("Back", data="osg")]])
        #     await bot.send_message(sender_id, "Нажмите на кнопку 'Back'",
        #                            buttons=[[custom.Button.inline("Back", data="osg")]])
        #     username = await bot.get_entity(sender_id)
        #     print(event)
        #     await bot.send_message(username, value)
        @bot.on(events.NewMessage(pattern='/start_example'))
        async def start_handler(event):
            api_obj = await Api.objects.aget(id=1)
            answer = get_answer(api_obj.example, api_obj)
            buttons = [
                [custom.Button.inline(button['text'], data=button['bytes']), custom.Button.url('Посмотреть счет', 'https://www.google.com/')] for button in answer['buttons']
            ] + [[custom.Button.inline('В начало', data='/start'), custom.Button.inline('Связаться с менеджером', data='/manager')]] + \
                      [[custom.Button.inline('<--', data='/start'), custom.Button.inline('-->', data='/manager')]] + \
                      [[custom.Button.inline('Выбрать по дате', data='/start'), custom.Button.inline('Выбрать по номеру счёта', data='/manager')]] + \
                      [[custom.Button.switch_inline('Передать бота', 'Телеграмм бот компанни ООО')]] +\
                [[custom.Button.url('пример ссылки', 'http://178.248.87.207/admin/')]]

            sender_id = event.message.peer_id.user_id
            await bot.send_message(sender_id,
                                       answer['text'],
                                       buttons=buttons)
            await bot.send_message(sender_id, answer['text'],
                                   buttons=[[custom.Button.text('Пример кнопки')]])


        # https://docs.telethon.dev/en/stable/modules/events.html#telethon.events.callbackquery.CallbackQuery
        # @bot.on(events.CallbackQuery)
        # async def callback_query_handler(event):
        #     print(event)
        #     # sender_id = event.message.peer_id.user_id
        #     callback_query = event.data
        #     # username = await bot.get_entity(sender_id)
        #     str_callback_query = callback_query.decode('utf-8')
        #     if str_callback_query.isdigit():
        #         answer = await Answer.objects.select_related("api").aget(id=int(str_callback_query))
        #         if answer.api:
        #             buttons = []
        #             response_json = json.loads(answer.api.example)
        #             template = Template(answer.api.sucsess)
        #             template.render(response_json=response_json, buttons=buttons, button=custom.Button)
        #             await event.reply(answer.clien_qw, buttons=buttons)
        #             await event.answer('Correct answer!')
        #         else:
        #             await event.reply(answer.clien_qw)
        #     else:
        #         print(callback_query)
        #         await event.reply(f'Отправленно Оератору - {callback_query.decode("utf-8")}', buttons=Button.clear())
        #         await event.reply( 'Для продолжения выбирите ещё счет',
        #                                buttons=[[custom.Button.text('Завершить диалог')]])
            # await Mess.objects.acreate(username=username, user_id=)

        # @bot.on(events.CallbackQuery)
        # async def create_mess(event):
        #     print(event)
        #     callback_query = event.data
        #     str_callback_query = callback_query.decode('utf-8')
        #     print(event.chat_id)
        #     user = await bot.get_entity(sender_id)
        #     print(user.username)
        #     await Mess.objects.acreate(username=user.username, user_id=event.chat_id, text=str_callback_query)

        # @bot.on(events.NewMessage(pattern='Завершить диалог'))
        # async def start_handler(event):
        #     await event.reply(f'Диалог завершен, до свидания', buttons=Button.clear())

        @bot.on(events.NewMessage(pattern='/jinjaexample'))
        async def start_jinjaexample(event):
            response_json = {"orders": [{"number": 2133, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"},
                                        {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"},
                                        {"number": 2143, "date": "12.08.2024"}, {"number": 2143, "date": "12.08.2024"},
                                        {"number": 2143, "date": "12.08.2024"}],
                             "descriptions": "Скорректировать заявку или задать вопрос по ней"}

            buttons = []
            template = Template('''
            {% for order in response_json.orders %}
                {% with %}
                    {% set text = "N:{number}, от: {date}".format(number = order.number, date = order.date) %}
                    {% set _ = buttons.append([button.inline(text=text, data=order.number), 
                    button.url('Посмотреть счет', 'https://www.google.com/')]) %}                    
                {% endwith %}
                
                    
            {% endfor %}
                    ''')
            template.render(response_json=response_json, buttons=buttons, button=custom.Button)

            await event.reply('Пример джинжа', buttons=buttons)

        @bot.on(events.NewMessage(pattern='/jinjadjango'))
        async def start_jinjadjango(event):
            buttons = []
            api_obj = await Api.objects.aget(id=1)
            response_json = json.loads(api_obj.example)
            template = Template(api_obj.sucsess)
            template.render(response_json=response_json, buttons=buttons, button=custom.Button)
            await event.reply('k', buttons=buttons)

        @bot.on(events.NewMessage(pattern='/sender_id'))
        async def get_sender_id(event):
            sender_id = event.message.peer_id.user_id
            await event.reply(str(sender_id))

        # @bot.on(events.NewMessage(pattern='/start'))
        # async def start_handler(event):
        #     start_message_qw = Answer.objects.filter(answer=None).values('id', 'clien_qw')
        #     buttons = [[custom.Button.inline(mess_obj['clien_qw'], data=mess_obj['id'])] async for mess_obj in start_message_qw]
        #     reply = await event.reply("Начало", buttons=buttons)
        #     print(reply)

        # @bot.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            botmess = await BotMess.objects.acreate(user_id=event.message.peer_id.user_id)
            answers = Answer.objects.select_related('api').filter(answer=None)
            buttons = []
            async for answer in answers:
                buttonsrow = await ButtonsRow.objects.acreate(botmess=botmess)
                kwargs = {"buttonsrow": buttonsrow,
                          "type_b": 'i',
                          "arg_1": answer.clien_qw,
                          "answer_id": answer.id
                          }
                if answer.api:
                    payload = {}
                    template = Template(answer.api.body)
                    template.render(user_id=event.message.peer_id.user_id, payload=payload)
                    kwargs.update({"payload": payload})
                await Button.objects.acreate(**kwargs)

            message = await event.reply("Начало", buttons=await get_telegramm_buttons(botmess.id))
            botmess.msg_id = message.id
            await botmess.asave(update_fields=["msg_id"])

        @bot.on(events.CallbackQuery)
        async def callback_query_handler(event):
            # print(event.chat_id)
            # print(event.message_id)

            callback_query = event.data
            str_callback_query = callback_query.decode('utf-8')
            button_django = await Button.objects.select_related("answer__api").select_related(
                "buttonsrow__botmess__context").select_related(
                "buttonsrow__botmess__answer").aget(id=int(str_callback_query))
            context = button_django.buttonsrow.botmess.context
            if button_django.collect_in_context:
                context.payload.update({button_django.collect_in_context:[payload_internal[button_django.collect_in_context] async for payload_internal in (Button.objects.filter(buttonsrow__botmess__context=context, select=True)
                .filter(**{f'payload_internal__has_key': button_django.collect_in_context}).values_list('payload_internal', flat=True))]})
                await context.asave(update_fields=["payload"])
            if button_django.delete_in_context:
                for key in button_django.delete_in_context:
                    if key in context.payload: context.payload.pop(key)
                await context.asave(update_fields=["payload"])
            user_id = button_django.buttonsrow.botmess.user_id
            botmess = button_django.buttonsrow.botmess
            payload = button_django.payload
            if button_django.select is not None:
                button_django.select = not button_django.select
                await button_django.asave(update_fields=["select"])

                if button_django.unique_select_in_context:
                    if button_django.select:
                        context.payload.update(button_django.payload_internal)
                    else:
                        context.payload.pop(list(button_django.payload_internal.keys())[0])
                    await context.asave(update_fields=["payload"])
                if button_django.select and button_django.hide:
                    await button_django.adelete()
                await bot.edit_message(user_id, botmess.msg_id, botmess.text, **await get_message_kwargs(botmess.id))
                await update_messages_all_context(button_django, user_id, bot)

            await event_reply(bot, button_django.answer, user_id, botmess, button_django)

        @bot.on(events.NewMessage(pattern='/'))
        async def message_handler(event):
            print(event.message.message)
            print(event.message.peer_id.user_id)
            client_message = await ClientMessage.objects.select_related("answer__api").aget(text=event.message.message)
            await event_reply(bot, client_message.answer, event.message.peer_id.user_id, None, None)

        @bot.on(events.NewMessage(pattern='/start'))
        async def start_handler(event):
            user_id = event.message.peer_id.user_id
            kwargs = await get_user_info(bot, user_id)
            await TelegrammUser.objects.aget_or_create(user_id=user_id, **kwargs)
            # await bot.send_message(user.id, "Приветствуем вам в нашем боте",
            #                        buttons=[[custom.Button.text('/start')]])

        @bot.on(events.NewMessage())
        async def user_input(event):
            # print(event.message.peer_id.user_id)
            # print(event.message)
            delete_messages = [event.message.id]
            bot_mess = await BotMess.objects.select_related('answer__answer_to_answer__api', "answer__api", 'context'
                                                                 ).filter(user_id=event.message.peer_id.user_id).alast()
            answer = bot_mess.answer
            if answer.do_with_user_input:
                message_template = Template(answer.do_with_user_input)
                user = await get_user_info(bot, event.message.peer_id.user_id)
                message_template.render(user=user, context=bot_mess.context.payload, message=event.message.message)

                await bot_mess.context.asave(update_fields=["payload"])
                if answer.answer_to_answer:
                    delete_messages.append(bot_mess.msg_id)
                    await event_reply(bot, answer.answer_to_answer, event.message.peer_id.user_id, bot_mess, None)

            await bot.delete_messages(event.message.peer_id.user_id,
                                      message_ids=delete_messages)


            # if event.message.reply_to:
            #     pass










        bot.run_until_disconnected()


