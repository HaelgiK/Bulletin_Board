from celery import shared_task
from .models import Comment, Post
from django.template.loader import render_to_string
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from config.settings import DEFAULT_FROM_EMAIL
from django.utils import timezone
import datetime



def comment_post_send_mail(pk, email):
    # указываем какой шаблон брать за основу и преобразовываем его в строку для отправки подписчику
    html_context = render_to_string(
        'new_comment_email.html',
        {
            'link': f'{settings.SITE_URL}/posts/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        # тема письма
        subject='Новый отклик',
        # тело пустое, потому что мы используем шаблон
        body='',
        # адрес отправителя
        from_email=settings.DEFAULT_FROM_EMAIL,
        # список адресатов
        to=email,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send(fail_silently=False)

@shared_task
def comment_post_notification(pk):
    comment = Post.objects.get(id=pk)
    post = comment.post
    user_email = [post.user.email]
    comment_post_send_mail(post.pk, user_email)
