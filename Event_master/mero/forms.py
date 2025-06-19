from django import forms
from .models import Mero_on_site


class EventFilterForm(forms.Form):
    """Форма для фильтрации мероприятий."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Динамически получаем года из базы данных
        years = Mero_on_site.objects.dates('time', 'year')
        year_choices = [('', 'Все года')] + [(y.year, y.year) for y in years]

        self.fields['year'] = forms.ChoiceField(
            choices=year_choices,
            widget=forms.Select(attrs={
                'class': 'form-select bg-black text-white border-secondary'
            }),
            required=False,
            label=''
        )

    MONTH_CHOICES = [
        ('', 'Все месяцы'),
        ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'),
        ('04', 'Апрель'), ('05', 'Май'), ('06', 'Июнь'),
        ('07', 'Июль'), ('08', 'Август'), ('09', 'Сентябрь'),
        ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'),
    ]

    event_type = forms.ChoiceField(
        choices=[('', 'Все типы')] + Mero_on_site.EVENT_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select bg-black text-white border-secondary'
        }),
        required=False,
        label=''
    )

    month = forms.ChoiceField(
        choices=MONTH_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select bg-black text-white border-secondary'
        }),
        required=False,
        label=''
    )

    volunteering = forms.BooleanField(
        required=False,
        label='Волонтёрство',
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input',
            'style': 'width: 3em; height: 1.5em; transition: all 0.3s ease;'
        })
    )