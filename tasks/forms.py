from django.forms import ModelForm
from . import models


class CreateNewTask(ModelForm):
    class Meta:
        model = models.Task
        fields = ['task_name', 'task_description']
        
class CreateNewProject(ModelForm):
    class Meta:
        model = models.Project
        fields = ['project_name', 'project_description']