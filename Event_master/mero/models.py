from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Mero_on_site(models.Model):
    """Модель для хранения мероприятий."""
    EVENT_TYPES = [
        ('Концерт', 'Концерт'),
        ('Курс', 'Курс'),
        ('Выставка', 'Выставка'),
        ('День открытых дверей', 'День открытых дверей'),
        ('Мастер-класс', 'Мастер-класс'),
        ('Конкурс', 'Конкурс'),
        ('Спектакль', 'Спектакль'),
        ('Спорт', 'Спорт'),
        ('Конгресс', 'Конгресс'),
        ('Форум', 'Форум'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Название мероприятия",
        help_text="Введите название мероприятия"
    )

    time = models.DateTimeField(
        default=timezone.now,
        verbose_name="Время проведения",
        help_text="Укажите дату и время начала"
    )

    description = models.TextField(
        verbose_name="Описание",
        help_text="Подробное описание мероприятия",
        blank=True
    )

    event_type = models.CharField(
        max_length=20,
        choices=EVENT_TYPES,
        verbose_name="Тип мероприятия"
    )

    volunteering = models.BooleanField(
        default=False,
        verbose_name="Требуются волонтеры",
        help_text="Отметьте, если нужны волонтеры"
    )

    volunteers = models.ManyToManyField(
        User,
        related_name='volunteer_events',
        blank=True
    )

    photo = models.ImageField(
        upload_to='events/photos/',
        verbose_name="Фотография",
        blank=True,
        null=True,
        help_text="Загрузите фотографию для мероприятия"
    )

    participants = models.ManyToManyField(
        User,
        related_name='events',
        blank=True
    )

    class Meta:
        verbose_name = "Мероприятие"
        verbose_name_plural = "Мероприятия"
        ordering = ['-time']

    def __str__(self):
        return f"{self.name} ({self.get_event_type_display()})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Автоматически добавляем волонтеров в участники
        for volunteer in self.volunteers.all():
            if volunteer not in self.participants.all():
                self.participants.add(volunteer)