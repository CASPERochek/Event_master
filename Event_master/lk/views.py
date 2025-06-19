from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from mero.models import Mero_on_site
from .models import UserRating
from .utils import add_points
import logging

logger = logging.getLogger(__name__)


@login_required
def profile(request):
    # Получаем мероприятия пользователя без select_related для event_type
    events = request.user.events.all().order_by('time')

    # Получаем топ-5 рейтинга
    top_ratings = UserRating.objects.select_related('user').order_by('-points')[:5]

    # Получаем рейтинг текущего пользователя
    user_rating, created = UserRating.objects.get_or_create(user=request.user)

    context = {
        'events': events,
        'top_ratings': top_ratings,
        'user_rating': user_rating,
    }
    return render(request, 'lk/personalAccount1.html', context)


@login_required
def event_register(request, event_id):
    """
    Регистрирует пользователя на мероприятие и начисляет баллы.
    """
    event = get_object_or_404(Mero_on_site, id=event_id)

    if request.user not in event.participants.all():
        event.participants.add(request.user)
        add_points(request.user, 20, f"Регистрация на мероприятие {event.name}")
        messages.success(request, "Вы успешно записались на мероприятие! +20 баллов")
    else:
        messages.info(request, "Вы уже записаны на это мероприятие")

    return redirect('event_detail', event_id=event.id)


@login_required
def event_unregister(request, event_id):
    """
    Обрабатывает отписку от мероприятия с вычетом баллов.
    """
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'error',
            'message': 'Требуется AJAX-запрос'
        }, status=400)

    try:
        event = get_object_or_404(Mero_on_site, id=event_id)
        user = request.user

        if user not in event.participants.all():
            return JsonResponse({
                'status': 'error',
                'message': 'Вы не записаны на это мероприятие'
            })

        is_volunteer = hasattr(event, 'volunteers') and event.volunteers.filter(id=user.id).exists()
        role = 'волонтера' if is_volunteer else 'участника'
        points_to_remove = -35 if is_volunteer else -20

        with transaction.atomic():
            event.participants.remove(user)
            if is_volunteer:
                event.volunteers.remove(user)

            if not add_points(user, points_to_remove, f"Отмена записи на {event.name}"):
                raise Exception("Ошибка вычета баллов")

        return JsonResponse({
            'status': 'success',
            'message': f'Вы отписались от мероприятия (списано {abs(points_to_remove)} баллов как {role})',
            'points': user.rating.points,
            'position': user.rating.position,
            'is_volunteer': is_volunteer
        })

    except Exception as e:
        logger.error(f"Ошибка отписки: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': 'Ошибка сервера при отписке'
        }, status=500)