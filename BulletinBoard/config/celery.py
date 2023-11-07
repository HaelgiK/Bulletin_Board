import os
from celery import Celery
from celery.schedules import crontab



# Связываем настройки Django с настройками Celery через переменную окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# Создаём экземпляр приложения Celery и устанавливаем для него файл конфигурации.
# Указываем пространство имён, чтобы Celery сам находил все необходимые настройки
# в общем конфигурационном файле settings.py.
# Он их будет искать по шаблону «CELERY_***»
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
# Указываем Celery автоматически искать задания в файлах tasks.py
# каждого приложения проекта
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every_monday_task': {
        'task': 'board.tasks.weekly_mailing',
        'schedule': crontab(hour=8, minute=00, day_of_week='monday'),
#        'schedule': crontab(),
    }
}

app.autodiscover_tasks()
