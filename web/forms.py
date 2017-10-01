from django.forms import ModelForm

from web.models import Order


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['email', 'url']
