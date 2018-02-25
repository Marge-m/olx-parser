from django.contrib import admin

# Register your models here.
from web.models import Subscription, SentUrls

class AdminSubscription(admin.ModelAdmin):
    list_display = ('pk', 'url', 'teleuser', 'if_newuser')


class AdminSentUrls(admin.ModelAdmin):
    list_display = ('pk', 'url', 'teleuser')


admin.site.register(SentUrls, AdminSentUrls)
admin.site.register(Subscription, AdminSubscription)
