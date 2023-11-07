from django.db import models
from django.contrib.auth.models import User
from resources import *
from django.urls import reverse
from django.core.mail import send_mail


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
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    comment = models.BooleanField(default=False)

    # def send_email(self):
    #     subject = 'Отклик на объявление'
    #     message = 'Здравствуйте!\n\nНа ваше объявление "{}" появился новый отклик.\n\nС уважением,\nВаш сайт.'.format(
    #         self.post.header)
    #     from_email = 'Nikon1987-63rus@yandex.ru'
    #     recipient_list = [self.post.author.email]
    #
    #     send_mail(subject, message, from_email, recipient_list)

    def __str__(self):
        return self.text