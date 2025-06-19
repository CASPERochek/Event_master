from django.contrib import admin
from django.utils.html import format_html
from .models import Mero_on_site


@admin.register(Mero_on_site)
class EventAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели мероприятий."""
    list_display = ('name', 'formatted_time', 'event_type', 'volunteering_status', 'photo_preview')
    list_filter = ('event_type', 'volunteering')
    search_fields = ('name', 'description')
    readonly_fields = ('photo_preview',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'time', 'description')
        }),
        ('Дополнительная информация', {
            'fields': ('event_type', 'volunteering', 'photo', 'photo_preview'),
            'classes': ('collapse',)
        }),
    )

    def formatted_time(self, obj):
        return obj.time.strftime('%d.%m.%Y %H:%M')

    formatted_time.short_description = 'Время проведения'
    formatted_time.admin_order_field = 'time'

    def volunteering_status(self, obj):
        return "Да" if obj.volunteering else "Нет"

    volunteering_status.short_description = 'Нужны волонтеры'

    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="200" style="border-radius: 5px;" />',
                obj.photo.url
            )
        return "Фотография не загружена"

    photo_preview.short_description = "Превью фотографии"