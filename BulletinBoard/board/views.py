from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Category, Comment
from .filters import PostFilter
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.utils import timezone
from django.shortcuts import redirect
#  импортируем стандартный модуль для работы с часовыми поясами
import pytz



class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date_created'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    form_class = PostForm
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('post', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(accepted=True, bill_id=self.kwargs['pk']).order_by('time_create')
        context['comments'] = comments

        return context

    def send(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            post = form.save(commit=False)
            post.comment = self.object
            post.user = self.request.user
            post.send_notification_email()
            post.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)



class SearchPost(ListView):
    model = Post
    ordering = '-date_created'
    template_name = 'search.html'
    context_object_name = 'search_post'
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
        return redirect('search_post')

# Добавляем новое представление для создания новостей.
class PostCreate(LoginRequiredMixin, CreateView):
    # Указываем разработанную форму
    form_class = PostForm
    # модель новостей
    model = Post
    # новый шаблон, в котором используется форма.
    template_name = 'post_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        current_user = self.request.user
        self.object.user = current_user

        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, DeleteView):
    form_class = PostForm
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class PostDetailUser(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_user.html'
    context_object_name = 'post_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments = Comment.objects.filter(accepted=True, post_id=self.kwargs['pk']).order_by('time_create')
        context['comments'] = comments

        return context


class CommentList(ListView):
    model = Comment
    template_name = 'comment.html'
    ordering = '-time_create'
    context_object_name = 'comment_list'

    def get_queryset(self):
        # Достаем из именованных аргументов (*kwargs) нашего представления наш 'pk'
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-date_created')
        return queryset


class CommentDetail(DetailView):
    model = Comment
    template_name = 'comment.html'
    context_object_name = 'comment'


class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comment_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post = Post.objects.get(pk=self.kwargs['pk'])
        current_user = self.request.user
        self.object.user = current_user
        return super().form_valid(form)

class CommentDelete(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comment_delete.html'
    success_url = reverse_lazy('user_clicks')


@login_required
def user_posts(request, pk):
    # Получаем текущего пользователя
    current_user = request.user
    # Получаем текущий пост
    posts = Post.objects.filter(user=current_user).order_by('-time_create')
    return render(request, 'user_posts.html', {'posts': posts})


@login_required
def user_comments(request):
    current_user = request.user
    posts = Post.objects.filter(user=current_user).order_by('-date_created')
    selected_post_id = request.GET.get('post')

    comments = Comment.objects.filter(post__user = current_user).order_by('-time_create')
    if selected_post_id:
        comments = comments.filter(post__id=selected_post_id)

    if request.method == 'GET':
        selected_post_id = request.GET.get('post')
        if selected_post_id:
            posts = posts.filter(post__id=selected_post_id)

    return render(request, 'user_posts.html', {'posts': posts, 'comments': comments, 'selected_bill_id': selected_post_id})


@login_required
def accept_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.accepted = True
    comment.save()
    comment.send_accepted_email()
    return HttpResponseRedirect(reverse('user_clicks'))


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
