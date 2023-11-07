import django_filters
from django_filters import FilterSet, CharFilter

from .forms import *
from django.utils.translation import gettext_lazy as _


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    header = CharFilter(
        field_name='header',
        lookup_expr='icontains',
        label=_('Header'),
    )

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = [
            # поиск по названию
            'header',
        ]

        labels = {
            'header': _('Header'),
            'author': _('Author'),
        }
