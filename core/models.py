from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django_celery_beat.models import PeriodicTask, IntervalSchedule
# Create your models here.


# docs
#################
#  celery -A [project-name] worker --loglevel=info
#####################
#  celery -A [project-name] beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
# or celery -A [project-name] beat -l info -S django
######################3
# or combine recommended for development mode only
# celery -A [project-name] worker --beat --scheduler django --loglevel=info
####################
class Project(models.Model):
    project_name = models.CharField(max_length=200,unique=True)
    project_scan = models.IntegerField()  ### Scan interval
    project_status = models.BooleanField()


    def set_periodic_task(self, task_name):
        schedule = self.get_or_create_interval()
        PeriodicTask.objects.create(
            interval=schedule, 
            name=f'{self.project_name}-{self.id}', 
            task=task_name,
        )

    def get_or_create_interval(self):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=self.project_scan,
            period=IntervalSchedule.SECONDS,
        )
        return schedule

    def get_periodic_task(self, task_name):
        interval = self.get_or_create_interval()
        periodic_task = PeriodicTask.objects.get(
            interval=interval, 
            name=f'{self.project_name}-{self.id}', 
            task=task_name,
        )
        return periodic_task

    # def sync_disable_enable_task(self, task_name):
    #     periodic_task = self.get_periodic_task(task_name)
    #     periodic_task.enabled = self.project_status
    #     periodic_task.save()


@receiver(post_save, sender=Project)
def set_or_sync_periodic_task(sender, instance=None, created=False, **kwargs):
    if created:
        instance.set_periodic_task(task_name='project_tasks')
    # else:
    #     instance.sync_disable_enable_task(task_name='project_tasks')