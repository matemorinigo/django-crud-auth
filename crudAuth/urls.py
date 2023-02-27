"""crudAuth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signUp,name="signup"),
    path('', views.home, name="index"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/create', views.create_task, name="create-task"),
    path('tasks/<int:task_id>', views.task_detail, name="task-detail"),
    path('projects/', views.projects, name="projects"),
    path('projects/create', views.create_project, name="create-project"),
    path('projects/<int:project_id>', views.project_detail, name="project-detail"),
    path('logout/', views.signOut, name="logout"),
    path('login/', views.signIn, name="login")
]
