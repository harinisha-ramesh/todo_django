from django.db import models
from django.contrib.auth.models import User


class Todo(models.Model):
    STATUS_CHOICES = [
        ('All', 'All'),
        ('In-Progress', 'In-Progress'),
        ('Completed', 'Completed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    task_name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='All')

    def __str__(self):
        return self.task_name

