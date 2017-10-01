import logging

from datetime import datetime
from time import sleep

from grab import Grab
from grab.spider import Spider, Task

logging.basicConfig(level=logging.DEBUG)


def get_datetime(str_time, str_date):
    day, month, year = str_date.split(' ')
    hour, minute = str_time.split(':')
    mos = ('янв', 'фев', 'март', 'апр',
           'май', 'июн', 'июл', 'авг',
           'сент','окт', 'ноябр', 'декабр')

    for i, m in enumerate(mos):
        if m in month:
            month = i + 1
            break

    return datetime(minute=int(minute), hour=int(hour), day=int(day), month=month, year=int(year))


class OlxSpider(Spider):
    initial_urls = []

    def task_initial(self, grab: Grab, task: Task):
        grab.setup(proxy='http://127.0.0.1:8080', proxy_type='https', timeout=1)

        for url in grab.doc.select(".//*[@id='offers_table']//*/td[1]/a/@href"):
            yield Task('detail', url=url.text())

        try:
            next_page = grab.doc.select(".//*[contains(@class, 'next')]/a[contains(@class, 'pageNextPrev')]/@href").one().text()
            yield Task('initial', url=grab.make_url_absolute(next_page))
        except IndexError as e:
            pass

    def task_detail(self, grab: Grab, task: Task):
        store = self.meta.get('store')

        try:
            time, date = grab.doc.rex_search(r'\d\d:\d\d.*20\d{2}').group(0).split(', ')
            creation_time = get_datetime(time, date)
            store(creation_time)
        except Exception as ex:
            print(ex)

        # anti ban
        sleep(8)


