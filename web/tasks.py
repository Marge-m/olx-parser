# coding=utf-8
from __future__ import absolute_import, unicode_literals

import telebot
import json

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse
from django_celery_beat.models import PeriodicTask, IntervalSchedule

# import celery_app as app
from olx_stats.celery import app

from olx_stats.settings import TOKEN

bot = telebot.TeleBot(TOKEN)

def send_url_to_teleuser(subscription_id):
    def add_url(url):
        from web.models import Subscription, SentUrls
        subs = Subscription.objects.get(pk=subscription_id)
        chat_id = subs.teleuser
        send_msg.delay(chat_id, url)
        subs.if_newuser = False
        subs.save()
        url = url.split('.html')[0] + '.html'
        SentUrls.objects.create(teleuser=chat_id, url=url)
    return add_url


def create_request_crawling(subscription_id):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=20,
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.create(
        interval=schedule,
        name='Crawling{}'.format(subscription_id),
        task='web.tasks.start_crawling',
        kwargs=json.dumps({'subscription_id': subscription_id})
    )


@app.task
def start_crawling(subscription_id):
    from web.models import Subscription
    from spider import OlxSpider
    subs = Subscription.objects.get(pk=subscription_id)
    parser = OlxSpider(thread_number=1, meta={'send_url': send_url_to_teleuser(subscription_id),
                                              'if_newuser': subs.if_newuser, 'teleuser': subs.teleuser})
    parser.initial_urls.append(subs.url)
    parser.run()


@app.task
def send_msg(chat_id, url):
    msg = 'Новое объявление на сайте olx.ua \n {}'.format(url)
    bot.send_message(chat_id, msg)

