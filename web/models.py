# coding=utf-8
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Subscription(models.Model):
    url = models.URLField()
    teleuser = models.TextField()
    if_newuser = models.BooleanField(default=True)


class SentUrls(models.Model):
    url = models.URLField()
    teleuser = models.TextField()

