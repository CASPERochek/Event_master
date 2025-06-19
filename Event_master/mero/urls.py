from django.urls import path
from . import views
from django.urls import path
from .views import event_register
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns= [
    path('event/', views.event, name='event'),
    path('event/<int:event_id>/register/', views.event_register, name='event_register'),
    path('volunteering/', views.volunteering, name='volunteering'),
    path('ComingSoon/', views.coming_soon, name='doc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)