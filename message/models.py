from django.db import models

# Create your models here.
class ClientQuestion(models.Model):
    text = models.CharField(max_length=250, verbose_name='текст комманды')

    def __str__(self):
        return str(self.text)

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'



def get_update_api_default():
    return {}

class Api(models.Model):
    TYPES = {
        'post': "post",
        'get': "get",
    }
    name = models.CharField(max_length=250, verbose_name='Название метода')
    url = models.CharField(max_length=250, verbose_name='Url', blank=True, null=True)
    headers = models.JSONField(verbose_name='headers', default=get_update_api_default, null=True, blank=True)
    method = models.CharField(max_length=250, verbose_name='Метод', choices=TYPES, blank=True, null=True)
    body = models.TextField(verbose_name='Тело запроса', help_text="user, payload, context", blank=True, null=True)

    response_json_test = models.JSONField(verbose_name='Пример тестового JSON ответа', default=get_update_api_default, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class Answer(models.Model):
    CONTEXT_TYPES = {
        'new': "Новый",
        'parrent': "Наследовать",
        'null': "Нет",
    }
    # clien_qw = models.CharField(max_length=250, verbose_name='Вопрос клиента')
    text = models.TextField(verbose_name='Текст сообщения', help_text="user(first_name, last_name, username, phone), context, response_json")
    template = models.TextField(verbose_name='Шаблон ответа',
                                help_text="user, button_kwargs, response_json, payload, payload_internal, message, context",
                                blank=True, default='')
    do_with_user_input = models.TextField(verbose_name='Делать с пользовательским вводом', blank=True, default='', help_text='user, context, message')
    forward = models.TextField(verbose_name='Переслать', blank=True, default='', help_text="select_payload",)
    api = models.ForeignKey(Api, on_delete=models.SET_NULL, max_length=250, verbose_name='Ответ из апи', blank=True, null=True)
    context = models.CharField(verbose_name='Правило контекста', max_length=250, choices=CONTEXT_TYPES, default='parrent')
    parrent = models.ForeignKey('Answer', on_delete=models.SET_NULL,
                               verbose_name='Родитель',
                               blank=True, null=True, default=None,
                               related_name='Answer_Answer')
    answer_to_answer = models.ForeignKey('Answer', on_delete=models.SET_NULL,
                                verbose_name='Ответить в случае ввода',
                                blank=True, null=True, default=None,
                                related_name='answeranswer_to_answer')
    # delete_button = models.BooleanField("Удалять кнопку-треггер", default=False)
    delete_buttons = models.ManyToManyField('Answer',
                                              verbose_name='Удалять кнопки в контексте, ссылающиеся на',
                                              related_name='delete_button_in_context', blank=True)


    def __str__(self):
        return self.text

class ClientMessage(models.Model):
    text = models.TextField(verbose_name='Текст сообщения', unique=True, default='', blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE,
                               blank=True, null=True, default=None)



class Chat(models.Model):
    name = models.CharField(max_length=250, verbose_name='клиент')
    operator = models.CharField(max_length=250, verbose_name='оператор')
    manager = models.CharField(max_length=250, verbose_name='Менеджер')

    def __str__(self):
        return self.name

class Mess(models.Model):
    username = models.CharField(max_length=250, verbose_name='Усернайм')
    user_id = models.IntegerField()
    text = models.TextField(verbose_name='Текст', blank=True, null=True)

    def __str__(self):
        return self.username + ' ' + self.text

    # chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class Context(models.Model):
    payload = models.JSONField(verbose_name='Полезная нагрузка', default=get_update_api_default, null=True, blank=True)


    async def get_select_payload(self):
        context_dict = {}
        async for button in Button.objects.filter(buttonsrow__botmess__context=self, select=True).values(
                'payload_internal', 'unique_in_context'):

                if button['unique_in_context']:
                    context_dict.update(button['payload_internal'])
                else:
                    try:
                        key = list(button['payload_internal'].keys())[0]
                    except:
                        continue
                    else:
                        seq = context_dict.setdefault(key, [])
                        seq.append(button['payload_internal'])

        return context_dict

class BotMess(models.Model):
    user_id = models.IntegerField()
    msg_id = models.IntegerField(null=True, blank=True)
    parrent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(verbose_name='Текст сообщения', default='', blank=True)
    context = models.ForeignKey(Context, on_delete=models.CASCADE, related_name='button_context', null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='bot_mess_answer', null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.msg_id}"


class ButtonsRow(models.Model):
    botmess = models.ForeignKey(BotMess, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.button_set.all().values_list('id', 'type_b', 'arg_1'))


class ButtonManager(models.Manager):
    async def acreate(self, **obj_data):
        context = obj_data['buttonsrow'].botmess.context
        if obj_data.get('unique_in_context'):
            if arg_1 := obj_data.get('arg_1'):
                print('удаляю')
                print(await Button.objects.filter(arg_1=arg_1, buttonsrow__botmess__context=context).adelete())
        return await super().acreate(**obj_data)

def get_default_list():
    return []
class Button(models.Model):
    TYPES = {
        'i': "inline",
        'u': "url",
    }
    type_b = models.CharField(max_length=250, choices=TYPES)
    arg_1 = models.CharField(max_length=250)
    arg_2 = models.CharField(max_length=250, null=True, blank=True)
    buttonsrow = models.ForeignKey(ButtonsRow, on_delete=models.CASCADE, null=True, blank=True)
    payload = models.JSONField(verbose_name='Полезная нагрузка', default=get_update_api_default, null=True, blank=True)
    payload_internal = models.JSONField(verbose_name='Полезная нагрузка внутрянняя', default=get_update_api_default, null=True, blank=True)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_bot_mess', null=True, blank=True)
    select = models.BooleanField(default=None, null=True)
    unique_in_context = models.BooleanField(default=False)
    unique_select_in_context = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    show_button_if = models.JSONField(verbose_name='Показывать если', default=get_default_list, null=True, blank=True)
    collect_in_context = models.CharField(max_length=250, null=True, blank=True)
    delete_in_context = models.JSONField(verbose_name='Удалять в контексте', default=get_default_list, null=True, blank=True)
    objects = ButtonManager()


    def __str__(self):
        return f'{self.type_b} {self.arg_1}'

    async def asave(self, *args, **kwargs):
        if self.unique_select_in_context and self.select and self.payload_internal:
            await Button.objects.filter(buttonsrow__botmess__context=self.buttonsrow.botmess.context) \
                .filter(**{f'payload_internal__has_key': list(self.payload_internal.keys())[0]}).filter(select=True) \
                .exclude(id=self.id).aupdate(select=False)



        # if self.unique_in_context:


        return await super().asave(*args, **kwargs)

    async def acreate(self):
        pass



# class BotAnswer(models.Model):
#     json = models.JSONField(default=get_update_api_default, null=True, blank=True)
#     text = models.CharField(max_length=250, null=True, blank=True)
#     numeric = models.IntegerField(null=True, blank=True)
#     botmess = models.ForeignKey(BotMess, on_delete=models.CASCADE)
#     answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='answer_bot_mess')
# class Branch(models.Model):
#
class TelegrammUser(models.Model):
    user_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=250, default='', blank=True)
    last_name = models.CharField(max_length=250, default='', blank=True)
    username = models.CharField(max_length=250, default='', blank=True)
    phone = models.CharField(max_length=250, default='', blank=True)