from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['task_name', 'description'] 

    def clean_is_completed(self):
        """Map the checkbox to the correct status."""
        return 'In Progress'