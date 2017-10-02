from __future__ import absolute_import, unicode_literals

import time

from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.urls import reverse

from web import celery_app as app
from spider import OlxSpider


def get_time_saver(request_crawling):
    def time_saver(date_time):
        from web.models import CreationTime
        CreationTime.objects.create(request_crawling=request_crawling, time=date_time)
    return time_saver


@app.task(ignore_result=True)
def start_crawling(req_crawl_id):
    from web.models import RequestCrawling
    r = RequestCrawling.objects.get(pk=req_crawl_id)
    bot = OlxSpider(thread_number=1, meta={'store': get_time_saver(r)})
    bot.initial_urls.append(r.url)
    bot.run()

    for order in r.order_set.all():
        send_email.delay(order.pk, req_crawl_id)


@app.task(ignore_result=True)
def send_email(order_id, req_crawl_id):
    from web.models import Order

    order = Order.objects.get(pk=order_id)
    send_mail('Результат сбора статистики',
              'Ссылка на график - {}'.format(reverse('charts', args=(req_crawl_id,))),
              from_email=EMAIL_HOST_USER, recipient_list=[order.email])
    order.delete()
