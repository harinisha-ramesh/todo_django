# Generated by Django 5.1.3 on 2024-11-27 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0006_remove_todo_completed_alter_todo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
