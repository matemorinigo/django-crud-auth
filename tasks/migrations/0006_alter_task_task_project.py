# Generated by Django 4.1.7 on 2023-02-27 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0005_project_project_date_task_task_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tasks.project'),
        ),
    ]
