from __future__ import absolute_import,unicode_literals

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'go.settings')

from celery import Celery

# import django
# django.setup()


app = Celery('go')

app.config_from_object('django.conf:settings', namespace='')

app.conf.beat_schedule = {
    'every_15' :{ 
        'task':'core.tasks.print_lol',
        'schedule':1,
        'args':(1,2,),
    }
}


app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')