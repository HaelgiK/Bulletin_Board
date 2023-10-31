import django_filters
from django_filters import FilterSet, ModelChoiceFilter, DateFilter

from .forms import *
from .models import Category, Author
from django.utils.translation import gettext_lazy as _


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    category = ModelChoiceFilter(
        field_name='postcategory__category',
        queryset=Category.objects.all(),
        label='Category',
        empty_label='any',

    )

    author = django_filters.ModelChoiceFilter(
        field_name='author',
        label='Author',
        lookup_expr='exact',
        queryset=Author.objects.all(),
        empty_label='any',
    )

    date = DateFilter(
        field_name='date_created',
        lookup_expr='gt',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Published after')

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = [
            # поиск по названию
            'header',  #: ['icontains']
            # по автору
            'author'  #: ['exact']
        ]

        labels = {
            'header': _('Header'),
            'author': _('Author'),
        }
