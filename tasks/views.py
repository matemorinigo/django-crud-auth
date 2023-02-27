from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

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
                return redirect('index')

            except IntegrityError:
                return render(request, 'sign-up.html', {'form': UserCreationForm, 'message': 'User already exists'})

        return render(request, 'sign-up.html', {'form': UserCreationForm, 'message': 'Passwords doesnt match'})

@login_required
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

@login_required
def projects(request):
    projects = models.Project.objects.filter(project_user=request.user)

    return render(request, 'projects/projects.html', {
        'projects': projects
    })

@login_required
def create_project(request):
    if request.method == 'GET':
        return render(request, 'projects/create_project.html', {'form': forms.CreateNewProject})

    else:
        form = forms.CreateNewProject(request.POST)
        new_project = form.save(commit=False)
        new_project.project_user = request.user
        new_project.save()

        return redirect('projects')

@login_required
def project_detail(request, project_id):
    
    if request.method == 'GET':
        project = get_object_or_404(
            models.Project, pk=project_id, project_user=request.user)
        updateForm = forms.CreateNewProject(instance=project)

        return render(request, 'projects/project_detail.html', {
            'project': project,
            'updateForm': updateForm
        })

    else:
        try:
            project = get_object_or_404(
                models.Project, pk=project_id, project_user=request.user)
            updateForm = forms.CreateNewProject(request.POST, instance=project)
            updateForm.save()

            return redirect('projects')

        except:
            project = get_object_or_404(
                models.Project, pk=project_id, project_user=request.user)
            updateForm = forms.CreateNewProject(instance=project)

            return render(request, 'projects/project_detail.html', {
                'project': project,
                'updateForm': updateForm,
                'message': 'Error'
            })

@login_required
def tasks(request):
    try:

        if request.method == 'GET' or request.POST['filterby'] == "":
            tasks = models.Task.objects.filter(task_user=request.user)
            filter="All"

        else: 
            tasks = models.Task.objects.filter(task_user=request.user, task_isDone=request.POST['filterby'])
            filter = request.POST['filterby']

            print(filter)

        return render(request, 'tasks/tasks.html', {'tasks': tasks,
                                                'filter': filter})
    except:
        tasks = models.Task.objects.filter(task_user=request.user)
        filter = "All"
        return render(request, 'tasks/tasks.html', {'tasks': tasks,
                                                'filter': filter})

@login_required
def create_task(request):
    if request.method == 'GET':

        UserProjects = models.Project.objects.filter(project_user=request.user)

        return render(request, 'tasks/create_task.html', {
            'form': forms.CreateNewTask,
            'projects': UserProjects})

    else:
        try:
            form = forms.CreateNewTask(request.POST)
            new_task = form.save(commit=False)
            new_task.task_user = request.user
            new_task.task_project = get_object_or_404(models.Project, pk=request.POST['task_project'], project_user= request.user)
            new_task.save()
            return redirect('tasks')

        except ValueError:
            UserProjects = models.Project.objects.filter(
                project_user=request.user)
            return render(request, 'tasks/create_task.html', {
                'form': forms.CreateNewTask,
                'message': 'Provide valid information :(',
                'projects': UserProjects})

@login_required
def task_detail(request, task_id):
    projects = models.Project.objects.filter(project_user=request.user)
    if request.method == 'GET':

        task = get_object_or_404(
            models.Task, pk=task_id, task_user=request.user)
        updateForm = forms.CreateNewTask(instance=task)

        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'projects':projects,
            'updateForm': updateForm})
    else:
        try:
            task = get_object_or_404(
                models.Task, pk=task_id, task_user=request.user)
            updateForm = forms.CreateNewTask(request.POST, instance=task)
            updatedTask = updateForm.save(commit=False)
            updatedTask.task_project = get_object_or_404(models.Project,pk=request.POST['task_project'], project_user=request.user)
            updatedTask.save()

            return redirect('tasks')

        except:
            task = get_object_or_404(
                models.Task, pk=task_id, task_user=request.user)
        updateForm = forms.CreateNewTask(instance=task)

        return render(request, 'tasks/task_detail.html', {
            'task': task,
            'projects':projects,
            'updateForm': updateForm,
            'message': 'Error'})
    
@login_required
def task_complete(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id, task_user=request.user)
    if request.method == 'POST':
        task.task_isDone = True
        task.save()

        print(task)


    return redirect('tasks')

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(models.Task, pk=task_id, task_user=request.user)
    if request.method =='POST':
        task.delete()

        return redirect('tasks')