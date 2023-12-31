from celery import Celery

app = Celery('your_project_name')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
