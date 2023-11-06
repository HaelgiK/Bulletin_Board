from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.utils.translation import activate,\
    get_supported_language_variant #LANGUAGE_SESSION_KEY
from .models import Post, Category, MyModel
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from django.utils import timezone
from django.shortcuts import redirect
#  импортируем стандартный модуль для работы с часовыми поясами
import pytz



class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_created'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    form_class = PostForm


    # def get_queryset(self):
    #     # Получаем обычный запрос
    #     queryset = super().get_queryset()
    #     # Используем наш класс фильтрации.
    #     # self.request.GET содержит объект QueryDict
    #     # Сохраняем нашу фильтрацию в объекте класса,
    #     # чтобы потом добавить в контекст и использовать в шаблоне.
    #     self.filterset = PostFilter(self.request.GET, queryset)
    #     # Возвращаем из функции отфильтрованный список товаров
    #     return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#        context['filterset'] = self.filterset
        context['form'] = self.form_class()
        context['current_time'] = timezone.localtime(timezone.now())
#        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
#        context['time_now'] = datetime.utcnow()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if request.method == 'POST':
            request.session['django_timezone'] = request.POST['timezone']
            return redirect('post_list')

        if form.is_valid():
            form.save()

        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'


class SearchNews(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('search_news')

# Добавляем новое представление для создания новостей.
class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post')
    # Указываем разработанную форму
    form_class = PostForm
    # модель новостей
    model = Post
    # новый шаблон, в котором используется форма.
    template_name = 'news_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'article' in self.request.path:
            type_post = 'AR'
        else:
            type_post = 'NW'
        self.object.type_post = type_post
        return super().form_valid(form)

class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'

class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post')
    form_class = PostForm
    model = Post
    template_name = 'article_edit.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post')
    model = Post
    template_name = 'article_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        # Достаем из именованных аргументов (*kwargs) нашего представления наш 'pk'
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-date_created')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Достаем пользователя, который не входит в число подписчиков
        # (обращаясь ко всем пользователям elf.category.subscribers.all())
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        # Передаем категорию в шаблон
        context['category'] = self.category
        context['current_time'] = timezone.now()
        context['timezones'] = pytz.common_timezones
        return context


@login_required
def subscribe(request, pk):
    # Получаем текущего пользователя
    user = request.user
    # Получаем текущую категорию
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    message = 'Вы подписались на категорию: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})


@login_required
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)
    message = 'Вы отписались от категории: '
    return render(request, 'subscribe.html', {'category': category, 'message': message})

# class CategoryListView(ListView):
#    model = Post
#    ordering = '-id'
#    template_name = 'category_list.html'
#    #template_name = 'posts_of_cateory_list.html'
#    #posts.html'
#    context_object_name = 'category_news_list'
#
#    def get_queryset(self):
#        self.queryset = Post.objects.get(pk=self.kwargs['pk']).post_category.all()
#        return super().get_queryset()
#
# @login_required
# def subscribe(request, pk):
#     user = request.user
#     category = Category.objects.get(id=pk)
#     category.subscribers.add(user)
#     message = 'Вы подписались на категорию: '
#     return render(request, 'subscribe.html', {'category': category, 'message': message})

class Index(View):
    def get(self, request):
        curent_time = timezone.now()
        # Translators: This message appears on the home page only
        models = Post.objects.all()
        # return HttpResponse(string)
        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones  # добавляем в контекст все доступные часовые пояса
        }

        return HttpResponse(render(request, 'index.html', context))

    #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
