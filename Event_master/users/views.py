from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginUserForm, RegisterUserForm

from django.contrib.auth.models import User




class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/entrance.html'
    extra_context = {'title': "Авторизация"}


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))


def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/welcome.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/registration.html', {'form': form})