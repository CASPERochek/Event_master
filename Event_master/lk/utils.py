from django.db import transaction
from .models import UserRating
import logging

logger = logging.getLogger(__name__)


def add_points(user, points: int, reason: str = "") -> bool:
    """
    Безопасно добавляет баллы пользователю с транзакцией.

    Args:
        user: Пользователь
        points: Количество баллов для добавления (может быть отрицательным)
        reason: Причина изменения баллов (для логов)

    Returns:
        bool: Успешность операции
    """
    try:
        with transaction.atomic():
            rating, created = UserRating.objects.get_or_create(
                user=user,
                defaults={'points': points}
            )

            if not created:
                rating.points += points
                rating.points = max(rating.points, 0)  # Защита от отрицательных значений
                rating.save()

            logger.info(f"Изменены баллы пользователя {user.username}. Причина: {reason}")
            return True

    except Exception as e:
        logger.error(f"Ошибка изменения баллов для {user.username}: {str(e)}")
        return False