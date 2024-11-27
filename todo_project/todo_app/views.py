from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView,LogoutView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.views import View
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import * 

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True 
    success_url = reverse_lazy('todo_list')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    http_method_names = ['get', 'post']

@login_required
def todo_list(request):
    """A todo list  page that requires login to view"""
    status_filter = request.GET.get('status', None)  
    if status_filter:
        status_filter = status_filter.strip().capitalize()
        if status_filter == "All":
            todos = Todo.objects.filter(user=request.user)  
        else:
            todos = Todo.objects.filter(user=request.user, status=status_filter)
    else:
        todos = Todo.objects.filter(user=request.user)

    if request.method == 'POST':
        if 'toggle_task' in request.POST:
            # Handle checkbox toggle for completing or reverting tasks
            task_id = request.POST.get('task_id')
            try:
                task = Todo.objects.get(id=task_id, user=request.user)
                task.completed = not task.completed
                if task.completed:
                    # task.completed = False
                    task.status = "In-Progress"
                else:
                    # task.completed = True
                    task.status = "Completed"
                task.save()
            except Todo.DoesNotExist:
                pass  
            return redirect('todo_list')
        else:
            # Handle adding a new task
            form = TodoForm(request.POST)
            if form.is_valid():
                task_name = form.cleaned_data['task_name']
                description = form.cleaned_data['description']
                status = 'In-Progress'
                Todo.objects.create(user=request.user, task_name=task_name, description=description, status=status)
                return redirect('todo_list')


    else:
        form = TodoForm()
    return render(request, 'registration/todo_list.html', {'todos': todos, 'form': form})  


class SignupView(View):
    """Handle the signup functionality"""

    def get(self, request):
        """Render the signup form"""
        if request.user.is_authenticated:  
            return redirect('todo_list')
        form = CustomUserCreationForm()  
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        """Handle the submission of the signup form"""
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('todo_list') 
        else:
            return render(request, 'registration/signup.html', {'form': form}) 



