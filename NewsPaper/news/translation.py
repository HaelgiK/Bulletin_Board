
from .models import Category, Post, MyModel
# импортируем декоратор для перевода и класс настроек,
# от которого будем наследоваться
from modeltranslation.translator import register, \
    TranslationOptions


# регистрируем наши модели для перевода

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    # указываем, какие именно поля надо переводить в виде кортежа
    fields = ('category_name',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    # указываем, какие именно поля надо переводить в виде кортежа
    fields = ('header', 'content', 'date_created',)


@register(MyModel)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('name',)
