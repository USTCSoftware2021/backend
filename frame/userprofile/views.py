from django import http
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm

# Create your views here.


def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data.get(
                'username'), password=data.get('password'))
            if user:
                # save user data to session
                login(request, user)
                return redirect('home')
            else:
                return HttpResponse('<h1>Incorrect username or password.</h1>')
        else:
            return HttpResponse('<h1>Invalid username or password.</h1>')
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': UserLoginForm}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse('<h1>Please use GET or POST to request data.</h1>')


def user_logout(request):
    logout(request)
    return redirect('home')


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data.get('password'))
            new_user.save()
            login(request, new_user)
            return redirect('home')
        else:
            return HttpResponse('<h1>Incorrect Form.</h1>')
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form': user_register_form}
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse('<h1>Please use POST or GET to request data.</h1>')
