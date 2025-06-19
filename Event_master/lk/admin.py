from django.contrib import admin
from .models import UserRating


@admin.register(UserRating)
class UserRatingAdmin(admin.ModelAdmin):
    """Административный интерфейс для модели UserRating."""
    list_display = ('user', 'points', 'position_display', 'last_updated')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    readonly_fields = ('last_updated',)
    list_filter = ('last_updated',)
    list_select_related = ('user',)

    def position_display(self, obj) -> int:
        """Отображает позицию пользователя в рейтинге."""
        return obj.position

    position_display.short_description = 'Позиция в рейтинге'