from django.urls import path
from .views import *
# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/',CustomLoginView.as_view(),name='login'),
    path('todo/',todo_list,name='todo_list'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]
