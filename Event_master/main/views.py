from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    data = {'title': 'Главная страница'}
    return render(request, 'main/events.html', data)

def categories(request):
    return HttpResponse("<h1>Статьи по категориям</h1>")