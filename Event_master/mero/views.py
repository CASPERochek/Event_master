from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db import transaction
from .models import Mero_on_site
from .forms import EventFilterForm
from lk.utils import add_points
import logging

logger = logging.getLogger(__name__)


def volunteering(request):
    """Отображение страницы волонтерства."""
    return render(request, 'mero/becomeVolunteer.html')


def event(request):
    """Отображение списка мероприятий с фильтрами."""
    queryset = Mero_on_site.objects.all().order_by('time')
    filter_form = EventFilterForm(request.GET or None)

    if filter_form.is_valid():
        data = filter_form.cleaned_data

        if data['event_type']:
            queryset = queryset.filter(event_type=data['event_type'])

        if data['year']:
            queryset = queryset.filter(time__year=data['year'])

        if data['month']:
            queryset = queryset.filter(time__month=data['month'])

        if data['volunteering']:
            queryset = queryset.filter(volunteering=True)

    context = {
        'events': queryset,
        'filter_form': filter_form
    }
    return render(request, 'mero/selectionEvents1.html', context)


@login_required
def event_register(request, event_id):
    """Обработка записи на мероприятие."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'error',
            'message': 'Требуется AJAX-запрос'
        }, status=400)

    try:
        event = get_object_or_404(Mero_on_site, id=event_id)
        user = request.user

        if user in event.participants.all():
            return JsonResponse({
                'status': 'error',
                'message': 'Вы уже записаны',
                'button_text': 'Вы записаны'
            })

        with transaction.atomic():
            event.participants.add(user)
            if not add_points(user, 20, f"посещение {event.name}"):
                raise Exception("Ошибка начисления баллов")

        return JsonResponse({
            'status': 'success',
            'message': 'Запись успешна! +20 баллов',
            'button_text': 'Вы записаны',
            'points': user.rating.points,
            'position': user.rating.position
        })

    except Exception as e:
        logger.error(f"Ошибка записи: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Ошибка сервера'
        }, status=500)


@login_required
def event_volunteer(request, event_id):
    """Обработка записи как волонтера."""
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'error',
            'message': 'Требуется AJAX-запрос'
        }, status=400)

    try:
        event = get_object_or_404(Mero_on_site, id=event_id)
        user = request.user

        if not event.volunteering:
            return JsonResponse({
                'status': 'error',
                'message': 'Волонтеры не требуются на это мероприятие'
            })

        if user in event.participants.all():
            return JsonResponse({
                'status': 'error',
                'message': 'Вы уже записаны на это мероприятие'
            })

        with transaction.atomic():
            event.participants.add(user)
            event.volunteers.add(user)
            if not add_points(user, 35, f"волонтерство на {event.name}"):
                raise Exception("Ошибка начисления баллов")

        return JsonResponse({
            'status': 'success',
            'message': 'Вы записаны как волонтер! +35 баллов',
            'is_volunteer': True,
            'points': user.rating.points,
            'position': user.rating.position
        })

    except Exception as e:
        logger.error(f"Ошибка записи волонтера: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Ошибка сервера'
        }, status=500)



@login_required
def coming_soon(request):
    return render(request, 'mero/documents.html')