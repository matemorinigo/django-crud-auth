from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate

# Create your views here.


def home(request):

    return render(request, 'index.html')


def signUp(request):

    if request.method == "GET":

        return render(request, 'sign-up.html', {
            'form': UserCreationForm(),
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('tasks')

            except IntegrityError:
                return render(request, 'sign-up.html', {'form': UserCreationForm, 'message': 'User already exists'})

        return render(request, 'sign-up.html', {'form': UserCreationForm, 'message': 'Passwords doesnt match'})


def tasks(request):

    return render(request, 'tasks.html')


def signOut(request):

    logout(request)

    return redirect('index')


def signIn(request):

    if request.method == 'GET':
        return render(request, 'sign-in.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'sign-in.html', {'form': AuthenticationForm,
            'message': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')


