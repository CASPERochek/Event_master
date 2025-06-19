# from . import views
# from django.urls import path
# from .views import profile, event_detail
#
#
# urlpatterns= [
#     path('profile/', views.profile, name='profile'),
#     path('event/<int:event_id>/', event_detail, name='event_detail'),
#
# ]




from django.urls import path

from mero.views import event_volunteer
from .views import profile, event_register, event_unregister

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('event/<int:event_id>/register/', event_register, name='event_register'),
path('event/unregister/<int:event_id>/', event_unregister, name='event_unregister'),
path('event/<int:event_id>/volunteer/', event_volunteer, name='event_volunteer'),

]
