from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class UserRating(models.Model):
    """Модель для хранения рейтинга пользователей."""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='rating',
        verbose_name='Пользователь'
    )
    points = models.IntegerField(
        default=0,
        verbose_name='Баллы'
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name='Последнее обновление'
    )

    class Meta:
        ordering = ['-points']
        verbose_name = 'Рейтинг пользователя'
        verbose_name_plural = 'Рейтинги пользователей'

    def __str__(self) -> str:
        return f"{self.user.username}: {self.points} баллов"

    @property
    def position(self) -> int:
        """Вычисляет текущую позицию пользователя в рейтинге."""
        return UserRating.objects.filter(points__gt=self.points).count() + 1


@receiver(post_save, sender=User)
def create_user_rating(sender, instance, created: bool, **kwargs) -> None:
    """Создает запись рейтинга при регистрации нового пользователя."""
    if created:
        UserRating.objects.get_or_create(user=instance)