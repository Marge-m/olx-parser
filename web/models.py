from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import web.tasks as tasks


class RequestCrawling(models.Model):
    url = models.URLField(unique=True)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return self.url


class CreationTime(models.Model):
    request_crawling = models.ForeignKey(RequestCrawling)
    time = models.DateTimeField()


class Order(models.Model):
    email = models.EmailField()
    url = models.URLField()
    request_crawling = models.ForeignKey(RequestCrawling, null=True)


@receiver(post_save, sender=RequestCrawling)
def create_request_crawling(instance, **kwargs):
    tasks.start_crawling.delay(instance.pk)


@receiver(post_save, sender=Order)
def create_order(instance, **kwargs):
    try:
        r = RequestCrawling.objects.get(url=instance.url)

        if r.is_finished:
            tasks.send_email.delay(instance.pk, r.pk)
        else:
            instance.request_crawling = r
    except Exception as ex:
        r = RequestCrawling.objects.create(url=instance.url)
        instance.request_crawling = r
