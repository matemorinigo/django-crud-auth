# Generated by Django 4.1.7 on 2023-02-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_project_project_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='project_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='task_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
