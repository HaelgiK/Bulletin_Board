import django_filters
from django_filters import FilterSet, CharFilter, ModelChoiceFilter

from .forms import *
from django.utils.translation import gettext_lazy as _


# Создаем свой набор фильтров для модели Post.
class PostFilter(FilterSet):
    header = CharFilter(
        field_name='header',
        lookup_expr='icontains',
        label=_('Header'),
    )
    # categories = ModelChoiceFilter(
    #     queryset=Category.objects.all(),
    #     label='Category',
    #     empty_label='any'
    # )
    def __init__(self, *args, **kwargs):
        category_choices = kwargs.pop('category_choices', None)
        super().__init__(*args, **kwargs)
        if category_choices:
            self.fields['categories'].queryset = category_choices

    class Meta:
        # В Meta классе мы должны указать Django модель,
        # в которой будем фильтровать записи.
        model = Post
        # В fields мы описываем по каким полям модели
        # будет производиться фильтрация.
        fields = [
            # поиск по названию
            'header',
            'categories',
        ]

        # labels = {
        #     'header': _('Header'),
        #     'author': _('Author'),
        # }

# class CommentFilter(FilterSet):
#     post__header = CharFilter(lookup_expr='icontains', label='Header')
#
#     class Meta:
#         model = Comment
#         fields = ['post__header', ]


