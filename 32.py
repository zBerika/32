INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
]

from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30, verbose_name="სახელი")
    last_name = models.CharField(max_length=30, verbose_name="გვარი")
    email = models.EmailField(unique=True, verbose_name="ელ. ფოსტა")
    age = models.PositiveIntegerField(verbose_name="ასაკი")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" 

from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserForm

def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'users/user_form.html', {'form': form})

def user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})

def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})

from django.urls import path
from .views import user_list, user_create, user_update, user_delete

urlpatterns = [
    path('', user_list, name='user_list'),
    path('create/', user_create, name='user_create'),
    path('<int:pk>/edit/', user_update, name='user_update'),
    path('<int:pk>/delete/', user_delete, name='user_delete'),
]
