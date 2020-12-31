from __future__ import absolute_import,unicode_literals
from celery import shared_task
from celery.decorators import task
from .models import Project
@shared_task
def sum(x,y):
    return x+y

@shared_task
def print_lol(x,y):
    print('hello')

@shared_task(name='project_tasks')
def Project_Tasks():
    print("common")
    # get_all_projects = Project.objects.all()
    # for each_project in get_all_projects:
    #     if each_project.project_status == True: ### Checking if it "Scan" is allowed.
    #         get_interval = each_project.project_scan
    #         get_name = each_project.project_name
    #         print("commmmmmmmmmmmmon")