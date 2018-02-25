# coding=utf-8
import telebot
import json

from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView
from django.http import HttpResponseForbidden, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from web.models import Subscription
from web.tasks import create_request_crawling
from olx_stats.settings import NGROK, TOKEN

bot = telebot.TeleBot(TOKEN)
webhook_url = 'https://api.telegram.org/bot{}/setwebhook?url=https://{}/'.format(TOKEN, NGROK)

urls = {'Детский мир': 'detskiy-mir', 'Работа': 'rabota', 'Бизнес и услуги': 'uslugi', 'Обмен': 'obmen-barter',
        'Недвижимость': 'nedvizhimost', 'Животные': 'zhivotnye', 'Мода и стиль': 'moda-i-stil',
        'Транспорт': 'transport', 'Дом и сад': 'dom-i-sad', 'Хобби, отдых и спорт': 'hobbi-otdyh-i-sport',
        'Запчасти для транспорта': 'zapchasti-dlya-transporta', 'Электроника': 'elektronika',
        'Отдам даром': 'otdam-darom'}

category_names = urls.keys()

@csrf_exempt
def web_hook(request):
    payload = json.loads(request.body.decode('utf-8'))
    update = telebot.types.Update.de_json(payload)
    bot.process_new_updates([update])
    return HttpResponse()


@csrf_exempt
@bot.message_handler(commands=['start'])
def send_options(m):
    bot.send_message(m.chat.id, '/subscribe - подписаться на категории сайта olx.ua')


@csrf_exempt
@bot.message_handler(commands=['subscribe'])
def send_menu(m):
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[telebot.types.KeyboardButton(name) for name in category_names])
    msg = bot.send_message(m.chat.id, 'Выберите категорию',
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, name)


@csrf_exempt
@bot.message_handler(commands=category_names)
def name(m):
    if m.text not in urls:
        pass
    url = 'https://www.olx.ua/{}/'.format(urls[m.text])
    if Subscription.objects.filter(url=url, teleuser=m.chat.id).exists():
        bot.send_message(m.chat.id, 'Подписка уже была оформлена')
    else:
        subs = Subscription.objects.create(url=url, teleuser=m.chat.id)
        bot.send_message(m.chat.id, 'Подписка оформлена')
        create_request_crawling(subs.pk)


# bot.remove_webhook()
#
# # Set webhook
# bot.set_webhook(webhook_url)