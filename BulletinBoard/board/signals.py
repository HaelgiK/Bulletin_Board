
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Comment
from config.settings import DEFAULT_FROM_EMAIL


@receiver(post_save, sender=Comment)
def feedback_save(instance, **kwargs):
    post_user_email = instance.post.user.email
    send_mail(
        subject='New comment',
        message='There is a review for your ad',
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[post_user_email],
    )
