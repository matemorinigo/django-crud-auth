from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Project(models.Model):
    project_name = models.CharField(max_length=200, )
    project_description=models.TextField(blank=True)

    def __str__(self):
        return self.project_name

class Task(models.Model):
    task_name=models.CharField(max_length=200)
    task_description=models.TextField(blank=True)
    task_project=models.ForeignKey(Project, on_delete=models.CASCADE)
    task_isDone=models.BooleanField(default=False)
    task_user=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name