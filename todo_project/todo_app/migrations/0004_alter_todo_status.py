# Generated by Django 5.1.3 on 2024-11-27 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_app', '0003_todo_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('In-Progress', 'In-Progress'), ('Completed', 'Completed')], default='In-Progress', max_length=20),
        ),
    ]
