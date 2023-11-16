from django.db import models
from django.contrib.auth.models import User
from resources import *
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, default=None)

    def __str__(self):
        return self.name


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    categories = models.CharField(max_length=2, choices=CATEGORIES, default='TK')
    header = models.CharField(max_length=100)
    content = models.TextField()

    def preview(self):
        return self.content[:124] + '...' if len(self.content) > 124 else self.content

    def __str__(self):
        return f'{self.header}: {self.content[:124]}'

    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)

    def send_notification_email(self):
        subject = 'Отклик на ваше объявление'
        message = f'Здравствуйте!\n\nНовый отклик на ваше объявление "{self.post}".'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.comment_post.user.email]

        send_mail(subject, message, from_email, recipient_list)

    def send_accepted_email(self):
        subject = 'Ваш отклик принят'
        message = f'Здравствуйте!\n\nВаш отклик "{self.text[:15]}" принят.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]

        send_mail(subject, message, from_email, recipient_list)

    def get_absolute_url(self):
        return reverse('posts')

    def __str__(self):
        return self.text
