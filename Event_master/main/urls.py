from . import views
from django.urls import path
from main.views import index, categories

urlpatterns = [

    path('', views.index, name="home"),
    path('cats/', views.categories, name="cat"),
]