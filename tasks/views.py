from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from . import forms, models

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


def signOut(request):

    logout(request)

    return redirect('index')


def signIn(request):

    if request.method == 'GET':
        return render(request, 'sign-in.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'sign-in.html', {
                'form': AuthenticationForm,
                'message': 'Username or password is incorrect'})
        else:
            login(request, user)
            return redirect('tasks')


def projects(request):
    projects = models.Project.objects.filter(project_user=request.user)


    return render(request, 'projects/projects.html',{
        'projects':projects
    })


def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {'form': forms.CreateNewProject})

    else:
        form = forms.CreateNewProject(request.POST)
        new_project = form.save(commit=False)
        new_project.project_user = request.user
        new_project.save()

        return redirect('projects')


def project_detail(request, project_id):
    if request.method == 'GET':
        project = get_object_or_404(
            models.Project, pk=project_id, project_user=request.user)
        updateForm = forms.CreateNewProject(instance=project)
        
        return render(request, 'projects/project_detail.html', {
            'project':project,
            'updateForm':updateForm
        })
    
    else:
        try:
            project = get_object_or_404(models.Project, pk=project_id, project_user = request.user)
            updateForm = forms.CreateNewProject(request.POST, instance=project)
            updateForm.save()
            
            return redirect('projects')
        
        except:
            project = get_object_or_404(
            models.Project, pk=project_id, project_user=request.user)
            updateForm = forms.CreateNewProject(instance=project)
        
            return render(request, 'projects/project_detail.html', {
                'project':project,
                'updateForm':updateForm,
                'message':'Error'
            })


def tasks(request):

    tasks = models.Task.objects.filter(task_user=request.user)

    return render(request, 'tasks/tasks.html', {'tasks': tasks})


def create_task(request):
    if request.method == 'GET':

        return render(request, 'tasks/create_task.html', {
            'form': forms.CreateNewTask})

    else:
        try:
            form = forms.CreateNewTask(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.project = 1
            return redirect('tasks')

        except ValueError:
            return render(request, 'tasks/create_task.html', {
                'form': forms.CreateNewTask,                                                'message': 'Provide valid information :('})


def task_detail(request, task_id):
    if request.method == 'GET':

        task = get_object_or_404(models.Task, pk=task_id, task_user=request.user)
        updateForm = forms.CreateNewTask(instance=task)


        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'updateForm': updateForm })
    else:
        try:
            task = get_object_or_404(models.Task, pk=task_id, task_user=request.user)
            updateForm = forms.CreateNewTask(request.POST, instance=task)
            updateForm.save()

            return redirect('tasks')
        
        except:
            task = get_object_or_404(models.Task, pk=task_id, task_user=request.user)
        updateForm = forms.CreateNewTask(instance=task)


        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'updateForm': updateForm,
            'message': 'Error'})
