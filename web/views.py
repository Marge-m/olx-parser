from django.views.generic import DetailView
from django.views.generic.edit import CreateView

from web.forms import OrderForm
from web.models import RequestCrawling, CreationTime


class HomeView(CreateView):
    template_name = 'home.html'
    form_class = OrderForm
    success_url = '/'


class RequestCrawlingView(DetailView):
    template_name = 'chart.html'
    model = RequestCrawling

    def get_context_data(self, **kwargs):
        context = super(RequestCrawlingView, self).get_context_data(**kwargs)
        context['hourly'] = []
        context['weekly'] = [0 for i in range(0, 7)]

        creation_times = CreationTime.objects.filter(request_crawling=context['object'])

        for h in range(0, 24):
            hr = creation_times.filter(time__hour=h).count()
            context['hourly'].append(hr)

        for c in creation_times:
            day_of_week = c.time.weekday()
            context['weekly'][day_of_week] += 1

        return context
