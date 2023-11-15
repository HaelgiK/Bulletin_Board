# Generated by Django 4.2.4 on 2023-11-07 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0004_category_category_name_en_us_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mymodel',
            name='kind',
        ),
        migrations.RemoveField(
            model_name='postcategory',
            name='category',
        ),
        migrations.RemoveField(
            model_name='postcategory',
            name='post',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='comment_time',
            new_name='time_create',
        ),
        migrations.RemoveField(
            model_name='category',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='category',
            name='category_name_en_us',
        ),
        migrations.RemoveField(
            model_name='category',
            name='category_name_ru',
        ),
        migrations.RemoveField(
            model_name='category',
            name='subscribers',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='comment_rating',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_category',
        ),
        migrations.RemoveField(
            model_name='post',
            name='post_rating',
        ),
        migrations.RemoveField(
            model_name='post',
            name='type_post',
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default=None, max_length=100, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(default=None, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_ru',
            field=models.CharField(default=None, max_length=100, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.CharField(choices=[('TK', 'Танки'), ('HL', 'Хилы'), ('DD', 'ДД'), ('DI', 'Торговцы'), ('GM', 'Гилдмастеры'), ('QM', 'Квестгиверы'), ('BS', 'Кузнецы'), ('TN', 'Кожевники'), ('PM', 'Зельевары'), ('SM', 'Мастера заклинаний')], default='TK', max_length=2),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Author',
        ),
        migrations.DeleteModel(
            name='MyModel',
        ),
        migrations.DeleteModel(
            name='PostCategory',
        ),
    ]