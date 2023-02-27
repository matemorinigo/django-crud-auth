from django.contrib import admin
from . import models
# Register your models here.
class readonly_project(admin.ModelAdmin):
    readonly_fields=("project_date",)

class readonly_task(admin.ModelAdmin):
    readonly_fields=("task_date",)

admin.site.register(models.Project, readonly_project)
admin.site.register(models.Task, readonly_task)