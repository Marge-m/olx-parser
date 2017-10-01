from django.contrib import admin

# Register your models here.
from web.models import RequestCrawling, CreationTime, Order


class AdminRequestCrawling(admin.ModelAdmin):
    list_display = ('pk', 'url', 'is_finished')


class AdminCreationTime(admin.ModelAdmin):
    list_display = ('time', 'request_crawling')


class AdminOrder(admin.ModelAdmin):
    list_display = ('url', 'email')


admin.site.register(RequestCrawling, AdminRequestCrawling)
admin.site.register(CreationTime, AdminCreationTime)
admin.site.register(Order, AdminOrder)
