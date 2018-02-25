# coding=utf-8
import logging

from grab import Grab
from grab.spider import Spider, Task


logging.basicConfig(level=logging.DEBUG)


class OlxSpider(Spider):
    initial_urls = []

    def task_initial(self, grab: Grab, task: Task):
        from web.models import SentUrls
        send_url = self.meta.get('send_url')
        teleuser = self.meta.get('teleuser')
        if_newuser = self.meta.get('if_newuser')
        for url in grab.doc.select(".//*[@id='offers_table']//*/td[1]/a/@href"):
            if SentUrls.objects.filter(teleuser=teleuser, url=url.text().split('.html')[0] + '.html').exists():
                print('Новых объявлений нет')
                return
            send_url(url.text())
            if if_newuser:
                return
        try:
            next_page = grab.doc.select(".//*[contains(@class, 'next')]/a[contains(@class, 'pageNextPrev')]/@href").one().text()
            yield Task('initial', url=grab.make_url_absolute(next_page))
        except IndexError as e:
            pass
