from django.contrib import admin
from django.forms import CheckboxSelectMultiple
from django.db import models
from message.models import ClientQuestion, Answer, Api, Chat, Mess, BotMess, ButtonsRow, Button, ClientMessage, \
    TelegrammUser, Context
# from message.serveses import get_answer, save_send
import asyncio
from asgiref.sync import async_to_sync

class SendingRuleInline(admin.TabularInline):
    model = Answer
    fk_name = 'parrent'

class ClientMessageInline(admin.TabularInline):
    model = ClientMessage


class MessInline(admin.TabularInline):
    model = Mess

admin.site.register(Mess)


# Register your models here.
admin.site.register(ClientQuestion)

@admin.register(Api)
class ApiAdmin(admin.ModelAdmin):
    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)
    #     loop = asyncio.new_event_loop()
    #     asyncio.set_event_loop(loop)
    #     save_send(api_obj=obj, loop=loop)
    pass
    # change_form_template = 'examplemessage.html'
    #
    # def change_view(self, request, object_id, form_url="", extra_context=None):
    #     extra_context = extra_context or {}
    #     api_obj = Api.objects.get(id=object_id)
    #     answer = get_answer(api_obj.example, api_obj)
    #     extra_context['text'] = answer['text']
    #     extra_context['buttons'] = answer['buttons']
    #
    #
    #
    #     return super().change_view(
    #         request,
    #         object_id,
    #         form_url,
    #         extra_context=extra_context,
    #
    #     )


@admin.register(
Answer
)
class AnswerAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['id', 'text', 'forward', 'api']
    inlines = [
        SendingRuleInline,
        ClientMessageInline
    ]
    list_filter = ['parrent']
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},

    }

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['name', 'operator', 'manager']
    # inlines = [
    #     MessInline,
    # ]

class ButtonsRowInline(admin.TabularInline):
    model = ButtonsRow

@admin.register(BotMess)
class BotMessAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'msg_id', 'parrent', 'context', 'context__payload']
    inlines = [
        ButtonsRowInline,
    ]

@admin.register(Button)
class ButtonAdmin(admin.ModelAdmin):
    list_display = ['buttonsrow__botmess__user_id', 'type_b', 'arg_1', 'payload', 'payload_internal', 'select', 'buttonsrow__botmess__context',
                    'buttonsrow__botmess__context__payload']
    list_filter = ['type_b']
    readonly_fields = ['buttonsrow']

    # def get_context(self, obj):



@admin.register(TelegrammUser)
class TelegrammUserAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'username', 'phone']

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ['id', 'payload']

    def get_select_payload(self, obj):
        return async_to_sync(obj.get_select_payload)()