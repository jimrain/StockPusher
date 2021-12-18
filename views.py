from django.shortcuts import render
from django_eventstream import get_current_event_id

# def index(request):
#    return render(request, 'StockPusher/index.html')

def home(request):
    context = {}
    context['url'] = '/events/'
    context['last_id'] = get_current_event_id(['time'])
    return render(request, 'StockPusher/home.html', context)